# Plans, Procedures, and Workflows Audit

Use this reference for implementation plans, runbooks, procedures, migration sequences, project workflows, checklists, and operational instructions.

## Validate the executable path to the objective

1. Start from the end state and verify that completing every planned step would actually produce it.
2. Check prerequisites, dependencies, ordering, ownership/authority, inputs, environment assumptions, and required access.
3. Simulate dependency order far enough to expose circular, impossible, or hidden prerequisites.
4. Verify material commands, tools, APIs, resource names, and version-specific actions against the real environment/documentation when uncertainty could make the plan fail.
5. Identify blockers or missing decision points before irreversible/expensive steps.
6. Check failure paths: partial completion, retry, rollback, recovery, resume, and idempotency where relevant.
7. Place validation gates where a wrong intermediate state would otherwise propagate.
8. Make critical acceptance checks observable and falsifiable: define what result would show the step or plan is wrong, not merely what activity should occur.
9. Remove redundant orchestration and add only steps needed for correctness, safety, validation, or recovery.

## Common plan defects

Look for:

- technically plausible steps in impossible dependency order;
- nonexistent/outdated command, tool, API, or option;
- hidden prerequisite discovered only after execution starts;
- destructive action before backup/validation;
- no rollback for a risky migration;
- “deploy succeeded” used as the only acceptance criterion;
- missing persistence/restart behavior;
- verification commands that cannot falsify the claimed success;
- a plan optimizing activity rather than user outcome;
- needless orchestration that increases failure surface without value.

Prefer the smallest plan that safely and verifiably reaches the objective.
