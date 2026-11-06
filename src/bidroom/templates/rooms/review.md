# BidRoom — Review Room

## Purpose

Apply the bid policy to the analyst matrix and the supplied evidence. The critic does not open the source document directly and does not approve.

## Members

- Human decision owner: {{decision_owner}}.
- `@bid-critic`.

Do not add `@bid-analyst` to this room. Do not add the raw source document.

## Authoritative documents

- The policy document.
- The capability/evidence snapshot.
- The `analyst-matrix` copied in by the human.

If a fact is missing, state the gap and ask the human to obtain it from the analyst. The analyst is not a member of this room.

## Critic output

Follow the output contract in `agents/critic.md`:

- Gate results, with base and decision-path statuses separate.
- Weighted score with evidence.
- Strongest case against the recommended path.
- Mitigations and conditions.
- Recommendation and what would change the decision.

## Handoff

The critic posts the review. The human copies it into the record room as the `critic-review` room document and makes the decision there.

## Prohibitions

- Do not open the raw source document.
- Do not approve, submit, price, or contact the buyer.
- Do not set the final decision.
