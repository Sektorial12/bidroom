# Clean fresh-agent audit runbook

The first `room-auditor` answered in `bid-record-clean` before `room-auditor-2`, so `room-auditor-2` could copy the first reconstruction. That makes the second audit a new-agent test, but not an independent one.

Use this runbook for a clean audit.

## 1. Create a clean audit room

- Create a new Switch room, `bid-audit-clean`.
- Put only the final record content in it: the confirmed `bid-decision-record` text.
- Do **not** add `analyst-matrix`, `critic-review`, `rfp-northstar`, or `bid-policy`.
- Do **not** invite `room-auditor` or `room-auditor-2`.
- Do **not** paste any prior auditor reply.

## 2. Create a new auditor

- Create `room-auditor-3` with `room/agent-room-auditor.md`.
- Do not brief it with the answer.
- Add only `room-auditor-3` to `bid-audit-clean`.
- Confirm with `!list-agents` that the room has only the human and `room-auditor-3`.

## 3. Ask the question

```text
@room-auditor-3 What is this room for, what did it decide, and why?
List all nine conditions and open risks.
```

## 4. Capture raw evidence

Export the room with:

```text
docker exec <mattermost-container> /mattermost/bin/mmctl --local post list switch:bid-audit-clean --number 100 --show-ids --json
```

Save the export as `verification/test-runs/raw/clean-audit.json`, and a readable reply as `raw/clean-audit.md`.

## 5. What good looks like

- The auditor reconstructs the decision, owner, fallback, and 50/68 scores.
- It lists all nine human-confirmed conditions.
- It flags the open risks without copying a prior auditor.
- It does not approve or change the decision.

If the clean audit matches the record, the fresh-agent claim is independent. If it misses conditions, report the miss; do not coach it.
