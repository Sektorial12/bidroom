# Bid Decision Record — Northstar Citizen Services Portal

**RFP:** AVL-2026-041 — State of Avalon, Department of Citizen Services  
**Decision:** Bid with partner  
**Human owner:** Priya Raman, Bid Director  
**Decision date:** October 24, 2026  
**Source:** historical single-room prototype run; the final three-room record is `decision-record.three-room.md`.  
**Partner:** Helix Systems; pursuit partner manager Marco Chen  
**Human approval reference:** Mattermost room message `sw_fa7ce0694d4b069dbd05c79ffbc747ea`, October 24, 2026 (fictional)  
**Record status:** Human decision, nine-condition confirmation, and verbatim record confirmation recorded; conditions open as noted. Scores are the Bid Critic's posted results.  
**Data status:** Fictional sample data. This is not a real procurement decision.

## 1. Decision and human owner

| Field | Value |
|---|---|
| Decision | Bid with partner |
| Human owner | Priya Raman, Bid Director |
| Partner | Helix Systems; pursuit partner manager Marco Chen |
| Decision source | Human room message, October 24, 2026 (fictional) |
| Fallback | No-bid if any condition is open at submission |

The decision is **conditional and not executable** until all nine conditions in §6 close. No agent approved, priced, submitted, or contacted the buyer.

## 2. Mandatory requirements — base and partner

| ID | Requirement | RFP ref | Base status | Partner status | Evidence or gap |
|---|---|---|---|---|---|
| M1 | Current ISO 27001 certification at submission | §3 | missing | partner-covered | Meridian ISO expired 2026-08-31; renewal December 2026 (capability §2). Helix current to 2027 (capability §5); certificate and teaming agreement pending. |
| M2 | Five comparable public-sector references, last five years | §3 | missing | partner-covered | Meridian has four references (capability §3). Helix adds City of Norvale 2025 (capability §5); fifth-reference letter pending. |
| M3 | 24/7 priority-one support, one-hour response target | §3 | met | met | Meridian in-house follow-the-sun tier 1/2; sample P1 SLA one-hour response (capability §4). |
| M4 | Production release for six services within six months | §3 | conflicting | partner-covered | Meridian architect unavailable January–March 2027 (capability §4). Helix delivery lead available (capability §5); written commitment pending. |
| M5 | WCAG 2.2 AA for all resident-facing pages and flows | §3 | met | met | Meridian audited on two public-sector projects; conformance reports and testing plan (capability §2, §2.1). |
| M6 | Resident data in Avalon or an approved cloud region | §3; App. A.1 | met | met | Avalon North, a region listed in Appendix A; attestation and architecture available (capability §2). |

## 3. Gate results — Bid Critic's posted results

| Gate | Base status | Partner status | Evidence or gap |
|---|---|---|---|
| G1 Mandatory requirements | fail | pass_with_conditions | M1, M2 and M4 shortfalls; Helix coverage named; ISO certificate, fifth-reference letter and teaming agreement pending. |
| G2 Minimum score ≥65 | fail | pass | Base 46/100; partner 68/100; partner 3 points above threshold. |
| G3 Margin ≥15% | pass | pass_with_conditions | Base 18%; partner 11%; VP Finance exception recorded October 23 by Dana Okafor; written exception pending. |
| G4 Capacity ≥50% first 90 days | fail | pass_with_conditions | Architect unavailable January–March 2027; engagement director at 20%; Helix lead available but uncommitted in writing. |
| G5 Deadline clarity | pass_with_conditions | pass_with_conditions | Cover October 28 vs §5.1 October 30; clarification submitted October 19 and acknowledged; response pending. |
| G6 Human approval | fail | pass_with_conditions | Base route not approved; partner decision recorded. VP of Delivery sign-off and final go/no-go pending. |

These gate statuses reflect the Bid Critic's posted results, with one final-record correction: base G6 is **fail** because the human selected the partner route and no base bid was approved. The analyst did not open the policy document.

## 4. Weighted score — Bid Critic's posted results

Formula per bid-policy §4: `sum(score × weight) / 5`.

| Criterion | Weight | Base score | Base score × weight | Partner score | Partner score × weight |
|---|---:|---:|---:|---:|---:|
| Technical approach | 40% | 2 | 80 | 4 | 160 |
| Past performance | 25% | 3 | 75 | 4 | 100 |
| Price | 20% | 3 | 60 | 1 | 20 |
| Supplier diversity | 15% | 1 | 15 | 4 | 60 |
| **Total** | **100%** | — | **46/100** | — | **68/100** |

The base score is 19 points below the 65 threshold. The partner score clears the threshold by 3 points. The partner price score stays at 1 because the 11% margin remains below the 15% target even after the VP Finance exception is recorded.

## 5. Margin exception

| Field | Value |
|---|---|
| Role | VP of Finance |
| Approver | Dana Okafor, VP of Finance |
| Date | October 23, 2026 |
| Record reference | Human update messages `sw_f28706a6fbe4cc3727ea2af810360b7a` and `sw_6417545a38dff47f3e55275fe8947112`, October 23–24, 2026 (fictional) |
| Status | Exception recorded; written exception pending |

The partner margin is 11% against a 15% policy minimum (capability §6).

## 6. Nine confirmed conditions

| # | Condition | Owner | Due | Status |
|---|---|---|---|---|
| 1 | Buyer response to the deadline clarification | Priya Raman | October 26 | open |
| 2 | Buyer response on Attachment C and page-limit/formatting requirements | Priya Raman | October 26 | open |
| 3 | Buyer confirmation that Helix ISO and the fifth reference satisfy bidder-level M1/M2 | Priya Raman | October 26 | open |
| 4 | Helix ISO certificate and fifth-reference letter | Marco Chen | October 27 | open |
| 5 | Helix delivery-lead written commitment for months 1–3 | Marco Chen | October 27 | open |
| 6 | VP Finance margin exception recorded in the decision record | Priya Raman | October 24 | recorded in this record; written exception pending |
| 7 | VP of Delivery sign-off on capacity mitigation, including engagement director allocation | VP of Delivery | October 27 | open |
| 8 | Supplier diversity plan evidence for the 15% criterion | Priya Raman (accountable); Marco Chen (Helix evidence) | October 27 | open |
| 9 | Final go/no-go after conditions close | Priya Raman | October 27 | open |

## 7. No-bid fallback

If any condition is open at submission, the outcome is **No-bid**.

## 8. Rationale

The base case is not viable. It fails three hard gates: G1 because ISO 27001 expired on 2026-08-31 and only four of five references are available; G2 because the base score is 46/100 against a 65 minimum; and G4 because the lead solution architect is unavailable January–March 2027, overlapping the six-month delivery window. The base route also has no human approval: base G6 is fail because the human selected the partner route. The 18% base margin passes G3, but margin alone does not offset the mandatory, score, and capacity failures.

The partner route is the only path that clears G2. Helix Systems covers M1, M2, and M4 with an ISO certificate current to 2027, the City of Norvale 2025 reference, and a delivery lead for months 1–3. That raises the score to 68/100. The route is still marginal: it clears the threshold by three points, the 11% partner margin is below the 15% policy minimum and needs a written VP Finance exception, the deadline conflict is unresolved, and the Helix evidence is not yet in writing.

The human owner therefore chose **Bid with partner**, conditional on the nine named conditions, with a **No-bid** fallback if any condition remains open at submission. The Bid Critic initially recommended no-bid on the base case; the partner route became conditional, not approved, only after the human supplied the partner evidence and margin-exception status. No gate is closed today.

## 9. Actions

| Action | Owner | Due | Status |
|---|---|---|---|
| Submit deadline clarification through the buyer portal | Priya Raman | October 19 | done |
| Request Attachment C and page-limit/formatting requirements | Priya Raman | October 19 | done |
| Request written buyer confirmation of partner coverage for M1/M2 | Priya Raman | October 19 | done |
| Obtain Helix ISO certificate and fifth-reference letter | Marco Chen | October 27 | open |
| Obtain Helix delivery-lead written commitment for months 1–3 | Marco Chen | October 27 | open |
| Obtain the written VP Finance margin exception | Dana Okafor | October 27 | open |
| Obtain VP of Delivery ruling on engagement-director key-role status, or written mitigation | VP of Delivery | October 27 | open |
| Request Helix supplier-diversity certificate and plan evidence | Marco Chen | October 27 | open |
| Compile the supplier diversity plan evidence for the bid | Priya Raman | October 27 | open |
| Record the final go/no-go after conditions close | Priya Raman | October 27 | open |

## 10. Uncertainty and open items

- **Deadline:** the RFP cover and Document control say October 28, 2026; §5.1 says October 30, 2026, 5:00 PM Avalon Time. The clarification was submitted October 19 and acknowledged; the buyer response is pending. No date is assumed.
- **Attachment C:** the Vendor Security Questionnaire is required for submission but was not provided with the RFP. Buyer response is requested under condition 2.
- **Page limit and formatting:** no page limit, font, or detailed formatting rules are stated in the supplied material. Buyer response is requested under condition 2.
- **Helix evidence:** ISO certificate, fifth-reference letter, signed teaming agreement, and delivery-lead written commitment are pending. Partner coverage is not assumed to be accepted by the buyer; condition 3 seeks confirmation that it satisfies bidder-level M1/M2.
- **Margin exception:** the exception is recorded in this record, but the written VP Finance exception has not been supplied.
- **Capacity:** the engagement director is at 20% allocation. The VP of Delivery must confirm whether this is a key role or provide a written mitigation under condition 7.
- **Supplier diversity:** Meridian has no diverse-supplier evidence in the snapshot. Helix holds a certification and must supply the plan evidence behind the 15% criterion. Priya Raman is accountable for the condition; Marco Chen owns the Helix evidence request.
- **Score headroom:** the partner route is 3 points above the minimum. Any slippage in Helix evidence or reference comparability can drop it below 65.
- **Record confirmation:** the human confirmed the nine conditions and this corrected record verbatim on the October 24, 2026 fictional review clock.

## 11. Approvals and evidence status

| Item | Status | Evidence |
|---|---|---|
| Human decision — Bid with partner | recorded | Human room message, October 24, 2026 (fictional) |
| Human confirmation of the full nine-condition set | recorded | Human room message, October 24, 2026 (fictional) |
| Human owner — Priya Raman | recorded | Human room message |
| VP Finance margin exception, October 23, 2026 | reported by human owner | Written exception not in supplied material |
| VP of Delivery sign-off | not recorded | Required by bid-policy §6 for bid with partner |
| Helix ISO certificate | pending | Capability §5 states certificate available; no copy supplied |
| Helix fifth-reference letter | pending | Capability §5 states reference available; no letter supplied |
| Helix delivery-lead commitment | pending | Capability §5 states available; no written commitment supplied |
| Six-service delivery plan | recorded | Capability §6.1 |
| Buyer deadline confirmation | pending | Clarification filed October 19; response pending |
| Record verbatim confirmation | recorded | Human review of the corrected record, October 24, 2026 (fictional review clock) |

## 12. Data confirmation and record sources

All names, organisations, dates, prices, margins, certifications, references, and requirements in this record are fictional sample data created for the BidRoom demo. This record is not a real procurement decision.

Sources:

- RFP facts: `rfp-northstar` (sections cited above).
- Meridian and Helix capability: `capability-snapshot` (sections cited above).
- Gate results and scores: Bid Critic's posted tables in the room.
- Decision, conditions, and margin exception: human update messages in the room.
- Policy document: outside the analyst's evidence scope; the analyst did not open or cite it.
