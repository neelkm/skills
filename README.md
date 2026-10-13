# Physical AI skills

Three portable Agent Skills for selecting, preparing, and tuning **ovnewton** simulations. Each skill includes instructions for agents, explanations for humans, public source links, and evaluation cases.

| Skill | Use it for | Example request |
| --- | --- | --- |
| [ovnewton-select-and-setup](skills/ovnewton-select-and-setup/SKILL.md) | Decide between direct Newton and ovnewton; prepare and verify a compatible runtime | "Does this robot workflow need ovnewton? Set up a small CPU test." |
| [ovnewton-prepare-scene](skills/ovnewton-prepare-scene/SKILL.md) | Inspect existing USD physics and validate the model imported through ovstage | "Check this USD gripper for ovnewton compatibility without changing its physics." |
| [ovnewton-tune-physics](skills/ovnewton-tune-physics/SKILL.md) | Diagnose simulation failures and compare bounded tuning experiments | "Reduce grasp slip without exceeding my penetration and runtime limits." |

These are independently authored community skills. They are not NVIDIA-verified catalog entries. They use public product documentation; they do not require access to an internal repository.

## Install and use

Clone or download this repository. Copy the **entire skill directory**, including its references, scripts, and assets, into the location your agent discovers. Install only the skills you need.

| Host | Project installation | Personal installation |
| --- | --- | --- |
| Codex | `.agents/skills/<skill-name>/` | `~/.agents/skills/<skill-name>/` |
| Claude Code | `.claude/skills/<skill-name>/` | `~/.claude/skills/<skill-name>/` |
| Other Agent Skills hosts | Use the host's supported skill directory or upload mechanism | Use its documented location |
| Custom agents without skill discovery | Load `SKILL.md` as task guidance; resolve its relative links from that skill directory | Provide file and execution tools as needed |

For example, after copying the setup skill, ask:

> Use ovnewton-select-and-setup to assess my existing USD/ovstage application. Explain whether I need the bridge, then verify the smallest appropriate runtime.

The instructions use the [Agent Skills specification](https://agentskills.io/specification). They contain no required host-specific tool names, hooks, MCP servers, slash commands, or model settings. Automatic selection depends on the host. Execution requires the tools and product runtime described by each skill; reading the instructions does not require a GPU.

See the official [Codex installation guidance](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill guidance](https://code.claude.com/docs/en/skills). Cloud agents need the files and dependencies inside their own execution environment. A local installation does not automatically provision a cloud session. Compatibility with every host has not been behaviorally tested.

## How the skills fit together

Use selection/setup when the runtime or product choice is unresolved. Use scene preparation before tuning imported physics. Use tuning once a reproducible simulation exists. Each skill works independently and links to public product guidance; none requires the other two to be installed.

Ovnewton connects a populated ovstage to Newton. The application still owns the solver, controls, collisions, and simulation loop. Direct Newton already supports USD import and viewers. Use ovnewton when the task needs the stage connection, not merely because a file ends in `.usd`.

The skills target public ovnewton 0.2.0 documentation as their initial baseline. Package compatibility is checked against the selected release, not assumed from the latest Newton branch. See [source provenance](docs/SOURCES.md).

## Included tools

- Setup: `probe_environment.py` reads package metadata without importing native simulation libraries or changing the environment.
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

When updating a skill, check its public references, rerun tests, and evaluate changed behavior. Keep the `skills/` directories as the source of truth; do not maintain separate Claude and Codex instruction copies.

## License

Apache-2.0. See [LICENSE](LICENSE). Linked projects retain their own licenses. Product names identify the software the skills support and do not imply endorsement.
