# BidRoom — Review Room

## Purpose

Apply the bid policy to the analyst's cited requirement matrix and the capability evidence. The critic does not open the RFP and does not approve the bid.

## Members

- Human pursuit lead.
- `@bid-critic`.

Do not add `@bid-analyst` to this room. Do not add `rfp-northstar`.

## Authoritative documents

Use only:

- `bid-policy` — gates, scoring rules, approval authority, and prohibitions.
- `capability-snapshot` — Meridian's evidence.
- `analyst-matrix` — the analyst's cited requirement matrix, copied in by the human.

The analyst is not a member of this room. If a fact is missing from the matrix, state the gap and ask the human to obtain it from the analyst. Do not contact the analyst directly.

## Scenario clock

The fictional review date is **October 24, 2026**. The deadline clarification was submitted on **October 19, 2026**; the buyer acknowledged receipt, and the response is pending.

Do not use the real system date. Do not say a deadline has passed based on the real date.

## Critic output

Follow the output contract in `examples/northstar/rooms/agent-bid-critic.md`:

- G1–G6 gate results, with base and partner statuses separate.
- Weighted score with evidence.
- Strongest case against bidding.
- Mitigations and partner scenario.
- Recommendation and what would change the decision.
- All nine condition categories, with owners and due dates. Do not leave the nine-condition table to the human.

## Handoff

The critic posts the review in this room. The human copies the **full** review into `bid-record` as the `critic-review` room document: both the base review and the partner recalculation, including both gate tables and both scores. Do not copy only the final recommendation.

The human makes the decision in `bid-record`, not here. The critic does not approve.

## Prohibitions

- Do not open or cite `rfp-northstar`.
- Do not approve, submit, price, or contact the buyer.
- Do not use local files, outside knowledge, or the kickoff message as evidence.
- Do not set the final decision or record the human's conditions as if they were your own.
