# BidRoom — Record Room

## Purpose

Write and confirm the human-owned decision record from the analyst matrix, the critic review, and the human decision.

## Members

- Human decision owner: {{decision_owner}}.
- `@bid-analyst` as record scribe.
- `@room-auditor` only after the record is confirmed.

Do not add `@bid-critic`, the raw source document, or the policy document.

## Authoritative documents

- `analyst-matrix`.
- `critic-review`.
- `bid-decision-record`.
- Human decision and confirmation messages.

## Record rules

- The human decision and confirmed conditions are authoritative.
- Copy the critic's posted gates and scores exactly; do not substitute target scores.
- Include the decision, owner, base and decision-path gates, weighted scores, margin exception, conditions, fallback, uncertainty, rationale, actions, and synthetic-data note.
- Quote the full document exactly as written.
- The record is conditional until every condition closes. Never say the bid is approved or submitted.

## Audit

After the human confirms the record, invite `@room-auditor` and ask it to reconstruct the decision from this room. Do not brief it with the answer.

## Prohibitions

- Do not open the raw source document or the policy document.
- Do not score, recommend, approve, submit, price, or contact the buyer.
- Do not invent conditions, approvals, evidence, or dates.
