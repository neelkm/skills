# Validation record

Original record: 2026-10-13. The ovphysx addition is dated 2026-10-14, and its submission-format replacement is dated 2026-10-16. This record describes completed checks and the limits of the evidence. It is not a NVIDIA catalog certification or a live-agent benchmark.

## Ovphysx submission-format replacement: 2026-10-16

Replaced `physical-ai-ovphysx-selection` 0.1.0 with `ovphysx-selection` 0.2.0 at `skills/ovphysx/ovphysx-selection/`. The 12 source files match the prepared submission package. The old installable folder was removed, and installation links and the probe tests use the new name. [Submission materials](../submissions/ovphysx/README.md) include the proposed catalog registration, an inactive validation-workflow template, PR drafts, and report alternatives.

All four skills passed the repository validator: 30 ovnewton cases and nine ovphysx CI cases. The original 23 ovphysx cases remain in the separate submission directory, together with their converted NVIDIA-format dataset. The repository validator now accepts both dataset formats and checks expected-script paths. All 24 helper tests passed on Windows with Python 3.13, including three tests for dataset compatibility and rejection of invalid or ambiguous data. The renamed skill passed the skill-creator validator.

The preparation-time NVIDIA evaluator result remains incomplete: eight of 11 results passed; three security-related scanner results were unavailable. Its static quality heuristic was 89.5/100, grade B. These are not live-agent benchmark results. See the submission record for the pinned evaluator, actual evidence, and remaining owner/license, security, evaluation, and signing steps. This replacement did not run ovphysx physics, qualify a GPU, or submit to NVIDIA's catalog. The historical checks below retain their original scope and dates.

## Completed locally

- All three skill entrypoints passed the skill-creator metadata validator.
- The repository validator passed for all three skills. It checked portable metadata, resource links, and 30 evaluation-case definitions: 18 for physics selection and six each for scene preparation and tuning.
- All 18 helper tests passed on Windows with Python 3.13.12. The initial sandbox prevented access to temporary directories; the unchanged tests passed outside that sandbox.
- All Python files compiled successfully.
- The environment probe ran with no simulation packages installed and correctly reported metadata-only evidence, with runtime and GPU testing both false.

The first skill is now `physical-ai-physics-selection` version 0.2.0. Its revised metadata and resource links passed validation, and all 18 helper tests passed again after the directory rename. The helper implementation is unchanged. The added selection cases cover Newton preferences, alternatives, integration limits, gradients, hardware requirements, and unsupported comparative claims. Their structure was checked; their agent behavior was not executed.

## Runtime and agent scope

The local host does not provide a supported Linux ovnewton environment. [GitHub Actions run 38440362196](https://github.com/neelkm/skills/actions/runs/38440362196) passed portable checks on Linux and Windows, plus the Linux CPU integration job. The runtime used Python 3.12.15, ovnewton 0.2.0, Newton 1.6.0, Warp 1.17.0, and resolved ovstage 0.2.1.385922. Dependency consistency checks also passed.

The CPU job inspected the original falling-box fixture, checked body/shape counts, mass, and gravity, and passed eight-frame packaged examples with XPBD and VBD. Newton emitted a VBD deprecation warning: the packaged example uses the legacy default `rigid_compliant_alm=False`, which is planned to change. This result does not qualify the future default. The job did not test MuJoCo-Warp, CUDA execution, RTX rendering, long-horizon contact stability, or a trained policy.

The workflow repeats portable checks and CPU integration for subsequent revisions; see the [run history](https://github.com/neelkm/skills/actions/workflows/validate.yml). The expanded selection guidance does not add runtime qualification for competitor engines, gradients, or all features in current Newton documentation.

The 30 evaluation prompts are ready for use but have not been run as a paired with-skill/without-skill benchmark in Claude Code, Codex, or other agent hosts. No measured agent uplift or universal platform compatibility is claimed. The shared Agent Skills format and host installation documentation provide the portability basis.

## Reproduce

```console
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

On a supported Linux CPU host:

```console
python -m pip install "ovnewton==0.2.0" "newton==1.6.0" "warp-lang==1.17.0"
python -m pip check
python tests/runtime_smoke.py
```

See [the workflow](../.github/workflows/validate.yml), [public source provenance](SOURCES.md), and each skill's evaluation directory. Ovnewton uses `evals/cases.json`; ovphysx 0.2.0 uses `evals/evals.json`. Store real run evidence separately from synthetic examples.

## Ovphysx addition: 2026-10-14

Added `physical-ai-ovphysx-selection` version 0.1.0 under `skills/ovphysx/`. Its seven-file package contains the entrypoint, four supporting references, a metadata probe, and 23 evaluation-case definitions. The repository now contains four skills and 53 evaluation-case definitions.

The new skill passed the skill-creator validator. All four skills passed the repository validator, including metadata, local resource links, evaluation structure, and unique installable names. All 21 helper tests passed on Windows with bundled Python 3.12.14. The metadata probe ran and reported no installed ovphysx, ovstage, or Warp in that interpreter. It correctly reported runtime, GPU, and dependency-compatibility testing as false.

All repository Python source files and the new reference's Python code example passed syntax checks. The portable ZIP passed an integrity check and contained all seven intended files, excluding Python caches. The sandbox command runner stalled; completed checks ran outside that sandbox. The bundled interpreter lacked PyYAML, so the two YAML-based validators used the existing Python 3.13 environment instead.

The ovphysx CPU lifecycle example, GPU execution, rendering, robot controls, contacts, cloning, reset, and performance were not executed or benchmarked. The 23 new evaluation cases were checked as data; they were not run as live-agent evaluations. The existing ovnewton CI result does not qualify ovphysx. No simulation performance, agent improvement, or full ASD-STE100 compliance is claimed.

## ASD-STE100-style version

Original record: 2026-10-13. The ovphysx addition is dated 2026-10-14. Its submission-format replacement is dated 2026-10-16. This record lists completed checks and their limits. It does not certify the skills for NVIDIA's catalog. It is not a live-agent benchmark.

### Ovphysx submission-format replacement: 2026-10-16

The repository replaced `physical-ai-ovphysx-selection` 0.1.0 with `ovphysx-selection` 0.2.0. Its path is `skills/ovphysx/ovphysx-selection/`. The 12 source files match the prepared submission package. The old installable folder was removed. Installation links and probe tests use the new name. The [submission materials](../submissions/ovphysx/README.md) include proposed catalog registration. They include an inactive validation-workflow template, PR drafts, and report alternatives.

All four skills passed the repository validator. It checked 30 ovnewton cases and nine ovphysx CI cases. The original 23 ovphysx cases remain in the separate submission directory. Their converted NVIDIA-format dataset is also there. The repository validator accepts both dataset formats. It checks expected-script paths.

All 24 helper tests passed on Windows with Python 3.13. Three tests check dataset compatibility and rejection of invalid or ambiguous data. The renamed skill passed the skill-creator validator.

The preparation-time NVIDIA evaluator result remains incomplete. Eight of 11 results passed. Three security-related scanner results were unavailable. Its static quality heuristic was 89.5/100, grade B. These are not live-agent benchmark results. The submission record identifies the pinned evaluator and actual evidence. It lists the remaining owner/license, security, evaluation, and signing steps.

This replacement did not run ovphysx physics. It did not qualify a GPU. It did not submit to NVIDIA's catalog. The historical checks below retain their original scope and dates.

All three skill entrypoints passed the skill-creator metadata validator. The repository validator passed for all three skills. It checked portable metadata, resource links, and 30 evaluation-case definitions. Physics selection has 18 cases. Scene preparation and tuning each have six cases.

All 18 helper tests passed on Windows with Python 3.13.12. The first run could not access temporary directories inside the sandbox. The unchanged tests passed outside the sandbox.

All Python files compiled successfully. The environment probe ran without installed simulation packages. It correctly reported metadata-only evidence. It reported runtime testing as false. It also reported GPU testing as false.

The first skill is now `physical-ai-physics-selection` version 0.2.0. Its revised metadata and resource links passed validation. All 18 helper tests passed again after the directory rename. The helper implementation did not change. The added selection cases cover Newton preferences, alternatives, integration limits, gradients, hardware requirements, and unsupported comparative claims. Their structure was checked. Their agent behavior was not executed.

The local host does not have a supported Linux ovnewton environment. [GitHub Actions run 38440362196](https://github.com/neelkm/skills/actions/runs/38440362196) passed portable checks on Linux and Windows. The Linux CPU integration job also passed. The runtime used Python 3.12.15, ovnewton 0.2.0, Newton 1.6.0, and Warp 1.17.0. The resolved ovstage version was 0.2.1.385922. Dependency consistency checks also passed.

The CPU job inspected the original falling-box fixture. It checked body/shape counts, mass, and gravity. It passed eight-frame packaged examples with XPBD and VBD. Newton gave a VBD deprecation warning. The packaged example uses the legacy default `rigid_compliant_alm=False`. This default is planned to change. The result does not qualify the future default. The job did not test MuJoCo-Warp, CUDA execution, RTX rendering, long-horizon contact stability, or a trained policy.

The workflow repeats portable checks and CPU integration for later revisions. See the [run history](https://github.com/neelkm/skills/actions/workflows/validate.yml). The expanded selection guidance does not qualify competitor engines or gradients through runtime tests. It does not qualify all features in current Newton documentation.

The 30 evaluation prompts are ready to use. No paired with-skill/without-skill benchmark has run in Claude Code, Codex, or other agent hosts. No measured agent improvement is claimed. No universal platform compatibility is claimed. Portability is based on the shared Agent Skills format and the host installation documentation.

To repeat the local checks, run:

```console
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

On a supported Linux CPU host, run:

```console
python -m pip install "ovnewton==0.2.0" "newton==1.6.0" "warp-lang==1.17.0"
python -m pip check
python tests/runtime_smoke.py
```

See [the workflow](../.github/workflows/validate.yml), [public source provenance](SOURCES.md), and each skill's evaluation directory. Ovnewton uses `evals/cases.json`. Ovphysx 0.2.0 uses `evals/evals.json`. Keep real run evidence separate from synthetic examples.

### Ovphysx addition: 2026-10-14

The repository now includes `physical-ai-ovphysx-selection` version 0.1.0. Its location is `skills/ovphysx/`. Its package has seven files. These files contain the entrypoint, four supporting references, a metadata probe, and 23 evaluation-case definitions. The repository now has four skills. It has 53 evaluation-case definitions.

The new skill passed the skill-creator validator. All four skills passed the repository validator. This validator checked metadata and local resource links. It checked evaluation structure. It also checked that each installable skill has a unique name.

All 21 helper tests passed on Windows with bundled Python 3.12.14. The metadata probe ran in that interpreter. It found no installed ovphysx, ovstage, or Warp. It correctly reported runtime testing as false. It reported GPU testing as false. It also reported dependency-compatibility testing as false.

All repository Python source files passed syntax checks. The Python example in the new reference also passed its syntax check. The portable ZIP passed an integrity check. It contained all seven intended files. It excluded Python caches.

The sandbox command runner stalled. The completed checks ran outside that sandbox. The bundled interpreter did not have PyYAML. The two YAML-based validators therefore used the existing Python 3.13 environment.

The ovphysx CPU lifecycle example was not executed. GPU execution and rendering were not tested. Robot controls, contacts, cloning, and reset were not tested. Performance was not benchmarked. The 23 new evaluation cases were checked as data. They were not run as live-agent evaluations. The existing ovnewton CI result does not qualify ovphysx. No simulation performance or agent improvement is claimed. No full ASD-STE100 compliance is claimed.
