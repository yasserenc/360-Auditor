# Code and Script Audit

Use this reference for source code, scripts, APIs, automation logic, application behavior, and code patches.

## Reconstruct the contract first

Identify language/runtime/library versions, expected inputs/outputs, side effects, interfaces, permissions, data/state boundaries, and acceptance behavior. Review against the actual requirement, not personal style.

## Validate the relevant axes

Check, as applicable:

- syntax and type/schema validity;
- semantic and control-flow correctness;
- API/library usage against the actual version;
- input validation and error/exception behavior;
- state transitions and resource cleanup;
- authentication versus authorization;
- permissions, secrets, untrusted input, and external integrations;
- destructive/data-integrity behavior;
- idempotency, retries, duplicate execution, concurrency, races, and ordering;
- boundary values and realistic edge cases;
- interface/schema compatibility and consumer impact;
- dependency/prerequisite availability;
- operational behavior, logging/observability, and recovery;
- performance only when it matters to the contract or measured constraints.

A potential optimization is not a material defect without evidence that it matters to the objective/constraints. Measure/profile when performance is the claim under audit.

## Verify behavior, not appearance

If safe execution is available, prefer tests that exercise the disputed behavior. For a bug fix, when feasible:

1. reproduce the original defect with a falsifiable check;
2. confirm the check fails for the original behavior for the expected reason;
3. apply the minimum correction;
4. run the same check and confirm it passes;
5. run relevant regression coverage.

A passing test proves only the behavior/environment it covers. Do not generalize a unit test to production state or a mocked boundary to the real integration.

If execution is unavailable, label the result **Statically reviewed** and state what runtime behavior remains unverified. Never describe static inspection as a test run.

## False-positive discipline

Do not flag code merely because it is unconventional, less elegant, or different from a preferred pattern. A material finding needs a concrete contract violation, realistic failure path, security/reliability issue, compatibility problem, or evidence-backed improvement.

Use the smallest correction that fixes the demonstrated issue and preserve unrelated working code.
