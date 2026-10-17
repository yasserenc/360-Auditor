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
