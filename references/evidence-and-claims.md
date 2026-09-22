# Evidence and Claim Calibration

Use this reference when the audit is complex/high-risk, claims are disputed, evidence comes from multiple layers, the target is mutable, or the conclusion could exceed what the evidence proves.

## Build proof obligations, not a paperwork ritual

For each material claim, determine the narrowest evidence that would actually establish it. When useful, keep a compact internal ledger:

| Claim | Claim type | Required proof | Evidence obtained | Provenance / target identity | Scope | Freshness | Status |
|---|---|---|---|---|---|---|---|

Use statuses: **CONFIRMED**, **SUPPORTED**, **UNVERIFIED**, **CONTRADICTED**, **NOT APPLICABLE**.

- **CONFIRMED**: direct, appropriate evidence establishes the claim at the stated scope.
- **SUPPORTED**: evidence materially favors the claim but does not establish the full scope or causal strength.
- **UNVERIFIED**: material proof is unavailable, stale, indirect, or missing.
- **CONTRADICTED**: appropriate evidence conflicts with the claim.
- **NOT APPLICABLE**: claim is outside the reconstructed contract.

Do not expose this table for trivial audits unless the user asks.

## Match proof scope to claim scope

Reject these substitutions:

- unit test → production behavior;
- documentation → actual runtime state;
- command exit code/API 2xx → desired end state;
- correlation → root cause;
- old snapshot → current mutable state;
- one observed case → universal behavior;
- AI/reviewer summary → independent evidence;
- absence of visible error → proof of success;
- unsupported source count → source quality.

A lower-fidelity observation can support a narrower claim. Narrow the wording rather than overstating proof.

## Track provenance and identity

For mutable or tool-executed targets, bind evidence to the state it actually observed: relevant host/resource/file/candidate identity, configuration version/hash/revision where available, environment, and time. If the target may have changed since the observation, do not present stale evidence as current verification.

Distinguish:

- **Specification evidence** — what should/supported behavior be.
- **Target-state evidence** — what the actual system/artifact currently is or does.
- **Independent field evidence** — observed behavior outside the implementation's own success signal.
- **Inference** — reasoned conclusion that remains weaker than direct proof.

## Calibrate language

Match wording to evidence strength and scope:

- Do not present a hypothesis as a root cause.
- Do not present an estimate/projection as a guaranteed outcome.
- Do not generalize an anecdote or small sample into a universal fact.
- Do not confuse vendor specification with a deployed implementation.
- Do not interpret absence of evidence as evidence of absence unless the observation method had enough sensitivity/scope to justify that inference.
- Do not add hedging when direct evidence is strong; precision is the goal, not caution theater.

## Resolve conflicts

When evidence conflicts, investigate likely boundary differences first: time, version, environment, population, cache/state, source authority, measurement method, or target identity. If the conflict remains material, preserve it as uncertainty instead of selecting the convenient source.

## Independent review as an optional check

For complex/high-risk artifacts, an independent fresh-context or different-model review can expose blind spots when such capability actually exists. Give the reviewer the artifact + contract, not the original author's conclusion. Treat reviewer findings as leads to reconcile against evidence, never as proof by themselves. Do not invoke external models/tools without the authorization required by the environment.

## Evidence hierarchy for subjective outputs

Prefer, in order:

1. deterministic/direct evidence when the acceptance criterion is objectively checkable;
2. a calibrated rubric/judge when the criterion is genuinely semantic/subjective;
3. unsupported subjective impression only when no stronger method exists, clearly labeled.

Do not use a proxy metric merely because it is easy to count. The verifier must test the actual acceptance criterion.
