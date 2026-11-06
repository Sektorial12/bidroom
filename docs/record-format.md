# Decision record format

A decision record is JSON validated against a policy. The engine does not require Northstar IDs or values.

## Required fields

| Field | Meaning |
|---|---|
| `pursuit` | Pursuit or project name. |
| `rfp` | Solicitation reference. |
| `decision` | One of the policy's decision options. |
| `human_owner` | Named human owner; agent/model names are rejected. |
| `human_signoff` | Must be `true`. |
| `human_approval_ref` | Specific room message or approval record for a bid. |
| `decision_date` | ISO date. |
| `data_note` | Must affirm fictional/synthetic data. |
| `requirements` | Decision-path requirement table. |
| `base_requirements` | Bidder-alone requirement table. |
| `scores` | Decision-path weighted score entries. |
| `base_scores` | Bidder-alone score entries. |
| `total_score` | Recomputed decision-path total. |
| `base_total_score` | Recomputed base total. |
| `gates` | Decision-path gate table. |
| `base_gates` | Base gate table. |
| `margin_percent` | Decision-path margin. |
| `base_margin_percent` | Base margin. |
| `policy_min_margin_percent` | Must match the policy. |
| `conditions` | Conditions with text, owner, due date, optional status. |
| `actions` | Actions with text, owner, due date, optional status. |
| `rationale` | Human-readable rationale. |
| `uncertainty` | Open items and unknowns. |

## Optional fields

- `fallback` — required when the policy lists the decision in `fallback_required_for`.
- `gate_exceptions` — human exceptions for failed gates.
- `margin_exception` — human exception for a below-policy margin.
- `policy_id`, `policy_version` — traceability.

## Gate table

Each gate object has:

```json
{ "id": "G1", "text": "Mandatory requirements", "status": "fail", "evidence": "..." }
```

Statuses: `pass`, `pass_with_conditions`, `fail`.

## Score table

Scores are keyed by the policy's criterion IDs:

```json
{
  "fit": { "weight": 60, "score": 4, "evidence": "..." },
  "price": { "weight": 40, "score": 3, "evidence": "..." }
}
```

## Conditions and actions

```json
{
  "text": "Buyer confirms the deadline",
  "owner": "Priya Raman",
  "due_date": "2026-10-26",
  "status": "open"
}
```

`status` is optional and may be `open`, `done`, `blocked`, or `cancelled`.
