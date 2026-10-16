# Proposed title

Register ovphysx-selection from the PhysX repository

# Proposed body

Register the approved ovphysx selection skill from `NVIDIA-Omniverse/PhysX` at `skills/ovphysx-selection/`. The proposed catalog directory is `ovphysx-selection`. Submit this registration only after that source path exists on the registered branch and its required approvals and validation are complete.

## Onboarding type

- [x] New product onboarding (new `components.d/ovphysx.yml` file)
- [ ] Other (catalog change, README fix, infrastructure, etc.)

## For new product onboarding — author affirmations

By submitting this PR, I confirm on behalf of my team:

- [ ] **Skills cleared for open source release** by the owning team, with all required approvals in place
- [ ] **License selected:** Apache 2.0 / CC-BY 4.0 / Dual (Apache 2.0 + CC-BY 4.0). Proposed: Apache 2.0, pending owning-team confirmation.
- [ ] **No new license or new third-party component** introduced beyond what the source repo already carries
- [ ] **Source repo is public and under an NVIDIA-owned GitHub org**
- [ ] `.agents/skills/` or `skills/` path used for new entries (or existing path retained for legacy entries per `components.d/<slug>.yml`)

## Reviewer checklist (OSS Skills PIC)

- [ ] Author confirmations above are checked
- [ ] `components.d/ovphysx.yml` entry valid (required fields, unique `catalog_dir`, path exists in source repo, filename slug matches name)
- [ ] `SKILL.md` frontmatter spec-compliant (at least one sampled)
- [ ] No new license or third-party dependency introduced

## All PRs

- [ ] All commits signed off with DCO (`git commit -s`).

## Submission context

The proposed skill contains selection guidance, first-run instructions, a metadata probe, and nine initial evaluation cases. No new runtime dependency is introduced by the probe. The source repository's BSD-3-Clause license differs from the proposed skill's Apache-2.0 license. Resolve that boundary and the “no new license” affirmation with the owning team before checking it. Attach the approved source PR and final source revision when available.

This draft follows the NVIDIA/skills PR template. Unchecked affirmations are intentionally pending; this packet does not certify them.
