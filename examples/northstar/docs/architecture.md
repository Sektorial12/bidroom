# Architecture

## Summary

BidRoom is a **three-room Switch workflow** with two Claude Code agents, one fresh auditor, and a human decision owner. The source boundary is enforced by **room membership**: the analyst and critic are never members of each other's source rooms, and the human carries the matrix and critic review between rooms.

A deterministic Python validator checks the structured decision record after the human decision.

## Rooms and components

| Component | Role |
|---|---|
| Switch Console | Creates the rooms and agents; manages membership and settings. |
| Switch server | Connects the room context and messaging. |
| `bid-intake` | Human + `bid-analyst`; holds `rfp-northstar` and `capability-snapshot`; no policy. |
| `bid-review` | Human + `bid-critic`; holds `bid-policy`, `capability-snapshot`, and `analyst-matrix`; no RFP. |
| `bid-record` | Human + `bid-analyst`; holds `analyst-matrix`, `critic-review`, and `bid-decision-record`; no RFP or policy. |
| `bid-analyst` | Extracts RFP facts with citations in intake; writes the record from the matrix and critic review. |
| `bid-critic` | Applies gates, scores fit, and argues against bidding in review. |
| `room-auditor` | Joins `bid-record` after the decision and reconstructs it without a briefing. |
| Human pursuit lead | Owns the decision and the handoff; the only member of all three rooms. |
| `bidcheck` | Standard-library Python validator for the decision JSON. |

## Data flow

```text
Human
  │
  ├── bid-intake ── @bid-analyst
  │     documents: rfp-northstar, capability-snapshot
  │     output: analyst-matrix
  │
  │   human copies analyst-matrix into bid-review
  │
  ├── bid-review ── @bid-critic
  │     documents: bid-policy, capability-snapshot, analyst-matrix
  │     output: critic-review (full base review + partner review)
  │
  │   human copies critic-review into bid-record
  │
  ├── bid-record ── @bid-analyst
  │     documents: analyst-matrix, critic-review
  │     human decision + nine conditions
  │     output: bid-decision-record
  │
  ├── human confirms the record verbatim
  │
  └── bid-record ── @room-auditor (invited after the decision)
        reconstructs purpose, decision, rationale, conditions, risks
```

## Why the rooms are structurally separate

- The critic never receives `rfp-northstar`; it works from the analyst's cited matrix.
- The analyst never receives `bid-policy`; it extracts evidence and writes the record.
- The human carries the matrix and critic review between rooms.
- No agent is a member of both source rooms. The boundary is visible in `!list-agents` and `!list-documents`.
- The analyst is in `bid-intake` and `bid-record`; it sees the RFP in intake and the derived matrix in record, never the policy.
- Switch does not enforce per-document permissions. The room membership list is the boundary, and the setup forbids adding both source agents to the same room.
- Remove the rooms and the workflow collapses into a single-agent summary with no independent review or durable decision trail.

## Agent boundaries

### Bid Analyst

- In `bid-intake`: extracts facts, requirements, deadlines, evaluation criteria, and contract terms; cites RFP sections; marks `met`, `missing`, `conflicting`, `partner-covered`, or `not assessed`.
- In `bid-record`: writes the record from the analyst matrix, critic review, and human decision; copies the critic's posted scores exactly.
- Does not open the policy; does not score, recommend, approve, or contact the client.

### Bid Critic

- Applies hard gates before scoring.
- Scores against the capability snapshot and analyst matrix.
- Argues the strongest case against bidding.
- Identifies mitigations and conditions.
- Does not open the RFP, approve, submit, price, or contact the client.

### Human

- Challenges assumptions.
- Carries the matrix and critic review between rooms.
- Chooses the final outcome.
- Approves any policy exception.
- Confirms the decision record verbatim.

### Room Auditor

- Joins after the decision.
- Reconstructs the purpose, decision, rationale, conditions, and risks from room context.
- Does not change or approve the decision.

## Decision record

The record contains:

- Pursuit and RFP reference.
- Decision and human owner.
- Base and partner mandatory status.
- Base and partner gate results.
- Base and partner weighted scores with evidence.
- Margin and any exception.
- Nine conditions and actions with owners and due dates.
- No-bid fallback.
- Uncertainty.
- Rationale.
- Synthetic-data note.

## Validator

`tools/bidcheck.py` validates:

- Required fields and decision enum.
- Human signoff and a named human owner; agent, project-agent, and model names plus placeholders are rejected.
- Agent approval/submission claims in the approval reference, rationale, or uncertainty are rejected.
- The data note rejects real-client-data and confidential-data claims.
- Specific human approval and record references.
- Requirement statuses and evidence; exactly M1–M6.
- Base requirements must describe Meridian alone; `partner_covered` belongs only in the decision path.
- G1 rejects missing, conflicting, or not-assessed mandatory requirements.
- Exactly G1–G6 in both gate tables.
- Four weighted criteria; weights sum to 100.
- Total score matches the weighted calculation.
- A bid decision requires at least 65.
- G2, G3, and G4 consistency with the evidence.
- Failed gates block a bid unless a complete human gate exception exists.
- Margin below policy requires a recorded exception.
- Nine named condition categories and substantive owners for bid-with-partner.
- The data note confirms synthetic data.

It emits a markdown decision record and returns `0` valid, `1` validation error, `2` usage/IO error.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── examples/northstar/sources/
├── examples/northstar/rooms/
├── examples/northstar/verification/
├── tools/
└── docs/
```

## Security and privacy

- All sample data is fictional.
- The agents run in an isolated working directory outside the repository.
- The authoritative materials live in the Switch rooms, not in agent-local files.
- Agents have no shell, network, or external-action tools.
- No agent can approve, submit, price, or contact a client.
- The decision record is human-approved.

## Limitations

- BidRoom is a decision-support prototype, not a production bid-management or legal system.
- It checks only the materials supplied in the rooms.
- It does not verify the truth of the RFP or capability evidence.
- It does not generate a proposal or submit a bid.
- The room-membership boundary depends on the human not adding both source agents to the same room. Room membership and the agent list make that visible.
- The scoring model is illustrative and must be calibrated for a real organization.
