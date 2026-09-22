# Changelog

All notable user-facing changes to 360° Output Auditor are documented here.

The project follows Semantic Versioning.

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
