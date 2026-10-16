# ovphysx-selection — submission draft

## Description

Select and establish a first working ovphysx integration for a Physical AI workflow. Evaluate PhysX through ovphysx against task requirements, compare relevant alternatives, and produce a release-aware setup and verification plan.

**Readiness:** Unsigned submission draft. NVIDIA release approval and the official validation pipeline are pending. This card does not assert commercial readiness or measured agent uplift.

## Owner

Proposed contributor: Neelakantan Mani. The ovphysx owning team must confirm the maintainer and release ownership before submission.

### License/Terms of Use

Apache-2.0; the complete text is in [LICENSE](LICENSE). The proposed NVIDIA copyright attribution and the skill-specific license placement require owning-team confirmation. The containing PhysX repository currently uses BSD-3-Clause; this package does not replace that repository's license.

## Use Case

Physical AI engineers and agents choosing a standalone USD-based robot simulator; teams planning ovphysx adoption; and developers checking a first control/observation loop. Workflows include rigid-body and articulated-robot simulation, shared ovstage applications, and batched robot learning. Requirements can justify another engine. This skill does not supply a renderer, sensor stack, training framework, or hardware control system.

### Deployment Geography for Use

Global, subject to applicable software terms and the user's deployment requirements.

## Requirements / Dependencies

**Requires API Key or External Credential:** No skill-specific credential is required. Public documentation access is useful. Private asset or package access can require application-specific credentials.

**Credential Type(s):** None for the included metadata probe. Do not place private credentials in generated code or reports.

Selection needs an agent with file and documentation access. The optional probe needs Python's standard library. Actual simulation needs a compatible ovphysx/ovstage installation and a supported OS/CPU. GPU features additionally need compatible NVIDIA hardware and drivers. Consult the selected release's requirements; an installed package is not proof of runtime readiness. No MCP server is required.

## Known Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Pre-release ovphysx APIs or package dependencies change | Check the installed release, matching source, and bundled examples; record versions. |
| A PhysX feature is unavailable through the selected API or device | Verify the entire asset, population, API, device, and application path. |
| Units, stage ordinals, buffer lifetimes, or reset semantics produce incorrect state | Use the per-attribute contract and a bounded representative check. |
| The ovphysx preference biases selection | Let unsupported hard requirements override the preference and compare the closest viable alternative. |
| A code recipe is mistaken for an executed benchmark or hardware qualification | Separate metadata, initialization, simulation, task validation, and measured performance evidence. |

## References

- [ovphysx source and documentation](https://github.com/NVIDIA-Omniverse/PhysX/tree/main/ovphysx)
- [Reviewed PhysX source snapshot](https://github.com/NVIDIA-Omniverse/PhysX/tree/6dc53585d7db07346f53d0598a5fd3bfdce47d8d/ovphysx)
- [Task-fit and source references](references/engine-selection.md)
- [Runtime and integration guidance](references/routing-and-runtime.md)
- [Workflow contracts](references/workflow-execution.md)
- [Selection validation](references/selection-validation.md)

## Skill Output

**Output Type(s):** Engine/integration recommendation, conditions and open requirements, setup commands, code, metadata inventory, and a bounded verification plan or observed result.

**Output Format:** Markdown, Python or C/C++ guidance, shell commands, and JSON from the metadata probe.

**Output Parameters:** Task-specific. The probe uses `schema_version: 1` and explicitly reports whether runtime, GPU, and dependency compatibility were tested.

**Other Properties Related to Output:** Claims must distinguish documentation from measurements. A justified alternative to ovphysx is a successful result.

## Evaluation Agents Used

None for live evaluation of this submission. Planned agents: Claude Code and Codex, each with a comparable without-skill baseline. Record actual models and harness versions when run.

## Evaluation Tasks

Nine initial CI cases: seven positive and two negative routing cases. A separate 23-case regression set is retained in the submission packet outside the installed skill. The CI dataset covers selection, a metadata probe, a CPU lifecycle recipe, shared-stage ownership, batching/reset, mixed units, required gradients, and non-activation. Only the metadata probe requires execution; the CPU recipe does not establish runtime physics correctness.

## Evaluation Metrics Used

Planned benchmark dimensions follow the published NVIDIA example: security, correctness, discoverability, effectiveness, and efficiency. Retain the underlying signals, task completion, token counts, elapsed time, trajectories, and final artifacts. Use actual results to calculate comparable baseline-to-skill changes.

## Evaluation Results

Live evaluations and uplift are **not run**. See [BENCHMARK.md](BENCHMARK.md) for the pending benchmark record. Local packaging checks do not replace NVIDIA's security scan, live evaluation, signing, or release approval. The official pipeline must regenerate this card and produce `skill.oms.sig`.

## Skill Versions

Skill package: **0.2.0**. Adapted from `physical-ai-ovphysx-selection` 0.1.0. Technical examples were reviewed against ovphysx **0.6.4**, PhysX source commit `6dc53585d7db07346f53d0598a5fd3bfdce47d8d`. The skill version and runtime version are distinct.

## Ethical Considerations

Simulation results do not establish physical-system safety or real-world transfer. Users must validate their actual task, assets, and hardware before deployment. This skill does not authorize physical robot operation. Keep proprietary assets and credentials out of public evaluation artifacts. Confirm the owning team's release and risk review before publishing under NVIDIA ownership.
