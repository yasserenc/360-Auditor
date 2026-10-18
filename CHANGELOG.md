# Changelog

## [Unreleased] — v2.0.0 candidate (2026-10-17)

This entry describes changes staged on the candidate branch, not a published version. Behavioral effectiveness and ChatGPT host acceptance remain unverified.

### Corrected

- Defined a fourth original-target verdict, **INCONCLUSIVE**, when decisive evidence is missing without a confirmed defect already settling the judgment.
- Separated the target verdict from remediation state and read-only audit completion, so unresolved authorized/pending fixes do not cause impossible stopping conditions.
- Replaced an implied single verification ladder with independent claim-scoped verification facets and reconciled instructions/examples.
- Replaced unsafe workflow-dispatch shell interpolation and overwrite-by-version release behavior with tag-bound, least-privileged, refusal-only publishing.
- Added YAML/frontmatter parsing, reference/asset closure, archive extraction checks, path/symlink safety, and deterministic ZIP bytes/checksums.

### Added

- Frozen E01–E22 synthetic gold corpus plus four edge fixtures. Synthetic tests do **not** constitute real host benchmark outcomes.
- Automated read-only CI with isolated E19–E22, malformed metadata, wrong-ref, symlink, and ZIP tests.
- A fail-closed release gate requiring actual ChatGPT host acceptance and matched E01–E18 trace records before tag publication.
- Reproducible candidate artifact in GitHub Actions for independently controlled host replay.
- Release readiness and observational feedback instructions.

### Breaking interface

The v1.x 3-valued verdict becomes a 4-valued verdict: PASS, PASS WITH CORRECTIONS, FAIL, or INCONCLUSIVE. Downstream parsers must accept the new outcome and treat remediation status as an independent field. The v1.0.1 release remains the rollback baseline.

### Unverified / blocked

- Actual installed candidate ChatGPT Web package acceptance and explicit/implicit/negative triggers;
- Matched baseline/candidate E01–E18 execution and ground-truth evaluation;
- GitHub repository-wide release immutability/branch ruleset configuration; and
- Final public release, which must not occur without the above mandatory gates.


All notable user-facing changes to 360° Output Auditor are documented here.

The project follows Semantic Versioning.

## [1.0.1] - 2026-09-22

### Fixed

- Switched the repository license file to canonical MIT text so GitHub detects the SPDX license correctly.
- Fixed release-note rendering so filenames and SHA-256 values are preserved.
- Fixed release publishing so an existing release refreshes `skill.zip` and `SHA256SUMS.txt` together, preventing checksum/asset drift.
- Added stable latest-release and direct package/checksum links to the README.

### Changed

- Release automation now supports repeatable packaging for semantic-version tags and manual release dispatches.
- No runtime 360° Output Auditor logic changed in this release.

## [1.0.0] - 2026-09-22

### Added

- Evidence-first second-pass audit workflow for existing AI outputs and completed AI-performed work.
- Risk-adaptive verification depth.
- Explicit claim-to-evidence calibration for complex, mutable, disputed, and high-risk targets.
- Separate verification guidance for factual research, code, infrastructure, diagnosis, calculations, plans, recommendations/design, high-stakes work, AI Skill evaluation, and tool-executed work.
- Distinction between command/tool completion and verified desired end state.
- Root-cause discipline that separates symptoms, hypotheses, supporting evidence, and confirmed causal mechanisms.
- Defined finding classes: Confirmed Defect, Verification-Dependent Risk, and Optional Improvement.
- Explicit verification-level labels from static review through end-state verification.
- Minimal-correction and regression-check requirements.
- Consequential-action authority boundaries.
- Skill Creator-compatible UI metadata and icon.

### Fixed

- Restored the complete Skill trigger description after an earlier manually assembled copy truncated the description.
- Preserved the Skill Creator-generated runtime metadata that is accepted by the actual ChatGPT environment.
