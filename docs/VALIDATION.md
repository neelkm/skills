# Validation record

Date: 2026-10-13. This record describes completed checks and the limits of the evidence. It is not a NVIDIA catalog certification or a live-agent benchmark.

## Completed locally

- All three skill entrypoints passed the skill-creator metadata validator.
- The repository validator passed for all three skills. It checked portable metadata, resource links, and 18 evaluation-case definitions.
- All 18 helper tests passed on Windows with Python 3.13.12. The initial sandbox prevented access to temporary directories; the unchanged tests passed outside that sandbox.
- All Python files compiled successfully.
- The environment probe ran with no simulation packages installed and correctly reported metadata-only evidence, with runtime and GPU testing both false.

## Runtime and agent scope

The local host does not provide a supported Linux ovnewton environment. [GitHub Actions run 38440362196](https://github.com/neelkm/skills/actions/runs/38440362196) passed portable checks on Linux and Windows, plus the Linux CPU integration job. The runtime used Python 3.12.15, ovnewton 0.2.0, Newton 1.6.0, Warp 1.17.0, and resolved ovstage 0.2.1.385922. Dependency consistency checks also passed.

The CPU job inspected the original falling-box fixture, checked body/shape counts, mass, and gravity, and passed eight-frame packaged examples with XPBD and VBD. Newton emitted a VBD deprecation warning: the packaged example uses the legacy default `rigid_compliant_alm=False`, which is planned to change. This result does not qualify the future default. The job did not test MuJoCo-Warp, CUDA execution, RTX rendering, long-horizon contact stability, or a trained policy.

The 18 evaluation prompts are ready for use but have not been run as a paired with-skill/without-skill benchmark in Claude Code, Codex, or other agent hosts. No measured agent uplift or universal platform compatibility is claimed. The shared Agent Skills format and host installation documentation provide the portability basis.

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

See [the workflow](../.github/workflows/validate.yml), [public source provenance](SOURCES.md), and each skill's `evals/cases.json`. Store real run evidence separately from synthetic examples.

## ASD-STE100-style version

Date: 2026-10-13. This record lists completed checks and their limits. It does not certify the skills for NVIDIA's catalog. It is not a live-agent benchmark.

All three skill entrypoints passed the skill-creator metadata validator. The repository validator passed for all three skills. It checked portable metadata, resource links, and 18 evaluation-case definitions.

All 18 helper tests passed on Windows with Python 3.13.12. The first run could not access temporary directories inside the sandbox. The unchanged tests passed outside the sandbox.

All Python files compiled successfully. The environment probe ran without installed simulation packages. It correctly reported metadata-only evidence. It reported runtime testing as false. It also reported GPU testing as false.

The local host does not have a supported Linux ovnewton environment. [GitHub Actions run 38440362196](https://github.com/neelkm/skills/actions/runs/38440362196) passed portable checks on Linux and Windows. The Linux CPU integration job also passed. The runtime used Python 3.12.15, ovnewton 0.2.0, Newton 1.6.0, and Warp 1.17.0. The resolved ovstage version was 0.2.1.385922. Dependency consistency checks also passed.

The CPU job inspected the original falling-box fixture. It checked body/shape counts, mass, and gravity. It passed eight-frame packaged examples with XPBD and VBD. Newton gave a VBD deprecation warning. The packaged example uses the legacy default `rigid_compliant_alm=False`. This default is planned to change. The result does not qualify the future default. The job did not test MuJoCo-Warp, CUDA execution, RTX rendering, long-horizon contact stability, or a trained policy.

The 18 evaluation prompts are ready to use. No paired with-skill/without-skill benchmark has run in Claude Code, Codex, or other agent hosts. No measured agent improvement is claimed. No universal platform compatibility is claimed. Portability is based on the shared Agent Skills format and the host installation documentation.

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

See [the workflow](../.github/workflows/validate.yml), [public source provenance](SOURCES.md), and each skill's `evals/cases.json`. Keep real run evidence separate from synthetic examples.
