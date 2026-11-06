# Northstar reference example

This directory is the frozen Northstar demo. It is a reference implementation of the BidRoom workflow, not the generic engine.

## What is here

- `sources/` — the fictional RFP, capability snapshot, and bid policy.
- `rooms/` — Switch room instructions, agent prompts, handoff messages, and boundary probes.
- `verification/` — the expected-findings oracle, example record, live record exports, transcripts, raw Mattermost evidence, and test-run runbooks.
- `fixtures/` — the validator's valid and adversarial decision fixtures.

## Demo quickstart

```powershell
python -m unittest discover -s tools/tests -q
python tools/bidcheck.py examples/northstar/verification/decision.example.json
```

Expected:

```text
VALID: Northstar Citizen Services Portal | bid_with_partner | 68/100
```

The three-room Switch setup is in `docs/setup.md`. The exact live evidence is in `verification/test-runs/`.

## Recorded result

- Base: **50/100**
- Partner: **68/100**
- Decision: **Bid with partner, conditional**
- Human owner: **Priya Raman, Bid Director**

The partner route clears the 65 threshold by three points. The record remains conditional and not approved or submitted.

## Notes

- The demo is intentionally opinionated: Meridian Digital Services, the State of Avalon, and Helix Systems.
- The production engine in `src/bidroom/` is policy-driven and does not contain these names or thresholds.
- The raw evidence contains local Mattermost post IDs and is sanitized for public display; see `verification/test-runs/raw/README.md`.
