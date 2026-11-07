# Changelog

## Unreleased

- Tightened the public documentation and repository layout.
- Added an at-a-glance overview and a CLI reference to the README.

## 0.1.0 — 2026-11-06

- Added policy-driven decision engine in `src/bidroom`.
- Added generic policy and decision schemas.
- Added `bidroom init`, `validate`, `render`, and `check`.
- Added optional gate rules; margin, score, capacity, and human-approval gates can be disabled per policy.
- Added generic room and agent templates.
- Preserved the Northstar reference example under `examples/northstar`.
- Added generic engine tests and retained the Northstar conformance suite.
- Added packaging, CI, security, and contribution docs.
