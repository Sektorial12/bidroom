# Raw evidence

Captured from the local Mattermost instance on 2026-11-06, with a follow-up exact-record and clean-audit capture on 2026-11-07. The Mattermost exports used:

```text
docker exec <mattermost-container> /mattermost/bin/mmctl --local post list switch:<channel> --number 200 --show-ids --json
```

Files:

- `intake.json` — raw `bid-intake-clean` posts.
- `review.json` — raw `bid-review-clean` posts.
- `record.json` — raw `bid-record-clean` posts.
- `user-map.json` — user IDs mapped to role labels (`human`, `bid-analyst`, `auditor-1`, etc.); **no emails or personal usernames**.
- `transcript.md` — readable transcript with timestamps and post IDs.
- `membership.md` — raw `!list-agents` and `!list-documents` replies.
- `fresh-agent.md` — raw `room-auditor-2` second-agent reply from the first room; the first auditor's reply was still in the room, so that was not a clean-room audit.
- `exact-record.md` — exact `bid-decision-record` document text from the 2026-11-07 three-room run, captured from the Switch room document store. This is the authoritative live record; `decision-record.three-room.md` is the canonical readable reconstruction.
- `clean-audit.md` — exact `room-auditor-2` reply from `bid-audit-clean`, a room containing only `exact-record.md`. The auditor recomputed base 50 and partner 68, listed all nine conditions, and flagged the record's internal condition-6 and attribution ambiguities. It is a new-session reconstruction, not an independent third-party audit.
- `final-critic-review.md` — the critic's final corrected review from the 2026-11-07 run: base 50, partner 68, M4 conflicting, partner G3 `pass_with_conditions`.
- `human-confirmation.md` — raw human record confirmation.
- `boundary-probes.json` — raw probe posts and agent replies.
- `boundary-probes.md` — readable boundary-probe transcript.
- `post-index.csv` — channel/timestamp/author/post ID index.

The boundary probes were posted as the human account with a temporary Mattermost token. The token was revoked after capture and is not stored in the repository.

Scope: the three fictional BidRoom rooms only. The exports contain no credentials or user emails. Localhost document hosts are rendered as `http://<switch-host>` in the readable transcript and redacted in the JSON; post IDs, timestamps, and messages are otherwise preserved.

Post IDs can be opened in the local Mattermost UI by the operator. The public evidence is the post ID plus the message text in these files.
