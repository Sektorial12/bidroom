# Policy authoring

A BidRoom policy is a JSON document that tells the engine how to evaluate a decision record. The policy is data, not prompt text.

## Minimal shape

```json
{
  "schema_version": "1.0",
  "policy_id": "example-policy",
  "policy_version": "1.0.0",
  "decision": {
    "options": ["bid", "no_bid"],
    "bid_options": ["bid"],
    "no_bid": "no_bid",
    "fallback_required_for": []
  },
  "requirements": {
    "ids": ["R1"],
    "statuses": ["met", "missing", "conflicting", "partner_covered", "not_assessed"],
    "base_partner_status": "partner_covered",
    "blocking_statuses": ["missing", "conflicting", "not_assessed"]
  },
  "scoring": {
    "formula": "weighted_sum_div_5",
    "minimum_score": 65,
    "criteria": [
      { "id": "fit", "label": "Fit", "weight": 60 },
      { "id": "price", "label": "Price", "weight": 40 }
    ]
  },
  "gates": [
    { "id": "G1", "text": "Mandatory requirements", "type": "requirements" },
    { "id": "G2", "text": "Minimum score", "type": "score_threshold" },
    { "id": "G3", "text": "Minimum margin", "type": "margin_threshold" },
    { "id": "G4", "text": "Human approval", "type": "human_approval" }
  ],
  "gate_rules": {
    "requirements_gate": "G1",
    "score_gate": "G2",
    "margin_gate": "G3",
    "capacity_gate": "G1",
    "capacity_requirement": "R1",
    "human_approval_gate": "G4"
  },
  "thresholds": {
    "minimum_margin_percent": 15,
    "gate_exception_role": "Pursuit Lead + Accountable Executive",
    "margin_exception_role": "VP of Finance"
  },
  "conditions": {
    "minimum_count": 0,
    "categories": [
      { "id": "approval", "label": "Approval", "keywords": [["approval"]] }
    ]
  },
  "data_note": {
    "required_any": ["fictional", "synthetic"],
    "forbidden_any": ["real client", "real data", "confidential data"]
  }
}
```

## Gate types

| Type | What the engine checks |
|---|---|
| `requirements` | The gate cannot pass while a required item is in a blocking status. Base requirements must be bidder-only. |
| `score_threshold` | The gate must align with the weighted score against `minimum_score`. |
| `margin_threshold` | A margin below `minimum_margin_percent` cannot be `pass`; a bid below the threshold needs a margin exception. |
| `capacity` | The gate cannot pass while the configured capacity requirement is blocking. |
| `deadline` | Reserved for deadline/conflict checks; the evidence still must be present. |
| `human_approval` | The gate cannot be `fail` when `human_signoff` is true. |
| `manual` | No automatic rule beyond the gate structure and exception handling. |

## Optional gates

A policy does not have to use every gate type. Set a gate rule to `null` or omit it:

```json
"gate_rules": {
  "requirements_gate": "G1",
  "score_gate": null,
  "margin_gate": null,
  "capacity_gate": null,
  "capacity_requirement": null,
  "human_approval_gate": "G4"
}
```

Rules:

- `margin_gate: null` disables the margin-exception requirement and the margin gate consistency check.
- `score_gate: null` disables the gate-alignment check, but the policy's `scoring.minimum_score` still applies to bid decisions.
- `capacity_gate` and `capacity_requirement` must both be set or both be `null`.
- Any gate defined in `gates` must still appear in the decision record's gate table; the engine validates its structure and evidence.
- A gate with no automatic rule is effectively a manual gate. The human and critic still fill it in.

## Scoring

`weighted_sum_div_5` is:

```text
sum(score × weight) / 5
```

Weights must sum to 100. Scores are 1–5. The engine recomputes the total from the score table; a mismatch is an error.

## Conditions

`conditions.categories` defines the condition categories a bid-with-partner (or other fallback-required decision) must cover. Each category has one or more keyword groups. A condition matches a category if every keyword in at least one group appears in the condition text.

Use categories to prevent nine placeholder rows. The condition text, owner, and due date are also checked for substance.

## Exceptions

- Gate exceptions need a gate ID, human approver, the configured role, a reason, a date, and a real record reference.
- Margin exceptions need a human approver, the configured role, a reason, a date, and a real record reference.
- Agent and model names are rejected as human owners or approvers.
- Agent approval/submission claims are rejected in the approval reference, rationale, and uncertainty.

## Versioning

- Change `policy_version` when behavior changes.
- Keep `policy_id` stable for a policy family.
- Record the policy version in each decision record if your process requires it.
- Do not edit a policy without re-validating the records it governs.
