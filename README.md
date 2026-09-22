# 360° Output Auditor

Independently audit, verify, correct, and revalidate an existing AI-produced output or completed AI-performed task as a second-pass quality check. Use when the user explicitly asks to audit, verify/reverify, validate/revalidate, deep-check, 360-check, check what you just did, audit a diagnosis, verify server/tool work, or review a prior AI result for correctness. Covers factual/research answers, calculations, code, infrastructure, plans, recommendations, specifications, and tool-executed work. Scale depth to consequence, preserve correct content, find only evidence-supported defects, and return a corrected ready-to-use result. Do not trigger for first-pass creation, ordinary proofreading/rewriting, generic code review, or routine questions unless the user is asking to verify prior AI output/work.

## Install

Use this repository as the canonical source for the Skill. The Skill files are at repository root.

## Typical use

- `360 audit the last output.`
- `Verify what you just did.`
- `Audit the diagnosis.`
- `Audit the server/tool work and verify the actual end state.`

The Skill is designed as a second-pass, evidence-first audit layer: reconstruct the original contract, verify material claims at the appropriate evidence layer, correct only justified defects, check the resulting/end state where possible, regression-check corrections, and preserve explicit uncertainty when proof is unavailable.
