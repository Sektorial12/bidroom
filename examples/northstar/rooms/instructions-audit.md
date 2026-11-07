# BidRoom — Clean Audit Room

## Purpose

Reconstruct the decision from the final decision record alone. This room tests whether the record is self-contained.

## Members

- Human decision owner.
- `@room-auditor`.

Do not add `@bid-analyst`, `@bid-critic`, or any prior auditor.

## Authoritative document

Only the final `bid-decision-record` content.

Do not add the RFP, capability snapshot, policy, analyst matrix, or critic review.

## Rules

- Reconstruct the purpose, decision, rationale, nine conditions, and open risks from the record.
- Recompute the base and partner scores from the posted tables.
- Report conflicts, gaps, and unsupported claims.
- Do not approve, change, or redo the decision.
- Do not use outside knowledge or local files.
- Use a new auditor session. Report the result as a reconstruction, not an independent third-party audit.

## Question

```text
@room-auditor What is this room for, what did it decide, and why?
List all nine conditions and open risks.
```
