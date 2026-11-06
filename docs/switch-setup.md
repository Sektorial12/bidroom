# Switch room setup

BidRoom uses three Switch rooms so the analyst and critic never share a source boundary. The human is the only member of all three rooms and carries the handoff.

## Rooms

| Room | Members | Documents | Output |
|---|---|---|---|
| Intake | Human + analyst | Source document(s), capability/evidence | Analyst matrix |
| Review | Human + critic | Policy, capability/evidence, analyst matrix | Critic review |
| Record | Human + analyst; auditor after the decision | Analyst matrix, critic review, decision record | Confirmed record |

Do not add the analyst to the review room. Do not add the critic to the intake or record rooms. Do not put the raw source in the review/record rooms or the policy in the intake/record rooms.

## Setup

1. Create the three rooms in Switch Console before adding agents.
2. Paste the matching prompts from `rooms/` into each room's instructions.
3. Create the analyst, critic, and auditor agents from `agents/`.
4. Add the analyst to intake and record, the critic to review, and the auditor to record only after the decision.
5. Capture `!list-agents` and `!list-documents` in each room. Those are the source-boundary evidence.

## Handoff

1. Intake: the analyst posts the cited matrix.
2. The human copies it into review as `analyst-matrix`.
3. Review: the critic posts gates, scores, reasons, and conditions.
4. The human copies the full critic review into record as `critic-review`.
5. The human posts the decision and confirmed conditions.
6. The analyst writes `bid-decision-record`.
7. The human confirms it verbatim.
8. A fresh auditor reconstructs it in a room that does not contain a prior auditor's answer.

## Why the boundary holds

The boundary is room membership, not per-document permissions. Switch does not enforce decision boundaries; it does enforce who is in the room. The setup and the `!list-agents` capture make that visible. If the human adds both source agents to the same room, the boundary is broken.
