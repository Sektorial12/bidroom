# BidRoom

**A policy-driven bid/no-bid decision workflow for Switch rooms — with a skeptical critic, a human-owned record, and a deterministic validator.**

BidRoom turns a qualification decision into a durable, auditable artifact. The generic engine is policy-driven; the Northstar pursuit is a frozen reference example.

> **Status:** The policy-driven engine, CLI, templates, and Northstar demo are complete. The exact live record export, clean independent audit, and demo video are still pending.
>
> **Public repository:** https://github.com/Sektorial12/bidroom

## The problem

Sales and proposal teams receive more RFPs than they can pursue well. Bid/no-bid decisions are often made in email or chat, without a shared evidence base or a record of why the team committed.

The failure mode is not “we need another summary.” It is a fragmented qualification process:

- Mandatory requirements and evidence gaps are scattered.
- Capacity and commercial constraints arrive late.
- The critic’s objections are lost.
- The final decision has no owner, conditions, or fallback.

BidRoom makes the decision explicit.

## What it does

The workflow uses three Switch rooms:

| Room | Members | Documents | Output |
|---|---|---|---|
| Intake | Human + analyst | Source document(s), capability/evidence | Analyst matrix |
| Review | Human + critic | Policy, capability/evidence, analyst matrix | Critic review |
| Record | Human + analyst; auditor after the decision | Analyst matrix, critic review, decision record | Confirmed record |

The human is the only member of all three rooms. The analyst never sees the policy; the critic never sees the raw source. The human carries the matrix and critic review between rooms.

A policy JSON file defines the gates, requirements, scoring, thresholds, condition categories, and decision rules. The engine validates a decision record against that policy and renders markdown.

## Quickstart

```powershell
python -m pip install -e .
```

Create a project:

```powershell
bidroom init my-pursuit --name "My Pursuit" --owner "Alex Doe, Bid Director"
```

Check the project and policy:

```powershell
bidroom check --project my-pursuit
```

Validate and render a decision:

```powershell
bidroom validate --policy my-pursuit/policy.json my-pursuit/records/decision.json
bidroom render --policy my-pursuit/policy.json my-pursuit/records/decision.json --md my-pursuit/records/decision.md
```

From a source checkout without installing:

```powershell
python tools/bidroom.py check --project examples/northstar
```

## Policy-driven, not scenario-specific

A policy is data:

```json
{
  "policy_id": "example-policy",
  "scoring": {
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
  ]
}
```

The engine does not contain Northstar IDs, weights, thresholds, or condition names. A second policy test under `tests/` uses different gates and criteria to prove that. Optional gates — such as margin or capacity — can be disabled by setting their gate rule to `null`.

Read more:

- `docs/policy-authoring.md`
- `docs/record-format.md`
- `docs/switch-setup.md`
- `docs/architecture.md`

## Northstar reference example

The original demo is preserved under `examples/northstar/`.

- Base: **50/100**
- Partner: **68/100**
- Decision: **Bid with partner, conditional**
- Human owner: **Priya Raman, Bid Director**
- Nine confirmed conditions and a no-bid fallback.

The demo includes the source packet, three-room prompts, decision records, transcripts, raw Mattermost exports, and adversarial fixtures. The canonical record is a reconstructed export; the exact room document and a clean independent audit are still pending, as documented in the demo runbooks.

```powershell
python -m unittest discover -s tools/tests -q
python tools/bidcheck.py examples/northstar/verification/decision.example.json
```

Expected:

```text
VALID: Northstar Citizen Services Portal | bid_with_partner | 68/100
```

See `examples/northstar/README.md`.

## Repository layout

```text
.
├── src/bidroom/          # policy engine, CLI, schemas, templates
├── tests/                # generic engine and scaffolding tests
├── examples/northstar/   # frozen Northstar demo
├── tools/                # source-checkout CLI and legacy conformance adapter
├── docs/                 # generic architecture and authoring docs
├── pyproject.toml
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## Tests

```powershell
python -m unittest discover -s tests -v
python -m unittest discover -s tools/tests -v
```

- `tests/` covers the generic engine, a second policy, optional gates, scaffolding, and project checks — **11 tests**.
- `tools/tests/` is the Northstar conformance suite — **49 tests**.

## Security and limits

- This is a decision-support prototype, not a production bid-management, legal, or procurement system.
- It validates structure, arithmetic, policy thresholds, and human-ownership fields.
- It does not prove that evidence is true, complete, or current.
- It does not submit bids, set prices, contact buyers, or approve spend.
- All sample data is fictional.
- Do not commit credentials, real procurement data, or personal data.
- The Switch boundary is room membership, not per-document permissions. If the human adds both source agents to the same room, the boundary is broken.

## Hackathon

Built for the **Flip the Switch Hackathon 2026** — **Best Business Workflow** track.

The workflow uses three Switch rooms to separate source evidence from bid policy, with a human carrying the handoff and owning the decision.

## License

MIT. See `LICENSE`.
