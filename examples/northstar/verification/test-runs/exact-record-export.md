# Exact record export

The repository's `decision-record.three-room.md` is a reconstructed canonical export, not a verbatim copy of the live room document. Use this to capture the exact text.

## Prompt

Post in `bid-record-clean`, addressed to `@bid-analyst`:

```text
@bid-analyst Quote the full bid-decision-record document exactly as written, in one message. Do not summarize or change it.
```

## Capture

- Save the analyst's reply as `examples/northstar/verification/test-runs/raw/exact-record.md`.
- Include the post ID, timestamp, and channel.
- If the analyst cannot quote the document, record that limitation. Do not reconstruct it and call it exact.

## Then

- Compare the exact text to `examples/northstar/verification/decision-record.three-room.md`.
- If they differ, use the exact text as the authoritative record and update the canonical export.
- If the exact record still has G5/G6/condition-6 caveats, run the optional canonical consistency pass in `examples/northstar/rooms/record-resolutions.md`, re-confirm, and re-audit.
