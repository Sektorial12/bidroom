# Northstar reference example

A frozen reference example for BidRoom. It shows a three-room bid/no-bid decision using fictional data; it is not the generic engine.

## What is here

- `manifest.json` — project metadata used by `bidroom check`.
- `policy.json` — the machine-readable Meridian policy used by the generic engine.
- `sources/` — the fictional RFP, capability snapshot, and bid policy.
- `rooms/` — room instructions, agent prompts, and handoff messages.
- `verification/` — the example decision JSON, an example decision record, and a record template.
- `fixtures/` — valid and adversarial decision fixtures used by the validator tests.
- `docs/architecture.md` — the example-specific architecture.

## Quickstart

```powershell
python -m unittest discover -s tools/tests -q
python tools/bidcheck.py examples/northstar/verification/decision.example.json
```

Expected:

```text
VALID: Northstar Citizen Services Portal | bid_with_partner | 68/100
```

## Result

- Base: **50/100**
- Partner: **68/100**
- Decision: **Bid with partner, conditional**
- Human owner: **Priya Raman, Bid Director**
- Nine confirmed conditions and a no-bid fallback.

The partner route clears the 65 threshold by three points. The record remains conditional and not approved or submitted.

## Notes

- All names, organisations, dates, prices, and documents are fictional.
- The production engine in `src/bidroom/` is policy-driven and does not contain these names or thresholds.
