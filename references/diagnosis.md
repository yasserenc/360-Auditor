# Diagnosis and Root-Cause Audit

Use this reference for troubleshooting, incidents, outage diagnoses, causal explanations, and repeated failed fixes.

## Keep epistemic states separate

Track the relevant states without collapsing them:

- symptom;
- direct observation;
- hypothesis;
- supporting evidence;
- contradicting evidence;
- eliminated cause;
- likely/supported cause;
- confirmed causal mechanism;
- unresolved unknown.

A cause is **confirmed** only when evidence establishes the causal relationship strongly enough for the claimed scope. Plausibility, prevalence, correlation, or a fix appearing to help are insufficient by themselves.

## Prefer discriminating evidence

Where feasible:

1. reproduce or precisely characterize the failure;
2. identify the disputed boundary;
3. preserve the smallest meaningful failing trace: starting state → action → expected result → actual result → environment/boundary;
4. define competing hypotheses and what would falsify them;
5. use logs, metrics, traces, configuration inspection, known-good comparisons, or controlled tests to distinguish them;
6. change one primary causal variable at a time when practical;
7. compare before → intervention → after;
8. re-run the acceptance check at the boundary that actually failed.

A successful mitigation can be reported as successful while causal attribution remains **SUPPORTED** or **UNVERIFIED**.

## Convergence guard

Switch from ordinary fixing to diagnostic mode when repeated materially equivalent fixes fail without information gain, target-environment evidence contradicts the current diagnosis, or the next proposal depends on an already falsified/unverified assumption.

In diagnostic mode:

- stop speculative implementation/revision;
- preserve observed evidence and the last known-good behavior;
- do not retry a falsified hypothesis without new evidence that reopens it;
- prefer the next action that eliminates the most plausible explanations with the fewest new assumptions;
- create an evidence bridge if the decisive state is currently unobservable;
- if available evidence/tools cannot distinguish the remaining material hypotheses, state **“I cannot confirm this.”** and identify the narrowest observation/test/access required.

Do not treat iteration count itself as progress. Resume corrective changes only when new evidence materially changes a hypothesis or verifies a requirement.

## Root-cause report discipline

A strong diagnosis report distinguishes:

- what is observed;
- what is inferred;
- what has been ruled out;
- what is likely;
- what is causally confirmed;
- what remains unknown;
- what test would most increase information next.
