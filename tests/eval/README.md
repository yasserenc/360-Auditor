# Behavioral acceptance protocol (P02/P12)

[Gold corpus](cases.json) was originally preregistered before candidate runtime changes; four ambiguous cases were corrected after those source edits but **before any actual matched host replay**, with the prior version retained in Git history and changes explained in [ORACLE_REVIEW.md](ORACLE_REVIEW.md). All E01–E22 and V01–V04 are synthetic controls. There is **no** verified real historical ground truth in this corpus, and user-reported 400+ uses must not be scored as trials.

## Replay method

1. Preserve the exact model/host, prompt, temperature where exposed, previous substantive context, source files, and available tools for **both** [v1.0.1](https://github.com/yasserenc/360-Auditor/releases/tag/v1.0.1) and the current candidate. Run in separate isolated ChatGPT Web sessions with explicitly identified installed revisions; do not treat text snippets pasted to a session as true Skill installation.
2. Run explicit E01–E15, E17–E18, implicit-negative E16 and positive implicit replays separately; record raw response, tool traces (if available), observed invocation and postconditions. Adjudicate every `gold.required_observables` and `gold.forbidden` against independent scenario evidence; record failures and any justified ambiguity before scoring.
3. Run deterministic E19–E22 with local/CI tests. Distinguish their PASS from **black-box host** behavioral PASS. For unsafe fixtures, use inert stubs and no live production access.
4. Compare matched v1.0.1 versus candidate verdict, evidence boundaries, mutation attempts, result integrity, trigger, cost and time **only where observed**. No precision, recall, or percentage without justified denominator and sampling protocol.
5. Record actual case-by-case trace with `case_id`, `skill_tag`, `host`, `model`, `invoked`, `verdict`, `observed_outputs`, `tool_trace`, `adjudication`, `date`, and `reviewer`. Do not pre-populate PASS outcomes.

**At P02 setup:** Actual v1.0.1/candidate host replay has not occurred, because this session has no tool to install/invoke a candidate skill in ChatGPT Web or query implicit-trigger decisions. The gate remains **NOT TESTED**. Independently verified historical cases were not supplied or retrievable. P12 cannot be marked passed by deterministic source assertions alone.
