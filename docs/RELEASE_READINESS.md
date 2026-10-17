# Release readiness and acceptance boundaries — v2.0.0 candidate

**Not released.** This is a controlled candidate branch. No CI result, source scan, or artificial fixture is a behavioral effectiveness benchmark.

## Required order and evidence

| Plan | Evidence required | Actual status as of 2026-10-17 |
|---|---|---|
| P01 | Main and v1.0.1 immutable IDs, manifest, release digests | Recorded in [BASELINE.md](BASELINE.md); historic download bytes not independently verified |
| P02 | Preregister E01–E22 and variants | [Versioned synthetic oracles, revision 3](../tests/eval/cases.json) and [pre-replay change log](../tests/eval/ORACLE_REVIEW.md); historical real cases unavailable |
| P03 | Safe workflow handling and least-privileged test stage | Tag-triggered workflow, no direct untrusted input interpolation; isolated regression |
| P04 | Exact tag/ref source and non-overwrite | CI guard and publish refusal; repository-wide immutable release setting not established |
| P05 | YAML/metadata and ZIP-link closure | Local/CI validator checks and official available Skill Creator quick validator; host schema acceptance separate |
| P06 | Two changed-mtime builds, identical bytes | E19 CI test, checksum + ZIP re-extraction |
| P07–P09 | Coherent four-way verdict, authority, facets | Instructions and examples edited; behavioral compliance not inferred from text |
| P10 | ChatGPT upload, explicit, implicit and negative host tests | **PARTIAL:** user reports successful upload and supplied one real audit output; this session can load installed candidate instructions and all 11 matching references. Exact installed ZIP provenance, full trigger coverage and negative-trigger checks remain unverified |
| P11 | Deterministic PR CI, unsafe fixtures fail | CI passes current candidate; new commits need their own CI run |
| P12 | Same-case v1.0.1 versus candidate E01–E18 traces | [Exact P10/P12 host replay runbook](../tests/eval/HOST_REPLAY_RUNBOOK.md) prepared. **BLOCKED: matched real-host traces and independent adjudication not yet supplied; do not score** |
| P13 | All above, matching artifact SHA, protections, downloaded published bytes | **BLOCKED: NO tag/release** |
| P14 | Actual post-release observation intake | Observation template prepared; not completed until valid release |

## Candidate host observation, 2026-10-17 (NOT a scored replay)

The user reports successful installation and supplied an actual ChatGPT audit report. That report identified a duplicate-ID issue in the *standalone gold-corpus* acceptance check. We reproduced that precise issue through two red regression tests and fixed it; a third test confirms the 19-recorded-results path was already rejected. The user's report is **one observational pilot**, not 18 matched benchmark traces and not proof of E01–E18 performance.

Using the Skill interface exposed to this conversation, the installed entrypoint **body (after frontmatter stripping)** and all **11 references** exactly match GitHub candidate commit `412541b6dc10dc740aa70d26afa5e7cf5da12855`. The installed `agents/openai.yaml` differs only in default-prompt wrapping and `assets/icon.svg` is **not** the same artwork as the candidate source icon. Thus no claim of exact 14-file installed-byte identity or exact original ZIP provenance is warranted. A host may transform metadata/assets, or the installed Skill may have been modified; that cause was not established.

The user-provided report correctly ends **INCONCLUSIVE for complete behavioral reliability**. Keep P10 explicit/implicit/negative tests and P12 baseline-versus-candidate matched replay **pending**, and never backfill `host_results.json` from the report alone.

**Acceptance checker correction:** Before dictionary conversion it now requires exactly one of each preregistered E01–E22 and V01–V04 gold-case ID; the pre-fix test failed on duplicates and subsequent regression tests passed. This correction affects test/release infrastructure **only**, not the Skill ZIP.

## Exact remaining host acceptance

1. Download the **candidate** ZIP and checksum from a successful CI workflow artifact for the latest candidate commit; verify checksum. Do not replace the user's installed v1.0.1.
2. In a **separate, explicit ChatGPT Web test environment**, import/create the candidate as a separate Skill (do not overwrite the user's working v1.0.1); record whether ChatGPT accepts the exact ZIP, its declared metadata and 14 members.
3. Follow the [isolated host replay runbook](../tests/eval/HOST_REPLAY_RUNBOOK.md) for the frozen revision-3 [E01–E18 controls](../tests/eval/cases.json) on independent **v1.0.1** and **candidate** host sessions with matched request, evidence, tools and model. Include explicit, implicit-positive and negative E16 trigger tests. Do not report a baseline/candidate trial unless actual invocation and the exact installed version are known.
4. Record the raw outputs and any tool traces under tests/eval/traces; match case, host, model, date, reviewer, verdict, evidence boundaries and actual action. Adjudicate against preregistered gold, not explanation fluency. Document failures even when fixed.
5. Create tests/eval/host_results.json **only** using genuine observed and sanitized records (no credentials, personal data, or invented PASS flags). Include baseline_tag=v1.0.1, candidate_skill_sha256=the exact archive digest, ChatGPT host flags true only when independently observed, and acceptance evidence_paths. Each of the 18 records must include baseline_status, candidate_status, candidate_observed_verdict, candidate_invoked, baseline_invoked, candidate_observables_verified, candidate_forbidden_seen, candidate_authority_violation_seen, baseline_trace_path, candidate_trace_path, baseline_trace_sha256, candidate_trace_sha256, adjudicated_at, reviewer and host_model. Explicitly mark E16 candidate_invoked=false; its gold verdict is NOT INVOKED. The validation script compares recorded verdicts and invocation fields to frozen gold, but **cannot authenticate the original host transcripts or the reviewer**; a separate independent review remains mandatory. Missing results fail closed.
6. Rebuild from the final candidate runtime bytes and repeat key host safety cases if the runtime changes. Review source and trace authenticity independently before merging/tagging.

## P10 — minimum unavoidable ChatGPT host action

OpenAI's current [Skills in ChatGPT help](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) documents: **Plugins (sidebar) -> Skills (Plugin Directory) -> Create -> Upload from your computer**. Actual skill upload is a ChatGPT user/workspace action; the repository GitHub connector cannot install or invoke an independent Skill.

Use the exact `skill.zip` generated by this branch's successful CI. **Use a separate isolated test workspace/account or genuinely separate test Skill install**, preserving the active v1.0.1. Do not change `SKILL.md` to avoid name collisions: a renamed package would have a different checksum and would not establish acceptance of the exact release candidate. If ChatGPT reports a duplicate-name conflict or denies upload permission, preserve that error as evidence and stop without replacing the active version.

Record the host product, timestamp, model (when visible), original ZIP SHA-256, upload accept/reject result, and precise installed Skill identity. Then check explicit invocation, implicit-positive invocation and negative E16 non-invocation in the real host. A screenshot of an upload dialog alone is not evidence of actual Skill triggering. The full E01–E18 cases still require comparable baseline/candidate invocations, recorded raw outputs, and independent adjudication. Never invent or backfill trial outcomes.

## Repository setting that is not changed by workflow code

GitHub's [immutable releases](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/prevent-release-changes) must be **enabled by a repository administrator** in repository Settings -> Releases -> Enable release immutability, and the state verified for new releases. It is distinct from merely refusing to clobber within one workflow. Protect main and release tags via appropriate rulesets after reviewing the contributor model; current main reported unprotected and rulesets empty. Do not claim immutability or require admin settings to have changed until verified.

## Controlled release

After accepting P10/P12 evidence and protecting new releases: review PR and CI, merge approved candidate into main, verify SHA and source tag identity, create a **new** v2.0.0 tag on the reviewed commit. The tag-triggered workflow reruns CI and blocks publishing unless recorded host results match the **exact runtime ZIP digest**. Published SHA256SUMS and publicly downloaded skill.zip must match. Never rewrite or refresh v1.0.0/v1.0.1.

Rollback: retain [v1.0.1](https://github.com/yasserenc/360-Auditor/releases/tag/v1.0.1) source and existing asset digests; a later user's explicit installed-Skill rollback is separate from GitHub release management.

## Non-claims

Do not present an unperformed host replay as a passing E01–E18 test. Do not infer precision, recall or improved performance from 400+ user-reported uses. Source control, local CLI validation and CI are narrow facets; cross-host portability is untested.
