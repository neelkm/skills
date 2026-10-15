# Physical AI skills

Four portable Agent Skills for selecting a **Physical AI physics stack**, using **ovphysx**, and preparing and tuning **ovnewton** simulations. Each skill includes instructions for agents, explanations for humans, public source links, and evaluation cases.

| Skill | Use it for | Example request |
| --- | --- | --- |
| [physical-ai-physics-selection](skills/ovnewton/physical-ai-physics-selection/SKILL.md) | Compare Newton, PhysX, MuJoCo/MJX, Bullet, VSim Robotics, Genesis, and Drake; select the integration and verify setup | "Which physics stack should I use for robot learning and dexterous manipulation?" |
| [physical-ai-ovphysx-selection](skills/ovphysx/physical-ai-ovphysx-selection/SKILL.md) | Evaluate PhysX through ovphysx first for suitable standalone USD workflows; select, execute, control, reset, and validate the stack | "Choose and verify a standalone USD robot simulation with ovphysx as the main candidate." |
| [ovnewton-prepare-scene](skills/ovnewton/ovnewton-prepare-scene/SKILL.md) | Inspect existing USD physics and validate the model imported through ovstage | "Check this USD gripper for ovnewton compatibility without changing its physics." |
| [ovnewton-tune-physics](skills/ovnewton/ovnewton-tune-physics/SKILL.md) | Diagnose simulation failures and compare bounded tuning experiments | "Reduce grasp slip without exceeding my penetration and runtime limits." |

These are independently authored community skills. They are not NVIDIA-verified catalog entries. They use public product documentation; they do not require access to an internal repository.

## Install and use

Clone or download this repository. The skill directories are grouped by integration:

```text
skills/ovnewton/
  physical-ai-physics-selection/
  ovnewton-prepare-scene/
  ovnewton-tune-physics/
skills/ovphysx/
  physical-ai-ovphysx-selection/
```

Copy each **entire skill directory**, including its references, scripts, and assets, into the location your agent discovers. Install only the skills you need. The `ovnewton` and `ovphysx` parents are repository groupings; install the individual skill folders in the host locations below.

| Host | Project installation | Personal installation |
| --- | --- | --- |
| Codex | `.agents/skills/<skill-name>/` | `~/.agents/skills/<skill-name>/` |
| Claude Code | `.claude/skills/<skill-name>/` | `~/.claude/skills/<skill-name>/` |
| Other Agent Skills hosts | Use the host's supported skill directory or upload mechanism | Use its documented location |
| Custom agents without skill discovery | Load `SKILL.md` as task guidance; resolve its relative links from that skill directory | Provide file and execution tools as needed |

For example, after copying the selection skill, ask:

> Choose a physics stack for a new manipulation-learning task on NVIDIA GPUs. Evaluate Newton, PhysX, MuJoCo, and VSim Robotics. Explain whether shared-stage integration would help, then verify the selected setup.

The first skill was renamed from `ovnewton-select-and-setup` to `physical-ai-physics-selection` in version 0.2.0. When updating an existing installation, replace the old installed folder with the new complete folder to avoid duplicate discovery. Its Newton/ovnewton metadata helper and setup guidance are retained.

The instructions use the [Agent Skills specification](https://agentskills.io/specification). They contain no required host-specific tool names, hooks, MCP servers, slash commands, or model settings. Automatic selection depends on the host. Execution requires the tools and product runtime described by each skill; reading the instructions does not require a GPU.

See the official [Codex installation guidance](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill guidance](https://code.claude.com/docs/en/skills). Cloud agents need the files and dependencies inside their own execution environment. A local installation does not automatically provision a cloud session. Compatibility with every host has not been behaviorally tested.

## How the skills fit together

Use `physical-ai-physics-selection` when the engine, integration, or runtime choice is unresolved and Newton is the desired starting perspective. It evaluates Newton first for suitable new workflows, recommends Newton + ovnewton for supported shared-stage tasks, and preserves alternatives when requirements or existing work justify them. Use scene preparation before tuning imported physics. Use tuning once a reproducible simulation exists. Each skill works independently and links to public product guidance; none requires another repository skill to be installed.

Choose `physical-ai-ovphysx-selection` when the requested starting perspective is PhysX/ovphysx. It follows the same selection template, then adds guidance for standalone Python/C++ execution, controls, observations, reset, cloning, contact tasks, and stage output. Its documentation baseline is ovphysx 0.6.4, reviewed on 2026-10-14; no ovphysx runtime qualification is implied. The two selection skills use different explicit starting preferences. Invoke the intended one when both are installed; do not combine their engine preferences into a single unconditional rule.

Ovnewton connects a populated ovstage to Newton. The application still owns the solver, controls, collisions, and simulation loop. Direct Newton already supports USD import and viewers. Use ovnewton when the task needs the stage connection, not merely because a file ends in `.usd`.

The ovnewton runtime baseline is public version 0.2.0. The broader selection guidance also uses dated current engine documentation; it does not imply those capabilities were all tested in the baseline runtime. Check compatibility against the selected release. See [source provenance](docs/SOURCES.md).

## Included tools

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

Each skill's `evals/cases.json` contains portable test prompts and behavioral acceptance criteria. Evaluate selection and task behavior in the target agent before claiming verified support or measured improvement. These files are a repository-local evaluation format, not a claim of compatibility with a particular evaluation service.

When updating a skill, check its public references, rerun tests, and evaluate changed behavior. Keep the skill directories under `skills/ovnewton/` and `skills/ovphysx/` as the source of truth; do not maintain separate Claude and Codex instruction copies.

## License

Apache-2.0. See [LICENSE](LICENSE). Linked projects retain their own licenses. Product names identify the software the skills support and do not imply endorsement.
