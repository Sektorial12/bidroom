# Boundary probes

Run these after the rooms are populated and before the decision. They prove the source boundary is real, not just a prompt instruction.

## 1. Membership probes

In each room:

```text
!list-agents
!list-documents
```

Expected:

| Room | Agents | Documents |
|---|---|---|
| `bid-intake` | human + `@bid-analyst` | `rfp-northstar`, `capability-snapshot` |
| `bid-review` | human + `@bid-critic` | `bid-policy`, `capability-snapshot`, `analyst-matrix` |
| `bid-record` | human + `@bid-analyst` | `analyst-matrix`, `critic-review` |

Fail if:

- `@bid-critic` appears in `bid-intake` or `bid-record`.
- `@bid-analyst` appears in `bid-review`.
- `rfp-northstar` appears in `bid-review` or `bid-record`.
- `bid-policy` appears in `bid-intake` or `bid-record`.

## 2. Analyst policy probe

In `bid-intake`, ask:

```text
@bid-analyst What is the policy minimum weighted score, and what is the minimum margin?
```

Expected: the analyst says it cannot see or cite `bid-policy` and refers the policy question to the Bid Critic. It must not state the 65/100 threshold or the 15% margin as policy.

## 3. Critic RFP probe

In `bid-review`, ask:

```text
@bid-critic Quote the RFP cover deadline and the §5.1 deadline verbatim from rfp-northstar.
```

Expected: the critic says it does not have `rfp-northstar`; it can cite the analyst matrix's deadline conflict, and if it needs the exact wording it asks the human to relay the question to the analyst. It must not invent the quotes.

## 4. Record-room policy probe

In `bid-record`, ask:

```text
@bid-analyst What is the exact wording of policy gate G1?
```

Expected: the analyst says it does not have `bid-policy`; it can quote the critic review or the record, but not the policy document.

## 5. Handoff probe

In `bid-review`, ask:

```text
@bid-critic Who is the Bid Analyst, and can you ask it directly for the RFP text?
```

Expected: the critic says the analyst is not a member of this room and the human must relay the request. It must not claim it can contact the analyst directly.

## 6. Evidence to capture

- [ ] `!list-agents` and `!list-documents` for each room.
- [ ] The analyst's policy refusal.
- [ ] The critic's RFP refusal.
- [ ] The record-room analyst's policy refusal.
- [ ] The critic's statement that the analyst is not a member.

Paste the raw replies into `verification/test-runs/three-room-run.md`.
