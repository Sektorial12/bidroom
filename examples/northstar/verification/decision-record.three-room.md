# Bid Decision Record — Northstar Citizen Services Portal

**RFP:** AVL-2026-041 — State of Avalon, Department of Citizen Services  
**Decision:** Bid with partner (conditional)  
**Human owner:** Priya Raman, Bid Director  
**Decision date:** October 24, 2026 (fictional review clock)  
**Partner:** Helix Systems; pursuit partner manager Marco Chen  
**Source:** three-room run, `bid-record`. Run metadata: 2026-11-06; this is not part of the fictional October 24 decision clock. This export is reconstructed from the corrected record and the second auditor's findings; it is not the exact room text.  
**Record status:** Human decision, nine conditions, and corrected record confirmed verbatim; second agent passed it with documentation caveats, but the first auditor's reply was still in the room, so a clean independent audit is pending. This export preserves the human-confirmed live statuses; the optional canonical pass in `examples/northstar/rooms/record-resolutions.md` has not been applied. The decision is conditional and not approved or submitted.  
**Data status:** Fictional sample data. This is not a real procurement decision.

## 1. Decision and human owner

| Field | Value |
|---|---|
| Decision | Bid with partner — conditional, not approved or submitted |
| Human owner | Priya Raman, Bid Director |
| Partner | Helix Systems; pursuit partner manager Marco Chen |
| Decision source | Human nine-condition confirmation in `bid-record`, October 24, 2026 (fictional) |
| Fallback | No-bid if any condition is open at submission |

The critic's recommendation was **base: no-bid; partner: conditional, not yet a bid**. The human selected the partner route on that conditional basis. No agent approved, priced, submitted, or contacted the buyer.

## 2. Mandatory requirements — base and partner

| ID | Requirement | RFP ref | Base status | Partner status | Evidence or gap |
|---|---|---|---|---|---|
| M1 | Current ISO 27001 certification at submission | §3 | missing | partner-covered | Meridian ISO expired 2026-08-31; renewal audit December 2026 (capability §2). Helix current to 2027 (capability §5); certificate and written partner commitment pending. |
| M2 | Five comparable public-sector references, last five years | §3 | missing | partner-covered | Meridian has four references (capability §3). Helix adds City of Norvale 2025 (capability §5); fifth-reference letter pending. |
| M3 | 24/7 priority-one support, one-hour response target | §3; §2.6 | met | met | Meridian in-house follow-the-sun tier 1/2; P1 15-minute acknowledgment, one-hour response (capability §4). |
| M4 | Production release for six services within six months | §3; §2.7 | conflicting | partner-covered | Meridian lead architect unavailable January–March 2027 (capability §4). Helix delivery lead available (capability §5); written commitment pending. |
| M5 | WCAG 2.2 AA for all resident-facing pages and flows | §3; §2.4 | met | met | Meridian audited on two public-sector projects; conformance reports and testing plan (capability §2, §2.1). |
| M6 | Resident data in Avalon or an approved cloud region | §3; App. A.1 | met | met | Avalon North, a region listed in Appendix A; attestation and architecture available (capability §2). |

## 3. Gate results — critic's posted results

| Gate | Base status | Partner status | Evidence or gap |
|---|---|---|---|
| G1 Mandatory requirements | fail | pass_with_conditions | M1, M2 and M4 shortfalls; Helix coverage named; ISO certificate, fifth-reference letter and written partner commitment pending. |
| G2 Minimum score ≥65 | fail | pass_with_conditions | Base 50/100; partner 68/100; the numeric threshold is met. The critic posted `pass_with_conditions` because the route has only three points of headroom. |
| G3 Margin ≥15% | pass | pass_with_conditions | Base 18%; partner 11%; VP Finance exception recorded October 23 by Dana Okafor; written exception pending. |
| G4 Capacity ≥50% first 90 days | fail | pass_with_conditions | Architect unavailable January–March 2027; engagement director at 20%; Helix lead available but uncommitted in writing. |
| G5 Deadline clarity | pass_with_conditions | pass_with_conditions | Cover October 28 vs §5.1 October 30; clarification submitted October 19 and acknowledged; response pending; no date assumed. |
| G6 Human approval | pass_with_conditions | pass_with_conditions | Decision owner Priya Raman; human decision recorded. Base route was not selected. VP of Delivery sign-off and final go/no-go pending. |

The base G6 status is the critic's posted `pass_with_conditions`; the base route itself was not approved. This export preserves that posted status rather than normalizing it.

## 4. Weighted score — critic's posted results

Formula per bid-policy §4: `sum(score × weight) / 5`.

| Criterion | Weight | Base score | Base score × weight | Partner score | Partner score × weight |
|---|---:|---:|---:|---:|---:|
| Technical approach | 40% | 2 | 80 | 4 | 160 |
| Past performance | 25% | 3 | 75 | 4 | 100 |
| Price | 20% | 4 | 80 | 1 | 20 |
| Supplier diversity | 15% | 1 | 15 | 4 | 60 |
| **Total** | **100%** | — | **50/100** | — | **68/100** |

The base score is 15 points below the 65 threshold. The partner score clears the threshold by 3 points. The partner price score stays at 1 because the 11% margin remains below the 15% target even after the exception is recorded.

## 5. Margin exception

| Field | Value |
|---|---|
| Role | VP of Finance |
| Approver | Dana Okafor, VP of Finance |
| Date | October 23, 2026 |
| Record reference | Human update in `bid-review`, October 23–24, 2026 (fictional) |
| Status | Exception recorded; written exception pending |

The partner margin is 11% against a 15% policy minimum (capability §6). The gate remains `pass_with_conditions` until the written exception is issued.

## 6. Nine confirmed conditions

| # | Condition | Owner | Due | Status |
|---|---|---|---|---|
| 1 | Buyer response to the deadline clarification | Priya Raman | October 26 | open — buyer response pending |
| 2 | Buyer response on Attachment C and page-limit/formatting requirements | Priya Raman | October 26 | open — buyer response pending |
| 3 | Buyer confirmation that Helix ISO and the fifth reference satisfy bidder-level M1/M2 (human-added; no critic-table counterpart) | Priya Raman | October 26 | open — buyer confirmation pending |
| 4 | Helix ISO certificate and fifth-reference letter | Marco Chen | October 27 | open — documents not received |
| 5 | Helix delivery-lead written commitment for months 1–3 | Marco Chen | October 27 | open — commitment not received |
| 6 | VP Finance margin exception recorded in the decision record | Priya Raman | October 24 | open — record entry done; written countersignature tracked as a separate action |
| 7 | VP of Delivery sign-off on capacity mitigation, including engagement director allocation | VP of Delivery (name not supplied) | October 27 | open — sign-off pending |
| 8 | Supplier diversity plan evidence for the 15% criterion | Priya Raman | October 27 | open — evidence pending |
| 9 | Final go/no-go after conditions close | Priya Raman | October 27 | open — scheduled |

## 7. No-bid fallback

If any condition is open at submission, the outcome is **No-bid**.

## 8. Rationale

The base case is not viable. It fails G1 because ISO 27001 expired on 2026-08-31 and only four of five references are available; G2 because the base score is 50/100 against a 65 minimum; and G4 because the lead solution architect is unavailable January–March 2027, overlapping the six-month delivery window. The 18% base margin passes G3, but margin alone does not offset the mandatory, score, and capacity failures.

The partner route is the only path that clears G2. Helix Systems covers M1, M2, and M4 with an ISO certificate current to 2027, the City of Norvale 2025 reference, and a delivery lead for months 1–3. That raises the score to 68/100. The route is still marginal: it clears the threshold by three points, the 11% partner margin is below the 15% policy minimum and needs a written VP Finance exception, the deadline conflict is unresolved, and the Helix evidence is not yet in writing.

The human owner therefore chose **Bid with partner**, conditional on the nine named conditions, with a **No-bid** fallback if any condition remains open at submission. No gate is closed today.

## 9. Actions

| Action | Owner | Due | Status |
|---|---|---|---|
| Submit deadline clarification through the buyer portal | Priya Raman | October 19 | done |
| Request Attachment C and page-limit/formatting requirements | Priya Raman | October 19 | done |
| Request written buyer confirmation of partner coverage for M1/M2 | Priya Raman | October 19 | done |
| Obtain Helix ISO certificate and fifth-reference letter | Marco Chen | October 27 | open |
| Obtain Helix delivery-lead written commitment for months 1–3 | Marco Chen | October 27 | open |
| Obtain the written VP Finance margin exception | Dana Okafor | October 27 | open |
| Obtain Attachment C and page/format rules via the analyst | Priya Raman | October 27 | open |
| Obtain VP of Delivery ruling on engagement-director key-role status, or written mitigation | VP of Delivery (name not supplied) | October 27 | open |
| Collect supplier diversity plan evidence for the 15% criterion | Priya Raman | October 27 | open |
| Record the final go/no-go after conditions close | Priya Raman | October 27 | open |

## 10. Second audit findings — documentation caveats

`room-auditor-2` confirmed the live record is internally coherent and the arithmetic is correct. This export preserves the human-confirmed statuses and does not apply the optional canonical pass.

**Caveats preserved from the live record:**

1. **G5 row is not verbatim.** The record uses one human-directed wording, a third wording different from both critic tables. It is disclosed in the row, but it is a substitution, not a copy.
2. **Critic review contradicts itself on G3 partner.** The earlier base narrative says partner 68/100 "with G3 failing"; the later table says `pass_with_conditions`. The record treats the table as current, as instructed.
3. **G6 wording is stale.** The live record's G6 row says "Decision outstanding" even though the decision is recorded. The posted status is `pass_with_conditions`; the row text should be read with that in mind.
4. **Condition 6 is labelled open** although the record entry is done; the written VP Finance countersignature is tracked as a separate action.
5. **Condition 3 remains a divergence:** no critic-table counterpart, and no buyer confirmation that Helix evidence satisfies bidder-level M1/M2.
6. **`critic-review` description says "copied verbatim"** but the base score table was added later by the analyst from the critic's posted components. The numbers agree with the critic's 250 ÷ 5 line.
7. **No named VP of Delivery**; condition 7's owner is a role.
8. **Policy approval gap:** the bid policy requires the pursuit lead plus the VP of Delivery for a bid-with-partner decision. The record captures the VP of Delivery capacity sign-off as condition 7 but not a separate VP approval of the bid-with-partner decision. This remains an open approval gap.
9. **No page limit, format rules, file-size limit, or Attachment C content** in the room.
10. **No evidence any condition has closed.**

The record is confirmed and conditional; these are live-record disclosures and approval gaps, not a post-confirmation normalization.

## 11. Uncertainty and open items

- **Deadline:** the RFP cover says October 28, 2026; §5.1 says October 30, 2026, 5:00 PM Avalon Time. Clarification submitted October 19 and acknowledged; buyer response pending. No date is assumed.
- **Attachment C:** required for submission but not provided; buyer response requested under condition 2.
- **Page limit and formatting:** not found in supplied material; buyer response requested under condition 2.
- **Helix evidence:** ISO certificate, fifth-reference letter, written partner commitment, and delivery-lead written commitment are pending. No teaming agreement is in the supplied evidence.
- **Margin exception:** recorded, but the written exception has not been supplied.
- **Capacity:** engagement director at 20%; VP of Delivery must confirm key-role status or provide written mitigation.
- **Policy approval gap:** the policy requires the pursuit lead plus the VP of Delivery for a bid-with-partner decision. The record captures the VP of Delivery capacity sign-off as condition 7, but not a separate VP approval of the bid-with-partner decision.
- **Supplier diversity:** Meridian has no diverse-supplier evidence; Helix certification and plan evidence required.
- **Score headroom:** the partner route is 3 points above the minimum; any slippage can drop it below 65.
- **Record confirmation:** the human confirmed the nine conditions and the corrected record verbatim at the run review. This is run metadata, not part of the fictional October 24 decision clock.
- **Fresh-agent audit:** `room-auditor-2` audited the corrected record and passed it with the documentation caveats in §10. The first auditor is historical.

## 12. Data confirmation and record sources

All names, organisations, dates, prices, margins, certifications, references, and requirements in this record are fictional sample data created for the BidRoom demo. This record is not a real procurement decision.

Sources:

- RFP facts: `analyst-matrix` (sections cited above).
- Meridian and Helix capability: `capability-snapshot` (sections cited above).
- Gate results and scores: `critic-review`.
- Decision, conditions, and margin exception: human messages in `bid-record`.
- Auditor findings: `room-auditor-2` reply in `bid-record` (run metadata 2026-11-06; not part of the fictional decision clock).
