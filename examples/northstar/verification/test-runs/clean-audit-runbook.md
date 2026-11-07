# Clean-room audit runbook

The first `room-auditor` answered in `bid-record-clean` before `room-auditor-2`, so `room-auditor-2` could copy the first reconstruction. That makes the second audit a new-agent test, but not an independent one.

Use this runbook for a record-only audit.

> **Captured 2026-11-07:** `bid-audit-clean` contained only the exact `bid-decision-record` and a new `room-auditor-2` session. The reply is `raw/clean-audit.md`. It recomputed base 50 and partner 68, listed all nine conditions, and flagged the record's condition-6 and attribution ambiguities. `room-auditor-3` was created but not controller-assigned, so it is not the captured auditor. This is a new-session reconstruction, not an independent third-party audit.

## 1. Create a clean audit room

- Create a new Switch room, `bid-audit-clean`.
- Paste `examples/northstar/rooms/instructions-audit.md` into the room instructions.
- Put only the exact final record content in it: `raw/exact-record.md`.
- Do **not** add `analyst-matrix`, `critic-review`, `rfp-northstar`, or `bid-policy`.
- Do **not** invite the first `room-auditor`.
- Do **not** paste any prior auditor reply.
- The captured fallback used `room-auditor-2` in this record-only room. Caption it **"new-session reconstruction; record-only room."**

## 2. Choose the auditor

Preferred:

- Create `room-auditor-3` with `examples/northstar/rooms/agent-room-auditor.md`.
- Confirm it is controller-assigned (it appears in the agent controller's assignment, not just the Switch agent list).
- Add only `room-auditor-3` to `bid-audit-clean`.

Captured fallback:

- Use `room-auditor-2` in the record-only room.
- Do not brief it with the answer.
- Add only `room-auditor-2` to `bid-audit-clean`.

Confirm the room has only the human and the chosen auditor.

## 3. Ask the question

```text
@room-auditor-3 What is this room for, what did it decide, and why?
List all nine conditions and open risks.
```

If using the fallback, replace `@room-auditor-3` with `@room-auditor-2`.

## 4. Capture raw evidence

For a bridged room, export with:

```text
docker exec <mattermost-container> /mattermost/bin/mmctl --local post list switch:bid-audit-clean --number 100 --show-ids --json
```

For an internal-only room, capture the room's message store from the local Switch database. The captured reply is already in `raw/clean-audit.md`.

## 5. What good looks like

- The auditor reconstructs the decision, owner, fallback, and 50/68 scores.
- It lists all nine human-confirmed conditions.
- It flags open risks and internal inconsistencies without copying a prior auditor.
- It does not approve or change the decision.

If the audit matches the record, say so. If it flags a conflict, report it; do not coach it. Do not call a new-session or record-only audit independent.
