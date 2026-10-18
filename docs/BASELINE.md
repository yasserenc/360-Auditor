# P01 — Frozen baseline (2026-10-17)

Source: [main at f051f112](https://github.com/yasserenc/360-Auditor/tree/f051f112bb23819c5738764d6ee42eee3b59cdab). Compared against tag [v1.0.1](https://github.com/yasserenc/360-Auditor/releases/tag/v1.0.1) at `cea2ee821ec46938420d90f9dd9ef7d715b10b7f`. On 2026-10-17 main matched the prior audited SHA. `v1.0.1...main` is two commits ahead and differs only in `.github/workflows/release.yml` (no runtime file drift).

The original tree has 14 runtime files: `SKILL.md`, `agents/openai.yaml`, `assets/icon.svg`, and 11 `references/*.md`. Source manifest: [immutable GitHub commit tree](https://github.com/yasserenc/360-Auditor/tree/f051f112bb23819c5738764d6ee42eee3b59cdab).

Existing releases (release API [v1.0.1](https://api.github.com/repos/yasserenc/360-Auditor/releases/tags/v1.0.1) and [v1.0.0](https://api.github.com/repos/yasserenc/360-Auditor/releases/tags/v1.0.0)):

| Version | Tag commit | `skill.zip` SHA-256 as reported by GitHub | `SHA256SUMS.txt` SHA-256 reported by GitHub |
|---|---|---|---|
| v1.0.1 | `cea2ee821ec46938420d90f9dd9ef7d715b10b7f` | `23caea8ee98c3d1ad7683108c1e825a05480112c53bf9e1a7d05f06d38efae8f` | `9ee83ab4fb9fb9b7efd5efa1f301aeb4aa2785d63df39230a914ec13076a19e3` |
| v1.0.0 | `2973df5da26210cfe8fa59b707d0c9fefa1dc379` | `d5fe96da8f964bef097ddd9b7287edd4ba9e6297eff755d0b8c29ab0f69bf616` | `5c17da34304978afa05c2a162987bb9ada4d27dcfc9cc6451d20` |

These are remote metadata digests, NOT locally recomputed download digests: raw historic ZIP bytes were not independently downloaded in this session. Do not represent metadata inspection as raw-byte verification.

At inspection `main` reported `protected:false`, repository rulesets query returned `[]`, and the protection-detail API returned 403 (GitHub App installation limitation). Therefore no protection is asserted. Neither old release/tag was modified. Work branch: `fix/v2-auditor-verified-release-20261017`, created from exact main SHA; no force push. New-tag publication prohibited until P10/P12/P13 host and behavior gates pass.
