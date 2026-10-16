# ASD-STE100-style version

## ovphysx-selection — submission draft

## Description

Use this skill to select ovphysx for a Physical AI workflow. Use it to establish a first working integration. Evaluate PhysX through ovphysx against the task requirements. Compare relevant alternatives. Produce a setup and verification plan for the selected release.

**Readiness:** This is an unsigned submission draft. NVIDIA release approval is pending. The official validation pipeline is pending. This card does not assert commercial readiness. It does not assert measured agent uplift.

## Owner

The proposed contributor is Neelakantan Mani. The ovphysx owning team must confirm the maintainer before submission. It must also confirm release ownership.

### License/Terms of Use

The proposed license is Apache-2.0. The complete text is in [LICENSE](../../skills/ovphysx/ovphysx-selection/LICENSE). The owning team must confirm the proposed NVIDIA copyright attribution. It must also confirm the skill-specific license location. The containing PhysX repository currently uses BSD-3-Clause. This package does not replace that repository's license.

## Use Case

Physical AI engineers and agents can use this skill to choose a standalone USD-based robot simulator. Teams can use it to plan ovphysx adoption. Developers can use it to check a first control/observation loop.

Workflows include rigid-body simulation and articulated-robot simulation. They also include shared ovstage applications and batched robot learning. Requirements can justify another engine. This skill does not supply a renderer or sensor stack. It does not supply a training framework or hardware control system.

### Deployment Geography for Use

Global. Applicable software terms and the user's deployment requirements still apply.

## Requirements / Dependencies

**Requires API Key or External Credential:** No skill-specific credential is required. Public documentation access is useful. Private asset or package access can require application-specific credentials.

**Credential Type(s):** The included metadata probe requires none. Do not put private credentials in generated code or reports.

Selection requires an agent with file and documentation access. The optional probe requires Python's standard library. Actual simulation requires a compatible ovphysx/ovstage installation. It also requires a supported OS and CPU. GPU features require compatible NVIDIA hardware and drivers.

Use the selected release's requirements. An installed package does not prove runtime readiness. No MCP server is required.

## Known Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Pre-release ovphysx APIs or package dependencies change | Check the installed release. Check matching source and bundled examples. Record versions. |
| A PhysX feature is unavailable through the selected API or device | Verify the complete asset, population, API, device, and application path. |
| Units, stage ordinals, buffer lifetimes, or reset semantics cause incorrect state | Use the contract for each attribute. Perform a bounded representative check. |
| The ovphysx preference biases selection | Let unsupported hard requirements override the preference. Compare the closest viable alternative. |
| A code recipe is mistaken for an executed benchmark or hardware qualification | Keep metadata, initialization, simulation, task validation, and measured performance evidence separate. |

## References

- [ovphysx source and documentation](https://github.com/NVIDIA-Omniverse/PhysX/tree/main/ovphysx)
- [Reviewed PhysX source snapshot](https://github.com/NVIDIA-Omniverse/PhysX/tree/6dc53585d7db07346f53d0598a5fd3bfdce47d8d/ovphysx)
- [Task-fit and source references](../../skills/ovphysx/ovphysx-selection/references/engine-selection.md)
- [Runtime and integration guidance](../../skills/ovphysx/ovphysx-selection/references/routing-and-runtime.md)
- [Workflow contracts](../../skills/ovphysx/ovphysx-selection/references/workflow-execution.md)
- [Selection validation](../../skills/ovphysx/ovphysx-selection/references/selection-validation.md)

## Skill Output

**Output Type(s):** The skill produces an engine/integration recommendation. It identifies conditions and open requirements. It can produce setup commands, code, a metadata inventory, and a bounded verification plan or observed result.

**Output Format:** Markdown, Python or C/C++ guidance, shell commands, and JSON from the metadata probe.

**Output Parameters:** These depend on the task. The probe uses `schema_version: 1`. It explicitly reports whether runtime, GPU, and dependency compatibility were tested.

**Other Properties Related to Output:** Claims must distinguish documentation from measurements. A justified alternative to ovphysx is a successful result.

## Evaluation Agents Used

No agent has completed live evaluation for this submission. The planned agents are Claude Code and Codex. Each must have a comparable baseline without the skill. Record actual models and harness versions when they run.

## Evaluation Tasks

The initial CI dataset has nine cases. Seven are positive. Two are negative routing cases. The submission packet retains a separate 23-case regression set outside the installed skill.

The CI dataset covers selection, a metadata probe, and a CPU lifecycle recipe. It also covers shared-stage ownership, batching/reset, mixed units, required gradients, and non-activation. Only the metadata probe requires execution. The CPU recipe does not establish runtime physics correctness.

## Evaluation Metrics Used

The planned benchmark dimensions follow the published NVIDIA example. They are security, correctness, discoverability, effectiveness, and efficiency. Retain the underlying signals. Retain task completion, token counts, elapsed time, trajectories, and final artifacts. Use actual results to calculate comparable changes from the baseline to the skill condition.

## Evaluation Results

Live evaluations are **not run**. Uplift is **not run**. See the [pending benchmark record](../../skills/ovphysx/ovphysx-selection/BENCHMARK.md). Local packaging checks do not replace NVIDIA's security scan. They do not replace live evaluation, signing, or release approval. The official pipeline must generate this card again. It must produce `skill.oms.sig`.

## Skill Versions

The skill package version is **0.2.0**. It is adapted from `physical-ai-ovphysx-selection` 0.1.0. Technical examples were reviewed against ovphysx **0.6.4**. The PhysX source commit was `6dc53585d7db07346f53d0598a5fd3bfdce47d8d`. The skill version and runtime version are distinct.

## Ethical Considerations

Simulation results do not establish physical-system safety. They do not establish real-world transfer. Users must validate their actual task, assets, and hardware before deployment. This skill does not authorize physical robot operation. Keep proprietary assets and credentials out of public evaluation artifacts. Confirm the owning team's release and risk review before publishing under NVIDIA ownership.

This is an ASD-STE100-style rewrite. It has not been checked for full compliance with the standard's writing rules and dictionary.
