# BidRoom — Intake Room

## Purpose

Extract the source facts for **{{project_name}}**. This room does not score, recommend, or decide.

## Members

- Human decision owner: {{decision_owner}}.
- `@bid-analyst`.

Do not add `@bid-critic` to this room. Do not add the policy document.

## Authoritative documents

Use only the source documents placed in this room. The reviewer will apply the policy in the review room.

## Scenario clock

Use the pursuit's review date. Do not use the real system date unless the project explicitly uses it.

## Analyst output

Follow the output contract in `agents/analyst.md`:

- Source facts with citations.
- Requirement table with status and evidence or gap.
- Evaluation criteria and weights.
- Conflicts and missing items.
- Document safety note.

## Handoff

The analyst posts the matrix. The human copies it into the review room as the `analyst-matrix` room document.

## Prohibitions

- Do not score or recommend.
- Do not issue a decision record.
- Do not open the policy document.
- Do not use local files, outside knowledge, or unrelated chat as evidence.
