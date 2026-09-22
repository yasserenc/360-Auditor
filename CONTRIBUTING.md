# Contributing

Contributions are welcome when they improve audit reliability without turning the Skill into a monolithic checklist.

## Design rules

1. Keep `SKILL.md` as the compact control plane.
2. Put domain-specific depth in directly linked files under `references/`.
3. Add a rule only when it changes behavior or prevents a demonstrated failure mode.
4. Preserve evidence calibration: claims must not be stronger than their proof.
5. Do not convert missing evidence, stylistic preference, or reviewer disagreement into a Confirmed Defect.
6. Preserve the distinction between command success, persisted state, runtime health, intended functionality, and desired end-state verification.
7. Preserve the distinction between a plausible diagnosis and a confirmed causal mechanism.
8. Do not broaden consequential-action authority merely because an audit was requested.
9. Prefer the minimum complete correction and regression-check the result.
10. Avoid adding scripts or dependencies unless they materially improve deterministic reliability.

## Change process

For a substantive change:

1. define the failure mode or behavior being improved;
2. identify whether it belongs in the core or a conditional reference;
3. make the smallest complete change;
4. validate the Skill structure;
5. test representative positive, negative-trigger, false-positive, missing-access, and regression cases;
6. compare behavior against the previous version;
7. update `CHANGELOG.md`;
8. release with an appropriate semantic version.

## Licensing and attribution

Do not remove or weaken third-party attribution in
`THIRD_PARTY_NOTICES.md` or the methodology note in
`references/skill-evaluation-security.md`.
