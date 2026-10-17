# Release readiness and acceptance boundaries — v2.0.0 candidate

**Not released.** This is a controlled candidate branch. No CI result, source scan, or artificial fixture is a behavioral effectiveness benchmark.

## Required order and evidence

| Plan | Evidence required | Actual status as of 2026-10-17 |
|---|---|---|
| P01 | Main and v1.0.1 immutable IDs, manifest, release digests | Recorded in [BASELINE.md](BASELINE.md); historic download bytes not independently verified |
| P02 | Preregister E01–E22 and variants | [Frozen synthetic oracles](../tests/eval/cases.json); historical real cases unavailable |
| P03 | Safe workflow handling and least-privileged test stage | Tag-triggered workflow, no direct untrusted input interpolation; isolated regression |
| P04 | Exact tag/ref source and non-overwrite | CI guard and publish refusal; repository-wide immutable release setting not established |
| P05 | YAML/metadata and ZIP-link closure | Local/CI validator checks and official available Skill Creator quick validator; host schema acceptance separate |
| P06 | Two changed-mtime builds, identical bytes | E19 CI test, checksum + ZIP re-extraction |
| P07–P09 | Coherent four-way verdict, authority, facets | Instructions and examples edited; behavioral compliance not inferred from text |
| P10 | ChatGPT upload, explicit, implicit and negative host tests | **BLOCKED: requires actual ChatGPT host session and installation/preview action** |
| P11 | Deterministic PR CI, unsafe fixtures fail | CI passes current candidate; new commits need their own CI run |
| P12 | Same-case v1.0.1 versus candidate E01–E18 traces | **BLOCKED: host replay unavailable; do not score** |
| P13 | All above, matching artifact SHA, protections, downloaded published bytes | **BLOCKED: NO tag/release** |
| P14 | Actual post-release observation intake | Observation template prepared; not completed until valid release |

## Exact remaining host acceptance

1. Download the **candidate** ZIP and checksum from a successful CI workflow artifact for the latest candidate commit; verify checksum. Do not replace the user's installed v1.0.1.
2. In a **separate, explicit ChatGPT Web test environment**, import/create the candidate as a separate Skill (do not overwrite the user's working v1.0.1); record whether ChatGPT accepts the exact ZIP, its declared metadata and 14 members.
3. Replay the frozen [E01–E18 controls](../tests/eval/cases.json) on independent **v1.0.1** and **candidate** host sessions with matched request, evidence, tools and model. Include explicit, implicit-positive and negative E16 trigger tests. Do not report a baseline/candidate trial unless actual invocation and the exact installed version are known.
4. Record the raw outputs and any tool traces under tests/eval/traces; match case, host, model, date, reviewer, verdict, evidence boundaries and actual action. Adjudicate against preregistered gold, not explanation fluency. Document failures even when fixed.
5. Create tests/eval/host_results.json only using observed records, with baseline_tag=v1.0.1, candidate_skill_sha256=the exact archive digest, chatgpt_host flags true only when observed, acceptance evidence_paths and 18 case entries (baseline_status, candidate_status, baseline_trace_path, candidate_trace_path, reviewer, host_model). The gate intentionally fails when this file is absent.
6. Rebuild from the final candidate runtime bytes and repeat key host safety cases if the runtime changes. Review source and trace authenticity independently before merging/tagging.

## Repository setting that is not changed by workflow code

GitHub's [immutable releases](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/prevent-release-changes) must be **enabled by a repository administrator** in repository Settings -> Releases -> Enable release immutability, and the state verified for new releases. It is distinct from merely refusing to clobber within one workflow. Protect main and release tags via appropriate rulesets after reviewing the contributor model; current main reported unprotected and rulesets empty. Do not claim immutability or require admin settings to have changed until verified.

## Controlled release

After accepting P10/P12 evidence and protecting new releases: review PR and CI, merge approved candidate into main, verify SHA and source tag identity, create a **new** v2.0.0 tag on the reviewed commit. The tag-triggered workflow reruns CI and blocks publishing unless recorded host results match the **exact runtime ZIP digest**. Published SHA256SUMS and publicly downloaded skill.zip must match. Never rewrite or refresh v1.0.0/v1.0.1.

Rollback: retain [v1.0.1](https://github.com/yasserenc/360-Auditor/releases/tag/v1.0.1) source and existing asset digests; a later user's explicit installed-Skill rollback is separate from GitHub release management.

## Non-claims

Do not present an unperformed host replay as a passing E01–E18 test. Do not infer precision, recall or improved performance from 400+ user-reported uses. Source control, local CLI validation and CI are narrow facets; cross-host portability is untested.
