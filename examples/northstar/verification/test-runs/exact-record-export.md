# Exact record export

The repository's `decision-record.three-room.md` is a canonical readable reconstruction, not a verbatim copy of the live room document.

**Captured 2026-11-07:** the exact live document text is `examples/northstar/verification/test-runs/raw/exact-record.md`. It was read from the Switch room document store for `bid-decision-record` in `bid-record-clean`. The exact export and the canonical reconstruction agree on the decision, base 50 / partner 68, the nine conditions, and the no-bid fallback; the exact export also contains the detailed condition-difference table and the live wording.

## Reproduce

Post in `bid-record-clean`, addressed to `@bid-analyst`:

```text
@bid-analyst Quote the full bid-decision-record document exactly as written, in one message. Do not summarize or change it.
```

## Capture

- Save the analyst's reply as `examples/northstar/verification/test-runs/raw/exact-record.md`.
- Include the post ID, timestamp, and channel.
- If the analyst cannot quote the document, read the room document store directly and say so. Do not reconstruct it and call it exact.

## Compare

- Compare the exact text to `examples/northstar/verification/decision-record.three-room.md`.
- If they differ, use the exact text as the authoritative record and update the canonical export.
- The captured exact record still has the condition-6 and attribution ambiguities flagged by the clean audit. Run the optional canonical consistency pass in `examples/northstar/rooms/record-resolutions.md`, re-confirm, and re-audit if those need to be normalized.
