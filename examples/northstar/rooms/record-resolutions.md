# Record resolution prompts

Use this after the three-room run if the auditor flags the same discrepancies. The goal is to make the record internally consistent without changing the human decision or inventing evidence.

## Resolutions to apply

1. **Condition 6:** keep Priya Raman as the record-keeping owner and October 24 as the record date. Add a separate action for the written exception: Dana Okafor, VP of Finance, October 27. Keep partner G3 as `pass_with_conditions` until the writing exists.
2. **Condition 9:** keep Priya Raman as the final go/no-go owner. Treat the VP of Delivery sign-off as condition 7, not a second owner of condition 9.
3. **Condition 3:** mark it as a human-added condition with no critic-table counterpart. It is not a conflict; it is an additional buyer confirmation.
4. **Condition 2:** keep the buyer-response condition (Priya Raman, October 26) and add the internal follow-up action: obtain Attachment C and page/format rules via the analyst (Priya Raman, October 27).
5. **Critic narrative vs table:** use the final partner-review table. The earlier base review's "G3 failing" line is superseded by the partner review after the October 23 recorded exception.
6. **G5 wording:** use one wording: "Cover October 28 vs §5.1 October 30; clarification filed October 19 and acknowledged; buyer response pending; no date assumed."
7. **Missing base score table:** add the base score table to `critic-review` and the record: Technical 2, Past performance 3, Price 4, Supplier diversity 1; total 50/100.
8. **VP of Delivery:** record "VP of Delivery (name not supplied)" and flag it as an ownership gap. If the human names the person, replace the role.
9. **Written evidence:** keep every condition open; no written evidence has arrived.
10. **Decision wording:** use "Bid with partner (conditional; not approved or submitted)." Do not say the bid is approved.

## Prompt to update the record

Post in `bid-record`, addressed to `@bid-analyst`:

```text
@bid-analyst Update bid-decision-record to resolve the auditor findings, using critic-review for all gates and scores. Do not open rfp-northstar or bid-policy.

1. Condition 6: keep Priya Raman, October 24, as the record-keeping owner. Add a separate action for the written VP Finance exception: Dana Okafor, October 27, open. Keep G3 partner as pass_with_conditions.
2. Condition 9: keep Priya Raman as the final go/no-go owner. The VP of Delivery sign-off is condition 7, not a second owner of condition 9.
3. Condition 3: label it as a human-added condition with no critic-table counterpart.
4. Condition 2: keep the buyer-response condition and add the internal follow-up action: obtain Attachment C and page/format rules via the analyst, Priya Raman, October 27.
5. Use the final partner-review G3 status. Note that the earlier base review's "G3 failing" line is superseded by the partner review after the October 23 recorded exception.
6. Use one G5 wording: cover October 28 vs §5.1 October 30; clarification filed October 19 and acknowledged; buyer response pending; no date assumed.
7. Add the base score table to the record: Technical 2, Past performance 3, Price 4, Supplier diversity 1; total 50/100. If critic-review is missing the table, add it there first from the critic's posted components.
8. Record "VP of Delivery (name not supplied)" and flag the ownership gap.
9. Keep every condition open; no written evidence has arrived.
10. Use "Bid with partner (conditional; not approved or submitted)."

Then quote the full updated record exactly as written. Do not summarize.
```

## Optional canonical consistency pass

Use this if the judge requires one exact record with no gate-status caveats. It changes the room record after the first confirmation, so the human must confirm again and a new auditor must be used.

```text
@bid-analyst Update bid-decision-record for canonical consistency, using critic-review for all gates and scores. Do not open rfp-northstar or bid-policy.

1. Base G6: set status fail. Evidence: the base route was not approved; the human selected the partner route.
2. Partner G2: set status pass. Evidence: 68/100 meets the 65 numeric threshold; note that the critic used pass_with_conditions for headroom.
3. Condition 6: set status done. The record entry is complete; the written VP Finance exception remains a separate action for Dana Okafor.
4. G5: use the critic's final partner-review wording exactly: "Cover October 28 vs §5.1 October 30; clarification filed October 19 and acknowledged; buyer response pending; solicitation still open." Do not call it verbatim if you normalize it.
5. G6 gap: change "Decision outstanding; no agent may approve" to "Decision recorded; no agent may approve."
6. Update the critic-review description to: "Bid Critic's posted gate results, weighted scores, reasons and conditions, copied verbatim; base score table added from the critic's posted components."

Then quote the full updated record exactly as written. Do not summarize.
```

After the analyst posts the updated record, re-post the human confirmation. For the final fresh-agent test, use a new room `bid-audit-clean` and a new `room-auditor-3`; if `room-auditor-3` is not controller-assigned, use `room-auditor-2` in the record-only room and caption it as a new-session reconstruction. See `examples/northstar/verification/test-runs/clean-audit-runbook.md`. Do not reuse the record room that contains the earlier auditor replies.

## Prompt to confirm the record

After the analyst posts the corrected record, post as the human:

```text
I confirm the corrected bid-decision-record verbatim as the human owner. The decision remains conditional, and the no-bid fallback applies if any condition is open at submission.
```

## Prompt to re-run the audit

The auditor that already saw the record is no longer fresh. Create a new auditor agent with the same `examples/northstar/rooms/agent-room-auditor.md` prompt, add it to `bid-record`, and ask:

```text
@room-auditor-2 What is this room for, what did it decide, and why?
List all nine conditions and open risks.
```

Do not brief it first. Capture the full reply.
