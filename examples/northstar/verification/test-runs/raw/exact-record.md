# Bid Decision Record — Northstar Citizen Services Portal (RFP AVL-2026-041)

Fictional review date: **October 24, 2026**. All dates in this record are on that clock.

## Decision and human owner

| Item | Detail |
|---|---|
| Decision | Bid with partner — Meridian as prime, Helix as partner |
| Human owner / decision owner | Priya Raman |
| Status | **Conditional** — all nine confirmed conditions below must close by their due dates. Not approved and not submitted. |
| Fallback | If any condition is open at submission, No-bid |
| Authoritative source | Human confirmation message of October 24, 2026 |
| Supporting sources | `analyst-matrix`; `critic-review` (gate tables and scores) |

The human confirmation is the authoritative decision. It sets a conditional route, not an unconditional one. This record does not approve or submit the bid.

## Base and partner mandatory status

| ID | Requirement | Base (Meridian) | Partner (Meridian + Helix) | Evidence or gap |
|---|---|---|---|---|
| M1 | Current ISO 27001 certification at submission | missing | partner-covered | Base: certificate expired 2026-08-31; renewal audit December 2026. Partner: Helix certificate current through 2027 — written evidence pending (condition 4). |
| M2 | Five comparable public-sector references, last five years | missing | partner-covered | Base: four references only. Partner: Helix adds City of Norvale 2025 — fifth-reference letter pending (condition 4). |
| M3 | 24/7 priority-one support, one-hour response target | met | met | Capability §4: in-house follow-the-sun; 15-minute acknowledgment, one-hour response, four-hour workaround. |
| M4 | Plan for six-service production release within six months | conflicting | partner-covered | Plan exists, but no available Meridian architect Jan–Mar 2027 and Helix mitigation unwritten (condition 5). Human correction of October 24 set M4 to conflicting. |
| M5 | WCAG 2.2 AA for all resident-facing pages and flows | met | met | Capability §2: audited on Avalon Transit and City of Riverton; conformance reports; §2.1 testing plan. |
| M6 | Data residency in Avalon or approved Appendix A region | met | met | Capability §2: Avalon North (approved); attestation; DR in Avalon South. |

Partner statuses describe what the Helix route would cover; the underlying evidence is not yet in hand.

## Gate results — posted by the Bid Critic (verbatim)

Base = Meridian as prime. Partner = Meridian with Helix. Review date October 24, 2026. M4 is treated as conflicting: the plan exists, but it names no available Meridian architect and Helix is unwritten.

| Gate | Policy ref | Base | Partner | Evidence | Gap |
|---|---|---|---|---|---|
| G1 Mandatory requirements | §2 G1 | fail | pass_with_conditions | Analyst M1–M2, M4 conflicting; capability §2 (ISO expired), §3 (four refs), §4 (architect), §5 (Helix) | Base: M1, M2, M4 unresolved. Partner: Helix certificate, reference, delivery-lead commitment unwritten |
| G2 Minimum score | §2 G2 | fail | pass | Policy §4 formula; score table below | Base 50 < 65; partner 68 clears by 3 points |
| G3 Margin | §2 G3 | pass | pass_with_conditions | Capability §6 (base 18%, partner 11%); Human update Oct 23 (VP Finance exception recorded) | Base passes; partner written exception pending |
| G4 Capacity | §2 G4 | fail | pass_with_conditions | Capability §4 (architect unavailable Jan–Mar 2027; engagement director 20%), §5 (Helix lead) | Base fails; partner lead not committed in writing; 20% engagement director unresolved |
| G5 Deadline clarity | §2 G5 | pass_with_conditions | pass_with_conditions | Analyst matrix: Oct 28 vs Oct 30; Human update Oct 24: clarification Oct 19, response pending | Buyer response outstanding as of October 24 |
| G6 Human approval | §2 G6 | pass_with_conditions | pass_with_conditions | Policy §6; room instruction names Priya Raman as decision owner | No sign-off recorded; partner bid also needs VP of Delivery |

### Base route — gate table

| Gate | Status | Policy ref |
|---|---|---|
| G1 Mandatory requirements | fail | §2 G1 |
| G2 Minimum score | fail | §2 G2 |
| G3 Margin | pass | §2 G3 |
| G4 Capacity | fail | §2 G4 |
| G5 Deadline clarity | pass_with_conditions | §2 G5 |
| G6 Human approval | pass_with_conditions | §2 G6 |

### Partner route — gate table

| Gate | Status | Policy ref |
|---|---|---|
| G1 Mandatory requirements | pass_with_conditions | §2 G1 |
| G2 Minimum score | pass | §2 G2 |
| G3 Margin | pass_with_conditions | §2 G3 |
| G4 Capacity | pass_with_conditions | §2 G4 |
| G5 Deadline clarity | pass_with_conditions | §2 G5 |
| G6 Human approval | pass_with_conditions | §2 G6 |

## Weighted score — posted by the Bid Critic (verbatim)

| Criterion | Weight | Base (1–5) | Base wtd | Partner (1–5) | Partner wtd | Evidence |
|---|---:|---:|---:|---:|---:|---|
| Technical approach | 40% | 2 | 80 | 4 | 160 | Capability §2 (ISO), §4 (architect), §6.1; analyst M1, M4 conflicting |
| Past performance | 25% | 3 | 75 | 4 | 100 | Capability §3 (four refs), §5 (Norvale); analyst M2 |
| Price | 20% | 4 | 80 | 1 | 20 | Capability §6: 18% vs 11% margin; $2.35M vs $2.50M |
| Supplier diversity | 15% | 1 | 15 | 4 | 60 | Capability §1 (small business); §5 (Helix certified); base participation not found |
| **Weighted score (sum/5)** | **100%** | | **50** | | **68** | Policy §4 formula |

Base recalculated total: **50**. Base G2 fails (50 < 65). The result is robust: technical 3 alone gives 58, and technical 3 plus diversity 3 together give 64 — still below 65.

Posted scores are **base 50** and **partner 68**. No target or alternative numbers are used.

## Margin exception

| Item | Detail |
|---|---|
| Role | VP of Finance |
| Approver | Dana Okafor, VP of Finance |
| Approval recorded | October 23, 2026 — per `critic-review`, gate G3 and its condition 1 |
| Exception scope | Partner bid at 11% margin, below the 15% minimum stated in the capability snapshot (§5–§6) |
| Record reference | This document, `bid-decision-record`, section "Margin exception"; created October 24, 2026 |
| Document status | Written exception document pending — critic condition 1, due October 26, 2026 |
| Recording owner | Priya Raman, per the human confirmation (condition 6), due October 24, 2026 |

The exception is recorded here as the human confirmation instructs. The written VP Finance document is still pending per `critic-review`, so condition 6 is not closed by this record. Per the posted score table, price remains a 1 at 11% margin; the exception unblocks G3 and does not change the score.

## The nine confirmed conditions, owners, due dates, and statuses

| # | Condition | Owner | Due | Status as of October 24, 2026 |
|---|---|---|---|---|
| 1 | Buyer response to the deadline clarification | Priya Raman | October 26, 2026 | Open — clarification submitted October 19; response pending |
| 2 | Buyer response on Attachment C and page-limit/formatting requirements | Priya Raman | October 26, 2026 | Open — Attachment C not supplied; page limits and formatting rules not found in supplied material |
| 3 | Buyer confirmation that Helix ISO and the fifth reference satisfy the bidder-level M1/M2 requirements | Priya Raman | October 26, 2026 | Open — no buyer confirmation in hand |
| 4 | Helix ISO certificate and fifth-reference letter | Marco Chen | October 27, 2026 | Open — Helix certificate current through 2027 per capability §5; written evidence not in hand |
| 5 | Helix delivery-lead written commitment for months 1–3 | Marco Chen | October 27, 2026 | Open — lead named; not committed in writing |
| 6 | VP Finance margin exception recorded in the decision record | Priya Raman | October 24, 2026 | Recorded in this record October 24; written VP Finance document pending — not closed |
| 7 | VP of Delivery sign-off on capacity mitigation, including engagement director allocation | VP of Delivery | October 27, 2026 | Open — engagement director at 20% unresolved |
| 8 | Supplier diversity plan evidence for the 15% criterion | Priya Raman | October 27, 2026 | Open — partner diversity rests on Helix; base participation not found |
| 9 | Final go/no-go after conditions close | Priya Raman | October 27, 2026 | Open — held only after all other conditions close |

All nine are open until closed evidence is recorded. The decision is conditional until then.

## Differences from the critic review's condition list

These are shown as conflicts and are not resolved here.

| Critic condition (`critic-review`) | Confirmed condition | Difference |
|---|---|---|
| 1. Written margin exception, 11% partner bid — Dana Okafor, VP of Finance — Oct 26 | 6. Margin exception recorded in the decision record — Priya Raman — Oct 24 | Approver is Dana Okafor in both; confirmed item covers recording by Priya Raman; dates differ (Oct 26 written vs Oct 24 recorded) |
| 2. Helix ISO certificate and teaming letter — Marco Chen — Oct 27 | 4. Helix ISO certificate and fifth-reference letter — Marco Chen — Oct 27 | Teaming letter is not named in the confirmed list |
| 3. Helix City of Norvale reference and fifth-reference letter — Marco Chen — Oct 27 | 4. Helix ISO certificate and fifth-reference letter — Marco Chen — Oct 27 | City of Norvale reference is not named in a confirmed condition |
| 4. Helix delivery-lead written commitment, Jan–Mar 2027 — Marco Chen — Oct 27 | 5. Helix delivery-lead written commitment for months 1–3 — Marco Chen — Oct 27 | Same requirement, restated |
| 5. Engagement director key-role ruling or written mitigation — VP of Delivery — Oct 26 | 7. VP of Delivery sign-off on capacity mitigation, including engagement director allocation — Oct 27 | Due date moves from Oct 26 to Oct 27; ruling vs sign-off |
| 6. Buyer deadline clarification response — Priya Raman — Oct 26 | 1. Buyer response to the deadline clarification — Priya Raman — Oct 26 | Same requirement |
| 7. Attachment C and §5.4 formatting/page-limit details — Priya Raman, via analyst — Oct 26 | 2. Buyer response on Attachment C and page-limit/formatting requirements — Priya Raman — Oct 26 | Confirmed version routes it to the buyer |
| 8. Bid-with-partner approvals: pursuit lead and VP of Delivery — Oct 28 | 9. Final go/no-go after conditions close — Priya Raman — Oct 27 | VP of Delivery approval for the partner bid is not separately named |
| 9. Signed Helix subcontract and teaming terms — Marco Chen — Oct 27 | — | No counterpart in the confirmed nine |
| — | 3. Buyer confirmation on bidder-level M1/M2 — Priya Raman — Oct 26 | New; not in the critic review |
| — | 8. Supplier diversity plan evidence — Priya Raman — Oct 27 | New; not in the critic review |

## No-bid fallback

- If any condition is open at submission, the decision falls to **No-bid**.
- The submission deadline is itself unresolved: October 28, 2026, 5:00 PM per the cover and document control versus October 30, 2026, 5:00 PM per §5.1; the buyer's response is condition 1.
- The critic's recommendation stands in the record: **No-bid as prime** — base fails G1, G2, and G4 at a score of 50; the partner route is conditionally viable at 68 but not ready.

## Uncertainty

- **Attachment C (Vendor Security Questionnaire)** was not provided with the RFP (§7); it is not in supplied material, and condition 2 depends on the buyer's response.
- **Page limit and detailed formatting rules** were not found in supplied material; §5.4 gives only file-naming and format rules. Compliance cannot be confirmed until the buyer answers.
- **Pending Helix evidence:** ISO 27001 certificate, City of Norvale reference, fifth-reference letter, and delivery-lead written commitment are all still unwritten as of October 24 (conditions 4 and 5).
- **Written margin exception:** the VP Finance approval is recorded October 23, but the written document is pending (condition 6).
- **Deadline conflict unresolved:** bidding on October 28 or October 30 without the buyer's answer risks a non-compliant submission.
- **Score margin is thin:** partner 68 clears the 65 minimum by three points; the critic notes a one-step lower technical score fails G2, and price scores 1 at 11% margin.
- **Capacity:** the engagement director allocation at 20% is unresolved (condition 7).
- **Base route:** M1, M2, and M4 remain uncured in the supplied evidence; no re-scoring lifts the base route.
- **Gate status:** G6 remains pass_with_conditions exactly as posted; no sign-off is recorded there, and the partner bid also needs VP of Delivery.

## Rationale

- The Bid Critic's posted review: the base route fails G1, G2, and G4 at 50; the partner route passes G2 at 68, with G1, G3, and G4 conditional on written Helix evidence and commitments.
- The human decision of October 24, 2026: Bid with partner, conditional on the nine confirmed conditions, with No-bid as the fallback if any condition is open at submission.
- The record does not re-score, re-weight, or re-assess any gate; it reproduces the posted results and the confirmed conditions.

## Actions

| Action | Owner | Due |
|---|---|---|
| Record the VP Finance margin exception in this record and obtain the written exception | Priya Raman / Dana Okafor, VP of Finance | October 24, 2026 recorded; written document by October 26, 2026 |
| Obtain the buyer's deadline clarification response | Priya Raman | October 26, 2026 |
| Obtain the buyer's response on Attachment C and page-limit/formatting requirements | Priya Raman | October 26, 2026 |
| Obtain buyer confirmation that Helix ISO and the fifth reference meet bidder-level M1/M2 | Priya Raman | October 26, 2026 |
| Obtain the Helix ISO certificate and fifth-reference letter | Marco Chen | October 27, 2026 |
| Obtain the Helix delivery-lead written commitment for months 1–3 | Marco Chen | October 27, 2026 |
| Obtain VP of Delivery sign-off on capacity mitigation, including engagement director allocation | VP of Delivery | October 27, 2026 |
| Assemble supplier diversity plan evidence for the 15% criterion | Priya Raman | October 27, 2026 |
| Hold the final go/no-go once conditions close | Priya Raman | October 27, 2026 |
| Resolve flagged gaps: City of Norvale reference, Helix teaming letter, signed Helix subcontract and teaming terms, separate VP of Delivery approval for the partner bid | Human decision | Before final go/no-go |

## Source-fidelity note

- Gate results, gate statuses, and weighted scores are copied exactly from the Bid Critic's posted `critic-review`; no target scores from any other source were substituted.
- The nine conditions, owners, due dates, decision, human owner, and fallback are taken from the human confirmation message of October 24, 2026.
- M4 is recorded as conflicting per the human correction of October 24, 2026, and is consistent with the review's premise for both routes.
- Where the review and the human confirmation differ, both are shown and the difference is flagged.

## Synthetic data note

This is a fictional sample procurement for the Northstar exercise. The RFP, capability snapshot, suppliers, people, dates, and figures are synthetic. The review date of October 24, 2026 is fictional and is the only clock used in this record. Nothing here is a real bid, approval, or submission.

