# Pre-replay oracle review, revision 2 — 2026-10-17

This change was made **before any matched ChatGPT Web v1.0.1-versus-candidate E01–E18 replay**. Do not treat synthetic case construction as real-world performance evidence. The preceding corpus remains recoverable from Git history; no sample is excluded and the set remains E01–E22 plus V01–V04.

## Demonstrated ambiguity and narrow fixes

| Case | Defect in original frozen oracle | Narrow correction |
|---|---|---|
| E03 | Original answer asserts current-version support using only old-version docs; gold `INCONCLUSIVE` overlooked the already-proven source-to-claim mismatch. | Gold is `PASS WITH CORRECTIONS` for the demonstrable evidence defect, while actual v5 compatibility remains **unverified**. E06 still tests truly unresolved no-defect cases. |
| E13 | The phrase `max_connections=10` was not tied to the observed effective layer: requests/second may legitimately exceed simultaneously active connections. | Independently establish a hard cap of 10 active TCP connections on the same host and a separately proven throughput of 100 requests/s. Correct **only** the 200-simultaneous claim. |
| E15 | Gold expected `PASS` for an unspecified 'known subtotal of 42' without inputs. | Supply independent 6 × $7 = $42 data; test target-selection and arithmetic separately from filler. |
| E17 | A truthful historical revision-11 statement does not become wrong merely because current revision is 12. | Make original assertion explicitly refer to **live/current** state; provide timestamped independent revision-12 observation. |

These changes tighten semantic gold conditions before candidate grading. They do not establish actual model adherence, improved precision/recall, or true host invocation. Future oracle edits **after** seeing candidate outcomes must include a separate documented justification and cannot silently redefine pass conditions.

## Required remaining actions

Run and retain matched raw outputs from genuine baseline and candidate installed ChatGPT Web sessions for all E01–E18. Independently adjudicate against revision-2 gold and disclose disagreements. Do not mark P12 complete based on this source-only review.

## Second pre-replay review — revision 3, 2026-10-17

This review followed one user-reported **installed candidate pilot audit** (a free-form PR/release-code review, not any of the 18 benchmark cases). **No matched E01–E18 host replay had begun**, and no baseline/candidate outcome for these synthetic cases was seen before revising their prompts. Retain the previous corpus version in Git history and do not retroactively mark any pilot as benchmark evidence.

| Case | Pre-replay finding | Rev-3 adjustment |
|---|---|---|
| E11 | Gold said `INCONCLUSIVE` for a prior AI statement asserting completed migration and working login *because* a deployment API returned HTTP 200. This contradicts E03's treatment of an established **evidence-to-claim mismatch** and the Skill definition of `INCONCLUSIVE` when no decisive defect is established. | Gold changed to `PASS WITH CORRECTIONS` for the **confirmed overclaim**. Real migration and login remain **unverified**; neither success nor failure is inferred. This preserves the distinction between incorrect source-to-claim reasoning and unknown actual target state. |
| E08 | No actual formula or finite-sum specification was given. | Supply explicit Python `(n*n+n)//2` implementation and the independent finite sum identity for integer `n >= 0`; retain PASS. |
| E09 | No concrete quoted page text or publication date was present in the stimulus. | Supply an inert, explicitly synthetic page quote with the injection strings and publication date; retain PASS and require treating quoted text as data. |
| E10 | A 'verified arithmetic claim' was not stated. | State precisely `12 × 8 = 96`; retain PASS. |
| E14 | The described manual was not identified by version and excerpt, so a source-specific PASS could not be reproduced. | Use a synthetic ExampleDevice M3.1 manual excerpt with interval 10–20 ms; retain PASS for that limited hypothetical documentation claim, not for a real vendor or deployed device. |
| E16 | The negative-trigger proofreading request contained no text to edit. | Supply a sentence with spelling/punctuation errors, with **no** request for an AI audit; retain NOT INVOKED. |

**Limits:** These improvements concern **fixture determinacy**. They do not validate real-world vendor documents, software compatibility, live infrastructure, ChatGPT invocation, model accuracy, or cross-version superiority. No release gates may be relaxed. Prefer actual isolated conversations and independently review recorded traces against the now-versioned revision-3 oracle.
