# Local evidence for versions 0.1.0 and 0.2.0

This is a local test record, not an official NVSkills evaluation or NVIDIA verification. [Machine-readable results](local-results.json) retain outcomes, dependency versions, source hashes, and checker cases. Test date: 2026-10-19.

## Original paired study: 0.1.0

Three prompts each ran with and without the skill, using six fresh agents. Agents built and executed small Windows CPU applications. All six met their prototype task checks. Both conditions selected suitable paths; no clear engine-selection or build-effort advantage was observed.

| Task | Without skill | With skill | Observed behavior |
| --- | --- | --- | --- |
| USD drop with shared ovstage | ovphysx / TGS | ovphysx / TGS | Both fell, settled, and verified published stage state |
| Spring stiffness identification | Newton / SemiImplicit | Newton / SemiImplicit | Both recovered stiffness within 1%, checked automatic gradients, and compared with an analytic trajectory |
| Gripper lift | Newton / MuJoCo CPU | Newton / XPBD CPU | Both held; both failed to lift in a zero-friction control |

Both drop implementations needed API corrections and a smaller timestep. Both spring implementations needed an API correction. The baseline gripper required dependency alignment and measured contact forces and penetration. The skill-assisted gripper checked release but did not measure those contact quantities. These observations motivated exact starter dependencies/API usage, shorter routing, and explicit reusable validation.

The study used one trial per condition and prompt, explicit skill loading, and an approximate seven-minute work target. Implementations, versions, thresholds, and environment delays differed. Concurrent work and compilation prevent a controlled timing comparison. It does not establish statistical uplift, engine superiority, automatic discovery, GPU behavior, Linux ovnewton support, or real robot performance.

## Direct starter validation: 0.2.0

Copies of the three packaged starters ran on Windows x86_64 with Python 3.13.12 and their exact pinned dependencies. Four executions completed with process exit 0: box drop, spring fit, nominal grasp, and zero-friction grasp. The drop settled at a center height of approximately 0.1 m with matching stage readback. The spring estimate was approximately 25.0011 N/m for a 25 N/m target. The gripper held and released; the zero-friction control did not lift. [Starter instructions](../references/tested-starters.md) define commands, limits, and unverified quantities.

All 13 saved-output checker regression cases passed their expected outcome, including expected rejections for stale stage state, wrong gradient sign, non-finite samples, duplicate timestamps, missing required contact evidence, no lift, changed control mass, floor support, and a mismatched limit profile. Altered and synthetic records tested checker behavior; they are not additional physics evidence.

The initial drop shell pipeline waited on a native helper's inherited output handle after Python completed. Direct output to a log file confirmed Python exit 0. The waiting validation shell was closed; shared helper services were not stopped. This was a process-output issue, not a numerical test failure.

No new paired agent study of 0.2.0 has run. The changes address observed failure modes; their effect on agent speed or selection quality remains unmeasured. The [32 evaluation cases](evals.json) are author-written and have not passed the official evaluation workflow. No official benchmark, signature, production qualification, or standard-compliance claim follows from these local checks.

## ASD-STE100-style version

This document records local tests. It is not an official NVSkills evaluation. It does not establish NVIDIA verification. The [machine-readable results](local-results.json) contain outcomes, dependency versions, source hashes, and checker cases. The test date was 2026-10-19.

The original study tested version 0.1.0. It used three prompts. Each prompt had one test with the skill and one test without it. Six fresh agents built and ran small Windows CPU applications. All six met their prototype task checks. Both conditions selected suitable paths. The tests showed no clear improvement in engine selection or build effort.

| Task | Without skill | With skill | Observed behavior |
| --- | --- | --- | --- |
| Drop a USD box with shared ovstage | ovphysx / TGS | ovphysx / TGS | Both fell and settled. Both verified published stage state. |
| Identify spring stiffness | Newton / SemiImplicit | Newton / SemiImplicit | Both recovered stiffness within 1%. Both checked automatic gradients. Both compared with an analytic trajectory. |
| Lift a block with a gripper | Newton / MuJoCo CPU | Newton / XPBD CPU | Both held the block. Neither lifted it with zero friction. |

Both drop implementations needed API corrections. Both needed a smaller timestep. Both spring implementations needed an API correction. The gripper without the skill required compatible dependency versions. It measured contact forces and penetration. The gripper with the skill checked release. It did not measure those contact quantities. These results led to exact starter dependencies and API usage. They also led to shorter routing and explicit reusable validation.

The study used one trial per condition and prompt. Agents loaded the skill explicitly. The work target was approximately seven minutes. Implementations, versions, thresholds, and environment delays differed. Concurrent work and compilation prevent a controlled timing comparison. The tests do not establish statistical improvement or engine superiority. They do not test automatic discovery, GPU behavior, Linux ovnewton support, or real robot performance.

Direct starter tests used version 0.2.0. Copies of all three starters ran on Windows x86_64 with Python 3.13.12. They used their exact pinned dependencies. Four executions returned process exit 0: box drop, spring fit, nominal grasp, and zero-friction grasp. The box settled at a center height of approximately 0.1 m. The published stage pose matched. The spring estimate was approximately 25.0011 N/m. Its target was 25 N/m. The gripper held and released. The zero-friction control did not lift. The [starter instructions](../references/tested-starters.md) give commands, limits, and unverified quantities.

All 13 checker regression cases produced the expected result. The checker rejected stale stage state, a wrong gradient sign, non-finite samples, and duplicate timestamps. It rejected missing required contact evidence and a no-lift result. It also rejected a changed control mass, floor support, and a mismatched limit profile. Altered and synthetic records tested the checker. They are not additional physics evidence.

The initial drop shell pipeline waited after Python completed. A native helper had inherited an output handle. Direct output to a log file confirmed Python exit 0. The waiting validation shell was closed. Shared helper services were not stopped. This was a process-output issue. It was not a numerical test failure.

Version 0.2.0 has not had a new paired agent study. The changes address observed failures. Their effect on agent speed and selection quality remains unmeasured. The [32 evaluation cases](evals.json) are author-written. They have not passed the official evaluation workflow. The local checks do not establish an official benchmark, signature, production qualification, or compliance with a standard.
