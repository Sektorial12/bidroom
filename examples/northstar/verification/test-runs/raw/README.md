# Raw evidence

Captured from the local Mattermost instance on 2026-11-06 with:

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
- `fresh-agent.md` — raw `room-auditor-2` reply.
- `human-confirmation.md` — raw human record confirmation.
- `boundary-probes.json` — raw probe posts and agent replies.
- `boundary-probes.md` — readable boundary-probe transcript.
- `post-index.csv` — channel/timestamp/author/post ID index.

The boundary probes were posted as the human account with a temporary Mattermost token. The token was revoked after capture and is not stored in the repository.

Scope: the three fictional BidRoom rooms only. The exports contain no credentials or user emails. Localhost document hosts are rendered as `http://<switch-host>` in the readable transcript and redacted in the JSON; post IDs, timestamps, and messages are otherwise preserved.

Post IDs can be opened in the local Mattermost UI by the operator. The public evidence is the post ID plus the message text in these files.
