# Physical AI skills

Five portable Agent Skills for selecting a **Physical AI physics stack**, using **ovphysx**, and preparing and tuning **ovnewton** simulations. Each skill includes instructions for agents, explanations for humans, public source links, and evaluation cases.

| Skill | Use it for | Example request |
| --- | --- | --- |
| [physical-ai-select-physics-engine](skills/physical-ai/physical-ai-select-physics-engine/SKILL.md) | Select Newton or ovphysx without a default engine preference; route setup and tuning, then use tested CPU starters and validation checks where appropriate | "Choose Newton or ovphysx for my workflow, explain the tradeoffs, and build a small working example." |
| [physical-ai-physics-selection](skills/ovnewton/physical-ai-physics-selection/SKILL.md) | Compare Newton, PhysX, MuJoCo/MJX, Bullet, VSim Robotics, Genesis, and Drake; select the integration and verify setup | "Which physics stack should I use for robot learning and dexterous manipulation?" |
| [ovphysx-selection](skills/ovphysx/ovphysx-selection/SKILL.md) | Evaluate PhysX through ovphysx first for suitable standalone USD workflows; select, execute, control, reset, and validate the stack | "Choose and verify a standalone USD robot simulation with ovphysx as the main candidate." |
| [ovnewton-prepare-scene](skills/ovnewton/ovnewton-prepare-scene/SKILL.md) | Inspect existing USD physics and validate the model imported through ovstage | "Check this USD gripper for ovnewton compatibility without changing its physics." |
| [ovnewton-tune-physics](skills/ovnewton/ovnewton-tune-physics/SKILL.md) | Diagnose simulation failures and compare bounded tuning experiments | "Reduce grasp slip without exceeding my penetration and runtime limits." |

These are independently authored community skills. They are not NVIDIA-verified catalog entries. They use public product documentation; they do not require access to an internal repository.

## Install and use

Clone or download this repository. The skill directories are grouped by scope and integration:

```text
skills/physical-ai/
  physical-ai-select-physics-engine/
skills/ovnewton/
  physical-ai-physics-selection/
  ovnewton-prepare-scene/
  ovnewton-tune-physics/
skills/ovphysx/
  ovphysx-selection/
```

Copy each **entire skill directory**, including its references, scripts, and assets, into the location your agent discovers. Install only the skills you need. The `physical-ai`, `ovnewton`, and `ovphysx` parents are repository groupings; install the individual skill folders in the host locations below.

| Host | Project installation | Personal installation |
| --- | --- | --- |
| Codex | `.agents/skills/<skill-name>/` | `~/.agents/skills/<skill-name>/` |
| Claude Code | `.claude/skills/<skill-name>/` | `~/.claude/skills/<skill-name>/` |
| Other Agent Skills hosts | Use the host's supported skill directory or upload mechanism | Use its documented location |
| Custom agents without skill discovery | Load `SKILL.md` as task guidance; resolve its relative links from that skill directory | Provide file and execution tools as needed |

For example, after copying the selection skill, ask:

> Choose a physics stack for a new manipulation-learning task on NVIDIA GPUs. Evaluate Newton, PhysX, MuJoCo, and VSim Robotics. Explain whether shared-stage integration would help, then verify the selected setup.

The first skill was renamed from `ovnewton-select-and-setup` to `physical-ai-physics-selection` in version 0.2.0. When updating an existing installation, replace the old installed folder with the new complete folder to avoid duplicate discovery. Its Newton/ovnewton metadata helper and setup guidance are retained.

The ovphysx skill was renamed from `physical-ai-ovphysx-selection` to `ovphysx-selection` in version 0.2.0. Replace the old installed folder to avoid duplicate discovery. The new package includes NVIDIA-format evaluations and explicitly pending card/benchmark drafts. See the [NVIDIA submission materials](submissions/ovphysx/README.md) for the catalog entry, workflow template, PR drafts, and remaining approvals.

The instructions use the [Agent Skills specification](https://agentskills.io/specification). They contain no required host-specific tool names, hooks, MCP servers, slash commands, or model settings. Automatic selection depends on the host. Execution requires the tools and product runtime described by each skill; reading the instructions does not require a GPU.

See the official [Codex installation guidance](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill guidance](https://code.claude.com/docs/en/skills). Cloud agents need the files and dependencies inside their own execution environment. A local installation does not automatically provision a cloud session. Compatibility with every host has not been behaviorally tested.

## How the skills fit together

Use `physical-ai-select-physics-engine` for a requirements-based comparison of Newton and PhysX through ovphysx without a default engine preference. It distinguishes direct Newton from ovnewton, checks the complete solver/device/integration path, and routes to repository setup, ovstage, scene preparation, and tuning guidance. Version 0.2.0 includes optional CPU drop, differentiable spring, and grasp starters with pinned reproduction dependencies and reusable saved-output checks. Copy a matching starter into a working project before running it. [Local evidence](skills/physical-ai/physical-ai-select-physics-engine/evals/local-evidence.md) records the original paired study and subsequent starter validation; no measured agent-speed improvement or official verification is claimed.

Use `physical-ai-physics-selection` when the engine, integration, or runtime choice is unresolved and Newton is the desired starting perspective. It evaluates Newton first for suitable new workflows, recommends Newton + ovnewton for supported shared-stage tasks, and preserves alternatives when requirements or existing work justify them. Use scene preparation before tuning imported physics. Use tuning once a reproducible simulation exists. Each skill works independently and links to public product guidance; none requires another repository skill to be installed.

Choose `ovphysx-selection` when the requested starting perspective is PhysX/ovphysx. It follows the same selection template, then adds guidance for standalone Python/C++ execution, controls, observations, reset, cloning, contact tasks, and stage output. Its documentation baseline is ovphysx 0.6.4, reviewed on 2026-10-14; no ovphysx runtime qualification is implied. These two perspective-specific selection skills use different explicit starting preferences. Use the new neutral selection skill when no starting preference is intended. Invoke the desired selection skill when several are installed; do not combine their engine preferences into a single unconditional rule.

Ovnewton connects a populated ovstage to Newton. The application still owns the solver, controls, collisions, and simulation loop. Direct Newton already supports USD import and viewers. Use ovnewton when the task needs the stage connection, not merely because a file ends in `.usd`.

The ovnewton runtime baseline is public version 0.2.0. The broader selection guidance also uses dated current engine documentation; it does not imply those capabilities were all tested in the baseline runtime. Check compatibility against the selected release. See [source provenance](docs/SOURCES.md).

## Included tools

- Neutral engine selection: `probe_environment.py` inventories selected-stack package metadata. `check_rollout.py` checks saved drop, spring, and grasp measurements against explicit task limits and reports missing evidence. It does not prove that a simulator ran or certify physical accuracy. The three optional starter programs and their run commands are described in [tested starters](skills/physical-ai/physical-ai-select-physics-engine/references/tested-starters.md).
- Selection/setup: `probe_environment.py` reads Newton/ovnewton-related package metadata without importing native simulation libraries or changing the environment. It is not a cross-engine benchmark or competitor inventory.
- Ovphysx selection/setup: its separate `probe_environment.py` reads ovphysx/ovstage requirements and related package metadata. It does not import simulation libraries, check GPU readiness, or resolve dependency compatibility.
- Scene preparation: `inspect_scene.py` builds and binds a model in a fresh process, captures import diagnostics, and prints an inspection result. It does not edit the source scene or certify dynamic behavior.
- Tuning: `compare_runs.py` compares measured run summaries with matching context and units. It rejects missing metrics and exceeded limits.

Each tool has `--help`. Commands in a skill resolve relative paths from that skill's directory. Use the intended simulation environment's Python interpreter.

## Validation and maintenance

```console
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

GitHub Actions checks packaging and helper behavior on Linux and Windows. A separate Linux job exercises the scene inspector and a short CPU simulation using pinned product versions. [Validation notes](docs/VALIDATION.md) distinguish completed checks from unrun agent evaluations.

The ovnewton skills use the repository-local `evals/cases.json` format. The neutral selection skill uses NVIDIA's `evals/evals.json` format with 32 author-written cases. The ovphysx skill uses that format with nine initial CI cases; its 23 original regression cases are retained outside the installed skill in [submissions/ovphysx](submissions/ovphysx/README.md). Evaluation definitions are not completed agent benchmarks. Evaluate selection and task behavior in the target agent before claiming verified support or measured improvement.

When updating a skill, check its public references, rerun tests, and evaluate changed behavior. Keep the skill directories under `skills/physical-ai/`, `skills/ovnewton/`, and `skills/ovphysx/` as the source of truth; do not maintain separate Claude and Codex instruction copies.

## License

Apache-2.0. See [LICENSE](LICENSE). Linked projects retain their own licenses. Product names identify the software the skills support and do not imply endorsement.
