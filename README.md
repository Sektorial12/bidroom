# BidRoom

**Turn a 40-page RFP into a defensible bid / no-bid decision — with cited evidence, a skeptical fit review, and a human-signed record — before anyone writes a proposal.**

> **Status:** Hackathon submission in progress. The three-room source-separated run is captured. The corrected record was confirmed verbatim by the human, and a second auditor passed it with documentation caveats; the first auditor's reply was still in the room, so a clean independent audit is pending. The decision remains conditional. Direct Mattermost JSON exports, post IDs, membership lists, the second-agent reply, and the boundary probes are in `examples/northstar/verification/test-runs/raw/`. The demo video remains.
>
> **Public repository:** https://github.com/Sektorial12/bidroom

## The problem

Sales and proposal teams receive more RFPs than they can pursue well. The decision to bid is often a gut call made in email or chat under deadline pressure, without a shared evidence base or a record of why the team committed.

The cost is material:

- The average RFP win rate is roughly **45%** ([Loopio](https://loopio.com/blog/rfp-statistics-win-rates/)), and a 2026 analysis of 2.9 million proposals reports a **39%** RFP win rate in 2025 ([Focus Digital](https://focus-digital.co/average-proposal-win-rate-by-industry-and-deal-size/)).
- **87% of top performers** — teams winning 50% or more of their RFPs — use some kind of evaluation or go/no-go process ([Loopio RFP Response Trends](https://link.loopio.com/hubfs/loopio-trends-report-2025-digital.pdf)).
- A mid-size RFP takes **20–60 hours** of response work, or roughly **$2,500–$7,500 per pursuit**, win or lose ([Pelican Bid](https://www.pelicanbid.com/resources/bid-no-bid-decision)).

The practical failure mode is not a lack of summaries. It is a fragmented qualification process: mandatory requirements, capacity conflicts, commercial constraints, and unresolved questions do not arrive together at the person who must decide.

## What BidRoom does

BidRoom is a **three-room Switch workflow** for one pursuit. The human carries evidence between rooms so the analyst and critic never share a source boundary:

1. **`bid-intake`** — the Bid Analyst extracts the RFP's mandatory requirements, deadlines, evaluation criteria, contract terms, and open questions, with a source citation for every material fact. The analyst sees the RFP and capability snapshot; it does not see the bid policy.
2. **`bid-review`** — the human copies the cited matrix into the review room. The Bid Critic applies the bid policy's hard gates, scores fit against the capability evidence, and argues the strongest case against bidding. The critic sees the policy, capability snapshot, and analyst matrix; it does not see the RFP.
3. **`bid-record`** — the human copies the critic review into the record room, chooses **Bid**, **Bid with partner**, or **No-bid**, and confirms the nine conditions. The Bid Analyst writes the record from the matrix, critic review, and human decision. A fresh `room-auditor` then reconstructs the decision from the record room.

This is not a generic RFP summarizer. It is a qualification decision with:

- Source separation by room membership, not prompt-only role play.
- A human handoff that carries the matrix and critic review between rooms.
- Distinct review responsibilities and visible uncertainty.
- Human accountability and a durable decision trail.
- A deterministic validator for the structured record.

## The demo scenario

All names, dates, figures, and documents are fictional.

- **Bidder:** Meridian Digital Services.
- **Buyer:** State of Avalon, Department of Citizen Services.
- **Opportunity:** Northstar Citizen Services Portal, RFP `AVL-2026-041`.
- **Deadline conflict:** the cover says October 28, 2026; the submission instructions say October 30, 2026.
- **Mandatory gaps:** ISO 27001 expired; only four of five required references are available; the lead architect is unavailable for months 1–3.
- **Partner option:** Helix Systems can cover ISO 27001, the fifth reference, and the delivery lead.
- **Commercial tension:** the partner reduces margin to 11%, below the 15% policy minimum.
- **Human decision:** bid with partner, conditional on nine named conditions covering buyer clarifications, Helix written evidence, the VP Finance margin exception, delivery capacity, supplier diversity, and the final go/no-go.

In the final three-room run, the critic scored the base **50/100** and the partner route **68/100**. The included `decision.example.json` uses **68/100**, matching that run. The earlier single-room prototype scored the base **46/100** and the partner route **68/100**; it is kept as historical evidence. The **72/100** in `examples/northstar/verification/expected-findings.md` is the pre-run expectation, not the recorded result. The decision bands are base below 65 and partner at least 65; the partner route clears the threshold by three points, which is why the decision remains conditional.

## The agents

### Bid Analyst

- Member of `bid-intake` and `bid-record`; never a member of `bid-review`.
- Extracts facts, requirements, dates, evaluation weights, and contract terms in intake.
- Cites RFP sections.
- Marks requirements `met`, `missing`, `conflicting`, `partner-covered`, or `not assessed`.
- Flags embedded instructions as data.
- Writes the decision record from the matrix, critic review, and human decision.
- Does not open the policy, score, or recommend.

### Bid Critic

- Member of `bid-review` only; never a member of `bid-intake` or `bid-record`.
- Applies hard gates before scoring.
- Scores against the capability snapshot and analyst matrix.
- Argues at least three reasons against bidding.
- Identifies partner mitigations and conditions.
- Does not open the RFP, approve, submit, price, or contact the client.

### Room Auditor

- Joins `bid-record` only after the human confirms the record.
- Gets no task-specific briefing.
- Reconstructs the purpose, decision, rationale, all nine conditions, and open risks.
- Recomputes the posted scores and reports inconsistencies.

## Why Switch is central

Switch is the workflow boundary, not a decorative chatbot channel.

- The analyst and critic are in **different source rooms**. The analyst never sees `bid-policy`; the critic never sees `rfp-northstar`.
- The human is the only member of all three rooms. The human copies the analyst matrix into review and the critic review into record.
- The rooms hold different documents: intake has the RFP and capability; review has the policy, capability, and analyst matrix; record has the matrix, critic review, and decision record.
- The critic cannot silently read the RFP, and the analyst cannot silently read the policy. The source boundary is visible in `!list-agents` and `!list-documents`.
- The decision record is a room document that a new agent can recover without a separate briefing.
- A fresh agent joins `bid-record` with no task briefing and reconstructs the decision from room context.

The boundary is enforced by **room membership**, not per-document Switch permissions. In the configured workflow, no agent is a member of both source rooms. A single agent cannot see both the RFP and the policy unless the human deliberately adds it to both rooms, which the setup forbids. The human handoff is the cost and the control: evidence moves only when the human carries it.

To prove the boundary in the live room, run `examples/northstar/rooms/boundary-probes.md`:

- The analyst in `bid-intake` must refuse to state the policy score or margin.
- The critic in `bid-review` must refuse to quote the RFP and must say it only has the analyst matrix.
- The critic must say the analyst is not a member and that the human must relay questions.
- The analyst in `bid-record` must refuse to quote the policy.

If any probe fails, the room membership is wrong and the evidence is contaminated.

### How it differs from Switch's vendor-review example

Switch publishes a vendor purchase review use case with security, legal, and finance agents. BidRoom is different:

- It is **sell-side**: deciding whether to bid to win work, not whether to buy a vendor.
- It uses one RFP and one bid policy, and it separates them into different rooms so the analyst and critic never share a source boundary.
- It produces a weighted qualification decision with hard gates, a human handoff, and a human-owned pursuit record.

## Architecture

```text
Human pursuit lead (only member of all three rooms)
  │
  ├── bid-intake ── bid-analyst
  │     documents: rfp-northstar, capability-snapshot
  │     output: analyst-matrix
  │
  │   human carries the matrix
  │
  ├── bid-review ── bid-critic
  │     documents: bid-policy, capability-snapshot, analyst-matrix
  │     output: critic-review (full base review + partner review)
  │
  │   human carries the critic review and makes the decision
  │
  ├── bid-record ── bid-analyst
  │     documents: analyst-matrix, critic-review
  │     output: bid-decision-record
  │
  ├── human confirms the record
  │
  └── bid-record ── room-auditor (fresh agent, no briefing)
        reconstructs the decision from room context

tools/bidcheck.py → validates decision JSON, emits markdown
```

More detail: `docs/architecture.md`.

## Quickstart

Full setup: `docs/setup.md`. Recorded versions and agent settings: `docs/environment.md`.

Prerequisites:

- Switch Console 0.40.1 or newer.
- Docker running locally.
- Bundled Mattermost.
- Claude Code signed in through Switch Console.
- Python 3.11 or newer.

The workflow uses three rooms: `bid-intake`, `bid-review`, and `bid-record`. Do not merge them; the source separation is the point.

Run the validator tests (expected: **49/49 pass**):

```powershell
python -m unittest discover -s tools/tests -v
```

Validate the example decision:

```powershell
python tools/bidcheck.py examples/northstar/verification/decision.example.json --md decision-record.md
```

Expected:

```text
VALID: Northstar Citizen Services Portal | bid_with_partner | 68/100
```

## Demo video

A 90–120 second walkthrough will be linked here before submission. It shows the three rooms, the human handoff, the analyst matrix, the critic review, the human decision, the decision record, and the fresh-agent reconstruction test.

## Sample data

All files in `examples/northstar/sources/` are fictional:

- `rfp-northstar.md` — the RFP, including the deadline conflict, missing security questionnaire, and prompt-injection appendix.
- `capabilities.md` — Meridian's certifications, four references, capacity gap, partner, and margin.
- `bid-policy.md` — hard gates, minimum score, margin threshold, capacity rule, and human approval boundary.

Room files:

- `examples/northstar/rooms/instructions-intake.md`, `examples/northstar/rooms/instructions-review.md`, `examples/northstar/rooms/instructions-record.md` — room-specific instructions.
- `examples/northstar/rooms/agent-bid-analyst.md`, `examples/northstar/rooms/agent-bid-critic.md`, `examples/northstar/rooms/agent-room-auditor.md` — agent instructions.
- `examples/northstar/rooms/kickoff-message.md`, `examples/northstar/rooms/handoff-review.md`, `examples/northstar/rooms/partner-evidence.md`, `examples/northstar/rooms/decision-confirmation.md`, `examples/northstar/rooms/handoff-record.md`, `examples/northstar/rooms/audit-question.md` — chat prompts.
- `examples/northstar/rooms/boundary-probes.md` — live questions that prove the source boundary.
- `examples/northstar/rooms/record-resolutions.md` — prompts to resolve the auditor's record findings and re-run the fresh-agent test.

`examples/northstar/verification/expected-findings.md` is the test oracle. It is not attached to any Switch room.

## Validator

`tools/bidcheck.py` checks:

- Required fields and decision enum.
- Human signoff and a named human owner; agent, project-agent, and model names plus placeholders are rejected.
- Specific human approval and record references; `n/a` and placeholders are rejected.
- Agent approval/submission claims in the approval reference, rationale, or uncertainty are rejected.
- The data note rejects real-client-data and confidential-data claims.
- Requirement statuses and evidence; exactly M1–M6.
- Base requirements must describe Meridian alone; `partner_covered` belongs only in the decision path.
- G1 rejects missing, conflicting, or not-assessed mandatory requirements.
- Exactly G1–G6 in both the base and decision-path gate tables.
- Four weighted criteria; weights sum to 100.
- Total score matches the weighted calculation.
- A bid decision requires a score of at least 65.
- G2 must align with the score; G1 cannot pass while a mandatory requirement is missing, conflicting, or not assessed; G3 cannot pass below the margin minimum.
- Base G2 must align with the structured base score.
- Failed gates block a bid unless a complete human gate exception exists.
- Gate exceptions require a known gate, approver, reason, date, and record reference.
- Margin below policy requires a recorded exception.
- Bid decisions require a human approval reference.
- Bid-with-partner decisions require a no-bid fallback.
- Base and partner gate tables are validated and rendered separately.
- Conditions and actions have substantive text, owners, due dates, and optional open/done statuses.
- Bid-with-partner records must cover the nine named condition categories, not just nine placeholder rows.
- Unknown top-level fields are rejected.
- The data note affirms synthetic data and rejects negative claims.

Exit codes: `0` valid, `1` validation errors, `2` usage/IO error.

Schema: `tools/decision.schema.json`.

## Tests

Current validator result: **49/49 pass**.

Covered:

- Valid partner and no-bid decisions.
- Markdown output.
- Missing evidence.
- Gate override.
- Weight errors.
- Missing human signoff.
- Missing margin exception.
- Missing conditions.
- Score mismatch.
- Low bid below the 65-point minimum.
- Mandatory requirement missing while G1 is marked pass.
- Missing or fake gate IDs; missing mandatory requirement IDs.
- Base G1/G2/G3/G4 inconsistent with the base path.
- G1 pass_with_conditions with a missing requirement; final G4 pass with M4 missing.
- Non-policy scoring weights and self-asserted margin policy.
- Fewer than nine conditions, or nine placeholders missing the named categories.
- Agent, project-agent, and model names as the human owner, approver, or condition owner.
- Agent approval/submission claims in the approval reference, rationale, or uncertainty.
- Real-client-data claims in the synthetic-data note.
- Placeholder approval and margin references.
- Base-path `partner_covered` requirements.
- Unknown score criteria.
- Margin approver is not the VP of Finance.
- Gate exception with an unauthorized role or no record reference.
- Negative or contradictory data note.
- Incomplete gate exception.
- Non-synthetic data note.
- Invalid decision.
- Invalid JSON.
- Missing file.

The **three-room run** completed: the intake, review, and record rooms used separate document and agent sets; the human carried the matrix and critic review; the record was corrected, confirmed verbatim, and audited by a second agent. That second agent shared the room with the first auditor's reconstruction, so the clean independent audit is still pending. The auditor recomputed 50/68 and passed the record with documentation caveats. The no-bid alternate remains untested. Clean-clone verification passed. Details are tracked in `docs/test-plan.md`.

Live evidence:

- `examples/northstar/verification/test-runs/three-room-run.md` — readable transcript of the final three-room run, including `!list-agents`, `!list-documents`, the correction, and the second audit.
- `examples/northstar/verification/test-runs/raw/` — direct Mattermost JSON exports, the user-ID map, `membership.md`, `fresh-agent.md`, `human-confirmation.md`, `boundary-probes.md`, `transcript.md`, and `post-index.csv` with post IDs.
- `examples/northstar/verification/test-runs/live-run-clean.md` — cleaned transcript of the historical single-room prototype.
- `examples/northstar/verification/test-runs/raw-evidence-checklist.md` — what to capture for raw membership and screenshot evidence.
- `examples/northstar/verification/test-runs/clean-audit-runbook.md` — how to run an independent fresh-agent audit in a clean room.
- `examples/northstar/verification/test-runs/exact-record-export.md` — how to capture the live record verbatim.
- `examples/northstar/verification/test-runs/clean-clone.md` — clean-clone validator results.
- `examples/northstar/verification/decision-record.three-room.md` — reconstructed canonical record export from the three-room run; the room document itself was not exported verbatim. It includes the second agent's caveats and the clean-audit gap.
- `examples/northstar/verification/decision-record.live.md` — historical single-room prototype record.

The Markdown transcripts are readable renderings; the direct Mattermost JSON exports and post IDs are in `examples/northstar/verification/test-runs/raw/`. The boundary probes are captured in `raw/boundary-probes.md`.

## Limitations and safety

- This is a hackathon prototype, not a production bid-management, legal, or procurement system.
- It checks only the materials supplied in the rooms.
- It does not verify the truth of the RFP or capability evidence.
- It does not generate a proposal, set a price, or submit a bid.
- No agent may approve, submit, price, sign, or contact a client.
- The source separation is room membership, not per-document permissions. If the human adds both source agents to the same room, the boundary is broken and the evidence is contaminated.
- The human is the handoff. The critic cannot ask the analyst directly; the human must relay missing-fact questions.
- The scoring model is illustrative and must be calibrated for a real organization.
- All sample data is fictional.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── examples/northstar/sources/
├── examples/northstar/rooms/
├── examples/northstar/verification/
├── tools/
└── docs/
```

## Hackathon

Built for the **Flip the Switch Hackathon 2026** — **Best Business Workflow** track.

Repository: https://github.com/Sektorial12/bidroom

The workflow uses three Switch rooms to separate RFP evidence from bid policy, with a human carrying the handoff and owning the decision at the end.

## License

MIT. See `LICENSE`.
