# Raw evidence capture checklist

Use this checklist during the final demo run. The goal is to replace the cleaned transcript with evidence a judge can verify without trusting a summary.

## Before the run

- [ ] Capture `!list-agents` in each room and confirm the expected members.
- [ ] Capture `!list-documents` in each room and confirm only the intended documents are present.
- [ ] Confirm `examples/northstar/verification/expected-findings.md` is **not** attached to any room.
- [ ] Confirm the analyst and critic are not members of each other's source room.
- [ ] Note the Switch Console, core, Mattermost, Claude Code, model, and effort versions in `docs/environment.md`.

## During the run

- [ ] Capture the human kickoff message.
- [ ] Capture the analyst's full requirement matrix, including the document safety note.
- [ ] Capture the critic's full base gate review, score table, and strongest case against bidding.
- [ ] Capture the human partner-evidence message.
- [ ] Capture the critic's full partner gate review and recommendation.
- [ ] Capture the human nine-condition confirmation as a separate message.
- [ ] Capture the analyst's decision-record creation and the full record.
- [ ] Capture the fresh-agent question and the auditor's full reply.
- [ ] Capture the human's verbatim record confirmation.

## How to capture

- Use the Mattermost message link or a screenshot that shows the author, timestamp, and full message.
- Save raw text exports or screenshots under `examples/northstar/verification/test-runs/raw/`.
- Keep message IDs where available.
- Do not redact fictional sample data; do not include real credentials, tokens, or local paths.
- If a message is too long for one screenshot, capture it in consecutive images with the author and timestamp visible.

## What the final transcript must show

| Evidence | Why it matters |
|---|---|
| `!list-documents` before and after the decision | Proves the room document set and the record creation |
| Analyst matrix with citations | Proves the analyst extracted facts rather than repeating the oracle |
| Critic base and partner gate tables | Proves the gates and scores were posted by the critic |
| Human nine-condition message | Proves the human, not an agent, set the conditions |
| Decision record | Proves the durable artifact matches the discussion |
| Fresh-agent raw reply | Proves the auditor reconstructed the decision from room context |
| Human verbatim confirmation | Proves the record was accepted by the human owner |

## If raw evidence cannot be captured

Say so in the README and test plan. Do not describe a cleaned transcript as a platform export. The judge should be able to distinguish:

- **Raw evidence:** a platform export or screenshot with author and timestamp.
- **Cleaned transcript:** a readable reconstruction with duplicate messages removed.

The repository now contains direct Mattermost JSON exports, post IDs, membership lists, the human confirmation, the fresh-agent reply, and the boundary-probe replies in `examples/northstar/verification/test-runs/raw/`. The remaining submission gap is the demo video.
