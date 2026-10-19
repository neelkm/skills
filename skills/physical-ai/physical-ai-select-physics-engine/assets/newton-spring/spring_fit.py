# SPDX-License-Identifier: Apache-2.0
"""Learn spring stiffness by differentiating an actual Newton CPU rollout."""
from pathlib import Path
import json
import math
import os

ROOT = Path(__file__).resolve().parent
os.environ["WARP_CACHE_PATH"] = str(ROOT / ".cache" / "warp")
import numpy as np
import warp as wp
import newton
from newton.solvers import SolverSemiImplicit

wp.config.kernel_cache_dir = str(ROOT / ".cache" / "warp")
wp.config.quiet = True
wp.init()
wp.set_device("cpu")

DT = 0.01
STEPS = 100
TRUE_K = 25.0
INITIAL_K = 10.0


@wp.kernel
def add_loss(q: wp.array(dtype=wp.vec3), target: wp.array(dtype=float),
             index: int, count: int, loss: wp.array(dtype=float)):
    error = q[1][0] - target[index]
    wp.atomic_add(loss, 0, error * error / float(count))


def build():
    builder = newton.ModelBuilder(gravity=(0.0, 0.0, 0.0))
    builder.add_particle((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 0.0)
    builder.add_particle((1.0, 0.0, 0.0), (0.0, 0.0, 0.0), 1.0)
    builder.add_spring(0, 1, INITIAL_K, 0.0, 0.0)
    # add_spring uses the initial distance as its rest length: exactly 1 m.
    model = builder.finalize(device="cpu", requires_grad=True)
    model.particle_grid = None  # No particle collisions in this smooth spring experiment.
    model.particle_q.assign(np.array([[0, 0, 0], [1.2, 0, 0]], dtype=np.float32))
    return model, SolverSemiImplicit(model), model.control()


def main():
    model, solver, control = build()
    target = wp.zeros(STEPS, dtype=float, device="cpu")

    def rollout(k, gradient=False):
        model.spring_stiffness.assign(np.array([k], dtype=np.float32))
        model.spring_stiffness.grad.zero_()
        # Preserve every intermediate state for reverse-mode differentiation.
        states = [model.state() for _ in range(STEPS + 1)]
        loss = wp.zeros(1, dtype=float, device="cpu", requires_grad=True)
        tape = wp.Tape()
        if gradient:
            tape.__enter__()
        try:
            for i in range(STEPS):
                states[i].clear_forces()
                solver.step(states[i], states[i + 1], control, None, DT)
                wp.launch(add_loss, dim=1,
                          inputs=[states[i + 1].particle_q, target, i, STEPS, loss],
                          device="cpu")
        finally:
            if gradient:
                tape.__exit__(None, None, None)
        derivative = None
        if gradient:
            tape.backward(loss)
            derivative = float(model.spring_stiffness.grad.numpy()[0])
        trajectory = np.array([s.particle_q.numpy()[1, 0] for s in states[1:]])
        anchors = np.array([s.particle_q.numpy()[0] for s in states])
        value = float(loss.numpy()[0])
        if gradient:
            tape.zero()
        return value, derivative, trajectory, anchors

    # Target generation uses the same actual Newton solver, without a tape.
    _, _, target_positions, anchors = rollout(TRUE_K)
    target.assign(target_positions)
    initial_loss, automatic_gradient, initial_positions, _ = rollout(INITIAL_K, True)
    epsilon = 0.02
    plus = rollout(INITIAL_K + epsilon)[0]
    minus = rollout(INITIAL_K - epsilon)[0]
    numerical_gradient = (plus - minus) / (2.0 * epsilon)
    relative_error = abs(automatic_gradient - numerical_gradient) / max(
        abs(automatic_gradient), abs(numerical_gradient), 1.0e-10)

    # Adam uses only reverse-mode automatic gradients for parameter updates.
    k, first, second = INITIAL_K, 0.0, 0.0
    history = []
    for iteration in range(1, 151):
        value, gradient, _, _ = rollout(k, True)
        history.append({"iteration": iteration, "k": k, "loss": value, "gradient": gradient})
        first = 0.9 * first + 0.1 * gradient
        second = 0.999 * second + 0.001 * gradient * gradient
        corrected_first = first / (1.0 - 0.9 ** iteration)
        corrected_second = second / (1.0 - 0.999 ** iteration)
        k = max(0.001, k - 0.5 * corrected_first / (math.sqrt(corrected_second) + 1e-8))
    final_loss, _, final_positions, _ = rollout(k)

    times = DT * np.arange(1, STEPS + 1)
    exact = 1.0 + 0.2 * np.cos(math.sqrt(TRUE_K) * times)
    analytic_max_error = float(np.max(np.abs(target_positions - exact)))
    checks = {
        "actual_cpu_newton_simulation": bool(model.device.is_cpu),
        "finite_changing_trajectory": bool(np.all(np.isfinite(target_positions)) and np.ptp(target_positions) > 0.1),
        "fixed_anchor": bool(np.max(np.abs(anchors)) < 1e-7),
        "oscillation_matches_analytic_within_0_006_m": analytic_max_error < 0.006,
        "finite_nonzero_automatic_gradient": bool(math.isfinite(automatic_gradient) and abs(automatic_gradient) > 1e-8),
        "gradient_relative_error_below_0_02": relative_error < 0.02,
        "loss_reduced_by_at_least_99_percent": final_loss < initial_loss * 0.01,
        "stiffness_within_1_percent": abs(k - TRUE_K) / TRUE_K < 0.01,
    }
    metrics = {
        "device": str(model.device), "dt_seconds": DT, "steps": STEPS,
        "mass_kg": 1.0, "rest_length_m": 1.0, "initial_position_m": 1.2,
        "target_stiffness_N_per_m": TRUE_K, "initial_stiffness_N_per_m": INITIAL_K,
        "estimated_stiffness_N_per_m": k, "initial_loss_m_squared": initial_loss,
        "final_loss_m_squared": final_loss, "automatic_gradient": automatic_gradient,
        "finite_difference_gradient": numerical_gradient, "finite_difference_epsilon_N_per_m": epsilon,
        "gradient_relative_error": relative_error, "analytic_max_error_m": analytic_max_error,
        "checks": checks, "physical_behavior_passed": all(checks.values()),
    }
    (ROOT / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (ROOT / "optimization_history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    np.savetxt(ROOT / "trajectory.csv", np.column_stack([times, target_positions, initial_positions, final_positions, exact]),
               delimiter=",", header="time_s,target_m,initial_estimate_m,fitted_m,analytic_m", comments="")
    print(f"Initial loss: {initial_loss:.10g} m^2")
    print(f"Final loss:   {final_loss:.10g} m^2")
    print(f"Estimated stiffness: {k:.8f} N/m (target {TRUE_K}; initial {INITIAL_K})")
    print(f"Gradient check: automatic={automatic_gradient:.10g}, finite difference={numerical_gradient:.10g}, relative error={relative_error:.6g}")
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}: {name}")
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
