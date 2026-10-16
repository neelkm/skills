# Proposed title

Add ovphysx selection and first-run skill

# Proposed body

Physical AI users need to decide whether standalone ovphysx meets their task requirements before adopting its runtime. Add `skills/ovphysx-selection`, which evaluates ovphysx first, compares relevant alternatives, and guides users through a release-aware setup and representative verification check. Preserve existing framework integrations and allow hard requirements to rule out ovphysx.

The package includes focused references, a standard-library metadata probe, nine CI evaluation cases, and draft benchmark/card files. Add the approved NVIDIA validation-request workflow. The benchmark and card explicitly identify unperformed live evaluations; the NVIDIA pipeline must regenerate them and create the signature.

Validation evidence and outstanding scanner requirements are listed in the accompanying submission README. No physics runtime, GPU benchmark, paired agent evaluation, or signing run has been completed for this submission. The public local evaluator is pinned to `NVIDIA/SkillEvaluator@a53af93d0059409679179a0d6bd2f594a351a32e` (package version 0.5.0).

## Author and maintainer checks

- [ ] Confirm `NVIDIA-Omniverse/PhysX` is the owning repository and accept the new skill path.
- [ ] Confirm maintainer, copyright attribution, and all required open-source/IP and release approvals.
- [ ] Resolve the Apache-2.0 skill license within the existing BSD-3-Clause product repository. Do not replace the product license.
- [ ] Follow the existing root `CONTRIBUTING.md`, which includes the full DCO; sign off actual commits only after the contributor can certify them.
- [ ] Complete repository onboarding for NVIDIA validation, including the approved App/secret and signing access.
- [ ] Run `/nvskills-ci` from an authorized maintainer account and retain the actual security/evaluation evidence.
- [ ] Confirm paired Claude Code and Codex evaluations, measured CI duration, generated card/benchmark, and a valid signature for the final content.
- [ ] Merge only after required reviewers and checks approve the change.

## Catalog follow-up

After the approved source skill exists on the registered branch, open a separate NVIDIA/skills PR adding `components.d/ovphysx.yml`. The catalog should point to `skills/ovphysx-selection/`, which contains one `SKILL.md`. Do not hand-copy the skill into NVIDIA/skills' generated mirror.

This is a PR-body draft. It records no approvals, signed-off commits, or completed CI runs.
