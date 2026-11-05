# BidRoom — Intake Room

## Purpose

This room extracts the RFP fact base for **RFP AVL-2026-041, Northstar Citizen Services Portal**. It does not score, recommend, or decide.

## Members

- Human pursuit lead.
- `@bid-analyst`.

Do not add `@bid-critic` to this room. Do not add `bid-policy`.

## Authoritative documents

Use only:

- `rfp-northstar` — the RFP.
- `capability-snapshot` — Meridian's evidence.

The bid policy is not in this room. The analyst does not evaluate policy gates, margin thresholds, or capacity thresholds.

## Scenario clock

The fictional review date is **October 24, 2026**. The deadline clarification was submitted on **October 19, 2026**; the buyer acknowledged receipt, and the response is pending.

Do not use the real system date. Do not say a deadline has passed based on the real date.

## Analyst output

Follow the output contract in `room/agent-bid-analyst.md`:

- RFP facts with section citations.
- M1–M6 mandatory requirements with status and evidence or gap.
- Evaluation criteria and weights.
- Conflicts and missing items.
- Document safety note.

The initial matrix describes **Meridian alone**. Do not mark a requirement `partner-covered` until the human explicitly asks for a partner scenario.

## Handoff

The analyst posts the matrix in this room. The human copies it into `bid-review` as the `analyst-matrix` room document.

This room does not make the decision.

## Prohibitions

- Do not score fit or recommend bid/no-bid.
- Do not issue a decision record.
- Do not open or cite `bid-policy`.
- Do not use local files, outside knowledge, or the kickoff message as evidence.
- Do not contact the buyer.
