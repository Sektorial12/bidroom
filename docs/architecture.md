# Architecture

## Summary

BidRoom is a policy-driven decision-record engine plus a three-room Switch workflow. The engine is generic; the Northstar pursuit is a reference example under `examples/northstar/`.

The product has four layers:

1. **Policy** — a JSON document that defines gates, requirements, scoring, thresholds, condition categories, and decision rules.
2. **Decision records** — structured JSON that the engine validates and renders.
3. **Switch rooms** — intake, review, and record rooms with membership-based source separation and a human handoff.
4. **CLI and templates** — `bidroom init`, `validate`, `render`, and `check`.

## Components

| Component | Role |
|---|---|
| `src/bidroom/policy.py` | Loads and validates policy JSON. |
| `src/bidroom/engine.py` | Policy-driven validation and markdown rendering. |
| `src/bidroom/scaffold.py` | Creates new projects and checks manifests. |
| `src/bidroom/cli.py` | `bidroom` command-line interface. |
| `src/bidroom/templates/` | Generic room, agent, and project templates. |
| `src/bidroom/schema/` | JSON schemas for policies and decision records. |
| `examples/northstar/` | Frozen Northstar demo with sources, rooms, records, and raw evidence. |
| `tools/bidcheck.py` | Legacy Northstar conformance adapter. |

## Engine flow

```text
policy.json ──▶ policy loader ──▶ validator ──▶ valid / errors
                                      │
decision.json ────────────────────────┴──▶ renderer ──▶ markdown
```

The engine does not know Northstar IDs, weights, thresholds, or condition names. It reads them from the policy. A second policy test under `tests/` proves that the same engine accepts different gates and criteria.

## Room flow

```text
Intake room: source + evidence ──▶ analyst matrix
        human copies matrix
Review room: policy + evidence + matrix ──▶ critic review
        human copies review and decides
Record room: matrix + review + human decision ──▶ decision record
        human confirms, fresh auditor reconstructs
```

The human is the only member of all three rooms. The analyst and critic never share a source room. The boundary is membership, not per-document permissions; the setup and `!list-agents` capture make it visible.

## Policy and record schemas

- Policy schema: `src/bidroom/schema/policy.schema.json`
- Decision schema: `src/bidroom/schema/decision.schema.json`
- Policy authoring: `docs/policy-authoring.md`
- Record format: `docs/record-format.md`
- Switch setup: `docs/switch-setup.md`

## Security and limits

- All examples are fictional or synthetic.
- The engine does not prove that evidence is true, complete, or current.
- The engine does not submit bids, contact buyers, price work, or approve spend.
- Human review and human approval remain required.
- Do not put credentials, real procurement data, or personal data in the public repository.

## Reference example

The Northstar demo is under `examples/northstar/`. It preserves the original three-room run, the base 50/100 and partner 68/100 scores, the conditional bid-with-partner decision, and the raw Mattermost exports. See `examples/northstar/README.md`.
