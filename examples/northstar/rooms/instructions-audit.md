# BidRoom — Clean Audit Room

## Purpose

Reconstruct the decision from the final decision record alone. This room exists to test whether the record is self-contained.

## Members

- Human decision owner.
- The chosen auditor: `@room-auditor-3` preferred, `@room-auditor-2` fallback.

Do not add `@bid-analyst`, `@bid-critic`, or the first `room-auditor`.

## Authoritative document

Only the exact `bid-decision-record` content from `verification/test-runs/raw/exact-record.md`.

Do not add the RFP, capability snapshot, policy, analyst matrix, or critic review.

## Rules

- Reconstruct the purpose, decision, rationale, nine conditions, and open risks from the record.
- Recompute the base and partner scores from the posted tables.
- Report conflicts, gaps, and unsupported claims.
- Do not approve, change, or redo the decision.
- Do not use outside knowledge or local files.

## Question

```text
@room-auditor-3 What is this room for, what did it decide, and why?
List all nine conditions and open risks.
```

If using the fallback, replace `@room-auditor-3` with `@room-auditor-2`. The captured 2026-11-07 audit used `room-auditor-2` in a record-only room; caption it **"new-session reconstruction; record-only room."**
