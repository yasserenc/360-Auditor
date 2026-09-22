# 360° Output Auditor

**360° Output Auditor** is a reusable ChatGPT Skill for independently auditing, verifying, correcting, and revalidating an existing AI-produced output or completed AI-performed task.

It is designed as a **second-pass quality gate**: reconstruct the original contract, verify material claims against the strongest available evidence, distinguish intermediate success from the actual desired end state, correct only justified defects, regression-check the result, and preserve uncertainty when proof is unavailable.

## What it is for

Use the Skill after substantive AI work when correctness matters, including:

- factual and research answers;
- calculations and quantitative analysis;
- code, scripts, APIs, and application logic;
- infrastructure, servers, networking, DNS, and cloud configuration;
- troubleshooting and root-cause analysis;
- work already performed through SSH, MCP, shell, browser, APIs, databases, deployments, or cloud consoles;
- plans, procedures, migrations, and implementation workflows;
- recommendations and comparisons;
- specifications, documentation, UI/UX, and design outputs;
- high-stakes or consequential material where stronger evidence discipline is needed;
- AI Skills, verifier designs, evaluator harnesses, and agent workflows.

It is **not** intended to run as a heavy audit for every trivial answer, ordinary rewrite, proofreading request, or first-pass creation task.

## Typical prompts

Minimal prompts are intentional:

```text
360 audit the last output.
```

```text
Verify what you just did.
```

```text
Audit the diagnosis.
```

```text
Audit the server/tool work and verify the actual end state.
```

```text
Audit this before I run it.
```

For tool-executed work, a useful fuller prompt is:

```text
360 audit the work you just performed. Verify the actual target state independently using read-only checks, check functionality, persistence, side effects and regressions where relevant, and do not make further consequential changes without separate authorization.
```

## Core behavior

The Skill follows a compact control-plane workflow:

1. resolve the exact audit target;
2. reconstruct the original objective, requirements, constraints, environment, and acceptance criteria;
3. scale verification depth to consequence and uncertainty;
4. define what evidence would actually prove each material claim;
5. load only the domain guidance relevant to the target;
6. audit and verify;
7. classify findings as:
   - **Confirmed Defect**
   - **Verification-Dependent Risk**
   - **Optional Improvement**
8. make the minimum complete correction;
9. reverify the corrected result and check regressions;
10. stop when further iteration would add no meaningful evidence.

For unverifiable material claims, the Skill uses the explicit wording:

> **I cannot confirm this.**

and identifies the evidence, access, or test needed to resolve the uncertainty.

## Verification levels

The Skill distinguishes the strongest verification level actually achieved:

- **Statically reviewed**
- **Source verified**
- **Recomputed**
- **Executed/tested**
- **Environment verified**
- **End-state verified**

This prevents a static review, successful command, test result, or deployment message from being presented as proof of a broader state than it actually establishes.

## Verdicts

The audit verdict applies to the **original target as received**, before corrections:

- **PASS — no material correction required**
- **PASS WITH CORRECTIONS — fundamentally sound, but justified corrections were required**
- **FAIL — material defects made the original target unreliable or unsuitable without substantial correction**

Optional improvements alone do not downgrade a PASS.

## Installation / reuse

### Download the stable package

- [Latest GitHub release](https://github.com/yasserenc/360-Auditor/releases/latest)
- [Download latest `skill.zip`](https://github.com/yasserenc/360-Auditor/releases/latest/download/skill.zip)
- [Download SHA-256 checksum](https://github.com/yasserenc/360-Auditor/releases/latest/download/SHA256SUMS.txt)

The canonical Skill source is stored at repository root.

Required Skill files:

```text
SKILL.md
agents/openai.yaml
assets/icon.svg
references/
```

### ChatGPT Skill Creator

The known-compatible installation path is to create/edit the Skill in ChatGPT Skill Creator and preserve the repository paths exactly:

1. create the Skill as `output-auditor`;
2. copy `SKILL.md`;
3. copy `agents/openai.yaml`;
4. copy `assets/icon.svg`;
5. copy every file under `references/`;
6. save and enable the Skill.

Do not omit the `references/` files: the core Skill routes to them progressively depending on the audit domain.

### Packaging

If your Skill authoring environment provides the official Skill validator/packager, validate the Skill source and create the installable `skill.zip` from the Skill files.

Repository documentation files such as `README.md`, `LICENSE`, `CHANGELOG.md`, and `CONTRIBUTING.md` are project documentation and are not part of the runtime Skill bundle.

## Repository structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── icon.svg
├── references/
│   ├── code.md
│   ├── diagnosis.md
│   ├── evidence-and-claims.md
│   ├── factual-research.md
│   ├── high-stakes.md
│   ├── infrastructure.md
│   ├── plans-workflows.md
│   ├── quantitative.md
│   ├── recommendations-writing-design.md
│   ├── skill-evaluation-security.md
│   └── tool-executed-work.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── THIRD_PARTY_NOTICES.md
```

## Design principles

- evidence strength must match claim strength;
- current/mutable state requires current state evidence;
- command success is not the same as desired outcome success;
- a successful fix does not automatically prove the original root-cause diagnosis;
- missing evidence is not automatically a defect;
- correct content is preserved rather than rewritten for appearance;
- corrections are minimal and traceable to evidence or explicit requirements;
- consequential remediation is not authorized merely because an audit was requested;
- progressive loading keeps the core instruction set lean.

## Important limitation

Successful Skill installation does not by itself prove implicit-trigger precision or end-to-end behavior on every future model/runtime configuration. Runtime behavior should be periodically exercised with representative positive, negative-trigger, missing-access, and high-risk cases.

## Versioning

The repository follows semantic versioning for public releases.

See [CHANGELOG.md](CHANGELOG.md) for user-facing changes.

## License

Original project content is licensed under the **MIT License**. See [LICENSE](LICENSE).

A portion of the methodology in `references/skill-evaluation-security.md` is adapted from **Task Observer / One Skill to Rule Them All** by Eoghan Henn / rebelytics.com under **CC BY 4.0**. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for attribution and license details.
