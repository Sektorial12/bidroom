# BidRoom — Three-Room Workflow

BidRoom separates the RFP evidence from the bid policy with **room membership**, not prompt-only role instructions.

## Rooms

| Room | Members | Authoritative documents | Output |
|---|---|---|---|
| `bid-intake` | Human + `@bid-analyst` | `rfp-northstar`, `capability-snapshot` | `analyst-matrix` |
| `bid-review` | Human + `@bid-critic` | `bid-policy`, `capability-snapshot`, `analyst-matrix` | `critic-review` |
| `bid-record` | Human + `@bid-analyst`; `@room-auditor` after the decision | `analyst-matrix`, `critic-review`, `bid-decision-record` | Human-confirmed decision record |

The human is the only member of all three rooms. The analyst is not a member of `bid-review`. The critic is not a member of `bid-intake` or `bid-record`. The auditor joins `bid-record` only after the record exists.

## Handoff

```text
bid-intake
  Human asks @bid-analyst for the requirement matrix.
  Analyst posts the cited matrix.
      ↓ human copies the matrix into bid-review as analyst-matrix
bid-review
  Human asks @bid-critic for the base gate review and strongest case against bidding.
  Human provides partner evidence; critic recalculates the partner route.
  Critic posts gates, scores, reasons, mitigations, and conditions.
      ↓ human copies the critic review into bid-record as critic-review
bid-record
  Human posts the decision and the nine confirmed conditions.
  Human asks @bid-analyst to create bid-decision-record.
  Analyst copies the critic's posted scores and records the human decision.
  Human confirms the record verbatim.
  Human invites @room-auditor and asks it to reconstruct the decision.
```

## Why the rooms are separate

- The critic never receives `rfp-northstar`; it works from the analyst's cited matrix.
- The analyst never receives `bid-policy`; it extracts evidence and writes the record.
- The human carries the matrix and the critic review between rooms.
- The source boundary is enforced by room membership. Do not add both agents to both source rooms; that would break the design.
- Switch does not enforce per-document permissions. The boundary here is the room membership list, which is visible in `!list-agents` and `!list-documents`.

## Scenario clock

The fictional review date is **October 24, 2026**. The deadline clarification was submitted on **October 19, 2026**; the buyer acknowledged receipt, and the response is pending. Do not use the real system date.

## Decision rules

- Apply hard gates **before** scoring.
- The minimum weighted score is **65/100**.
- The minimum margin is **15%** unless the VP of Finance approves a written exception.
- Key roles must be staffed at **50% or more for the first 90 days**, or a written mitigation must be recorded.
- Any deadline conflict must be clarified with the buyer; do not assume a date.
- The human chooses the final outcome. No agent may approve, submit, price, or contact the client.

## Room setup

Paste the room-specific instructions into each room before adding agents:

- `examples/northstar/rooms/instructions-intake.md`
- `examples/northstar/rooms/instructions-review.md`
- `examples/northstar/rooms/instructions-record.md`

Create the three rooms and add the matching agents. The room prompts in this directory define the handoff.
