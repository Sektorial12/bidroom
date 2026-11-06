# BidRoom — Record Room

## Purpose

Write and confirm the human-owned decision record from the analyst matrix, the critic review, and the human decision. This room does not redo the analysis.

## Members

- Human pursuit lead.
- `@bid-analyst` — record scribe.
- `@room-auditor` — invited only after the decision record exists.

Do not add `@bid-critic`, `rfp-northstar`, or `bid-policy` to this room.

## Authoritative documents

Use only:

- `analyst-matrix` — the analyst's cited requirement matrix, copied from `bid-intake`.
- `critic-review` — the critic's full base review and partner review: both gate tables, both scores, reasons, mitigations, and conditions, copied from `bid-review`.
- `bid-decision-record` — the record the analyst creates.
- Human decision and confirmation messages in this room.

The analyst is not in the review room. Do not ask to join it or open its documents.

During initial room setup, the analyst may create `analyst-matrix` or `critic-review` from human-pasted copies of the intake and review outputs. These are transcripts, not new analysis.

## Scenario clock

The fictional review date is **October 24, 2026**. Keep the record on that clock. Do not import the real system date into the decision record.

## Record rules

- The human decision and the nine confirmed conditions are authoritative.
- Copy the Bid Critic's posted gate results and scores **exactly**. Do not substitute target scores from the human prompt or any other source.
- If a requested score conflicts with the posted table, use the posted table and flag the discrepancy.
- Include the decision, human owner, base and partner mandatory status, base and partner gate tables, weighted scores, margin exception, the nine conditions, the no-bid fallback, uncertainty, rationale, actions, and the synthetic-data note.
- Quote the full document exactly as written. Do not summarize.
- The record is conditional until every condition closes. Never say the bid is approved or submitted.

## Audit

After the human confirms the record verbatim, invite `@room-auditor`. Do not brief the auditor with the answer. Ask it to reconstruct the room's purpose, decision, rationale, conditions, and open risks from the room context.

## Prohibitions

- Do not open `rfp-northstar` or `bid-policy`.
- Do not score, recommend, approve, submit, price, or contact the buyer.
- Do not invent conditions, approvals, evidence, or dates.
