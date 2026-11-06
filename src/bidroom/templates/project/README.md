# {{project_name}}

This BidRoom project was created with `bidroom init`.

## Files

- `manifest.json` — project metadata and source paths.
- `policy.json` — machine-readable bid/no-bid policy.
- `sources/` — the RFP, capability evidence, and other source material.
- `rooms/` — room prompts for the three-room Switch workflow.
- `agents/` — analyst, critic, and auditor prompts.
- `records/` — decision records and validation output.

## First steps

1. Replace the placeholder files in `sources/` with your own material.
2. Edit `policy.json` to match your gates, criteria, thresholds, and evidence rules.
3. Paste the prompts in `rooms/` into your Switch rooms.
4. Validate a decision with:

```text
bidroom validate --policy policy.json records/decision.json
```

5. Render the record with:

```text
bidroom render --policy policy.json records/decision.json --md records/decision.md
```
