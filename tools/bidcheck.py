#!/usr/bin/env python3
"""Legacy Northstar conformance adapter.

The generic, policy-driven engine is in ``src/bidroom``. This adapter keeps the
original `python tools/bidcheck.py <decision.json>` command working for the
Northstar example and its 49 conformance tests.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

DECISIONS = {"bid", "bid_with_partner", "no_bid"}
REQUIREMENT_STATUSES = {
    "met",
    "missing",
    "conflicting",
    "partner_covered",
    "not_assessed",
}
GATE_STATUSES = {"pass", "pass_with_conditions", "fail"}
ITEM_STATUSES = {"open", "done", "blocked", "cancelled"}
SCORE_KEYS = ("technical", "past_performance", "price", "supplier_diversity")
REQUIRED_FIELDS = (
    "pursuit",
    "rfp",
    "decision",
    "human_owner",
    "human_signoff",
    "decision_date",
    "data_note",
    "requirements",
    "base_requirements",
    "scores",
    "base_scores",
    "total_score",
    "base_total_score",
    "base_margin_percent",
    "base_gates",
    "gates",
    "margin_percent",
    "policy_min_margin_percent",
    "conditions",
    "actions",
    "rationale",
    "uncertainty",
)

EXPECTED_GATES = {"G1", "G2", "G3", "G4", "G5", "G6"}
EXPECTED_REQUIREMENTS = {"M1", "M2", "M3", "M4", "M5", "M6"}
EXPECTED_WEIGHTS = {
    "technical": 40,
    "past_performance": 25,
    "price": 20,
    "supplier_diversity": 15,
}
POLICY_MIN_MARGIN = 15.0
PLACEHOLDER_VALUES = {
    "",
    "n/a",
    "na",
    "none",
    "null",
    "tbd",
    "todo",
    "placeholder",
    "unknown",
    "not set",
    "not applicable",
}
AGENT_MARKERS = (
    "bid-analyst",
    "bid-critic",
    "room-auditor",
)
AGENT_WORD_PATTERN = re.compile(
    r"\b(bid analyst|bid critic|room auditor|analyst|critic|auditor|"
    r"agent|bot|assistant|system|claude|gpt|openai|autogpt|llm|model|"
    r"deepseek|gemini|copilot|chatgpt|anthropic|openrouter|opencode|cursor|"
    r"windsurf|qwen|llama|mistral|perplexity|grok|sonnet|opus|haiku)\b",
    re.IGNORECASE,
)
AGENT_APPROVAL_PATTERN = re.compile(
    r"(?<!no )(?<!not )(?<!never )"
    r"\b(bid analyst|bid critic|room auditor|analyst|critic|auditor|"
    r"agent|bot|assistant|ai|model|claude code|claude|gpt|openai|autogpt)\b"
    r"\s+(approved|approves|submitted|submits|signed|authorized|authorised)\b"
    r"|(?<!no )(?<!not )(?<!never )"
    r"\b(approved|approves|submitted|submits|signed|authorized|authorised)\b"
    r".{0,40}\bby\s+(the\s+)?(bid analyst|bid critic|room auditor|analyst|critic|"
    r"auditor|agent|bot|assistant|ai|model|claude code|claude|gpt|openai|autogpt)\b",
    re.IGNORECASE,
)
CONDITION_CATEGORIES = (
    ("deadline clarification", (("deadline", "clarification"), ("deadline", "response"))),
    (
        "Attachment C and page-limit/formatting",
        (("attachment c",), ("page-limit", "formatting"), ("page limit", "formatting")),
    ),
    (
        "buyer confirmation of partner coverage",
        (
            ("buyer confirmation", "helix"),
            ("buyer confirms", "helix"),
            ("bidder-level", "m1"),
        ),
    ),
    (
        "Helix ISO certificate and fifth reference",
        (
            ("iso", "certificate"),
            ("iso", "certification"),
            ("fifth-reference", "letter"),
            ("fifth reference", "letter"),
        ),
    ),
    (
        "Helix delivery-lead commitment",
        (
            ("delivery", "lead", "commitment"),
            ("delivery-lead", "commitment"),
            ("delivery lead", "commitment"),
        ),
    ),
    ("VP Finance margin exception", (("margin", "exception"), ("vp finance", "exception"))),
    (
        "VP of Delivery capacity sign-off",
        (
            ("vp of delivery", "capacity"),
            ("delivery", "sign-off", "engagement director"),
            ("vp of delivery", "engagement director"),
        ),
    ),
    ("supplier diversity evidence", (("supplier diversity",), ("diversity", "plan"))),
    (
        "final go/no-go",
        (("go/no-go",), ("go / no-go",), ("final", "no-bid"), ("final", "no bid")),
    ),
)
ALLOWED_TOP_LEVEL = set(REQUIRED_FIELDS) | {
    "human_approval_ref",
    "fallback",
    "gate_exceptions",
    "margin_exception",
}

DECISION_LABELS = {
    "bid": "Bid",
    "bid_with_partner": "Bid with partner",
    "no_bid": "No-bid",
}


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_iso_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def _escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _present(value: Any) -> bool:
    return bool(str(value or "").strip())


def _normalise(value: Any) -> str:
    return " ".join(str(value or "").strip().lower().split())


def _is_placeholder(value: Any) -> bool:
    text = _normalise(value)
    return (
        text in PLACEHOLDER_VALUES
        or text.startswith("placeholder")
        or text.startswith("todo")
    )


def _looks_like_agent(value: Any) -> bool:
    text = _normalise(value)
    return any(marker in text for marker in AGENT_MARKERS) or bool(
        AGENT_WORD_PATTERN.search(text)
    )


def _is_meaningful_reference(value: Any) -> bool:
    text = _normalise(value)
    return (
        not _is_placeholder(text)
        and len(text) >= 8
        and any(character.isalnum() for character in text)
    )


def _matches_condition(text: str, alternatives: tuple[tuple[str, ...], ...]) -> bool:
    return any(
        all(keyword in text for keyword in alternative) for alternative in alternatives
    )


def _missing_condition_categories(conditions: list[Any]) -> list[str]:
    texts = [
        _normalise(condition.get("text"))
        for condition in conditions
        if isinstance(condition, dict)
    ]
    used: set[int] = set()

    def assign(index: int) -> bool:
        if index == len(CONDITION_CATEGORIES):
            return True
        _, alternatives = CONDITION_CATEGORIES[index]
        for text_index, text in enumerate(texts):
            if text_index in used or not _matches_condition(text, alternatives):
                continue
            used.add(text_index)
            if assign(index + 1):
                return True
            used.remove(text_index)
        return False

    if assign(0):
        return []
    return [
        name
        for name, alternatives in CONDITION_CATEGORIES
        if not any(_matches_condition(text, alternatives) for text in texts)
    ]


def _validate_gate_list(
    gates: Any,
    label: str,
    *,
    decision: str,
    exception_ids: set[str],
    enforce_bid_block: bool,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(gates, list) or not gates:
        return [f"{label} must be a non-empty list."]

    gate_ids = [
        gate.get("id") for gate in gates if isinstance(gate, dict) and gate.get("id")
    ]
    if set(gate_ids) != EXPECTED_GATES:
        errors.append(f"{label} must contain exactly G1-G6; got {sorted(set(gate_ids))}.")
    if len(gate_ids) != len(set(gate_ids)):
        errors.append(f"{label} contains duplicate gate ids.")

    for index, gate in enumerate(gates, start=1):
        item = f"{label}[{index}]"
        if not isinstance(gate, dict):
            errors.append(f"{item} must be an object.")
            continue
        for field in ("id", "text", "status", "evidence"):
            if field not in gate:
                errors.append(f"{item} missing field: {field}")
        if gate.get("status") not in GATE_STATUSES:
            errors.append(f"{item} invalid status: {gate.get('status')!r}.")
        if not _present(gate.get("evidence")):
            errors.append(f"{item} requires evidence.")
        if (
            enforce_bid_block
            and gate.get("status") == "fail"
            and decision in {"bid", "bid_with_partner"}
            and gate.get("id") not in exception_ids
        ):
            errors.append(
                f"{item} failed; a bid decision requires a recorded human gate exception."
            )
    return errors


def validate(data: Any) -> list[str]:
    """Return a list of validation errors. Empty means valid."""
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["Decision record must be a JSON object."]

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    if errors:
        return errors

    unknown_fields = set(data) - ALLOWED_TOP_LEVEL
    if unknown_fields:
        errors.append(f"Unknown top-level fields: {sorted(unknown_fields)}.")

    for field in ("pursuit", "rfp", "human_owner", "rationale", "uncertainty"):
        if not _present(data.get(field)):
            errors.append(f"Field must not be empty: {field}")

    human_owner = data.get("human_owner")
    if (
        _is_placeholder(human_owner)
        or _looks_like_agent(human_owner)
    ):
        errors.append(
            "human_owner must name a human decision owner, not an agent or placeholder."
        )

    decision = data.get("decision")
    if decision not in DECISIONS:
        errors.append(f"Invalid decision: {decision!r}. Expected one of {sorted(DECISIONS)}.")

    if not _is_iso_date(data.get("decision_date")):
        errors.append("decision_date must be an ISO date (YYYY-MM-DD).")

    if data.get("human_signoff") is not True:
        errors.append("human_signoff must be true; a human must own the decision.")

    if decision in {"bid", "bid_with_partner"} and not _is_meaningful_reference(
        data.get("human_approval_ref")
    ):
        errors.append(
            "human_approval_ref must cite a specific room message or approval record "
            "for a bid decision; placeholders are not accepted."
        )

    for field in ("human_approval_ref", "rationale", "uncertainty"):
        if AGENT_APPROVAL_PATTERN.search(str(data.get(field, ""))):
            errors.append(
                f"{field} must not claim an agent approved, signed, or submitted the bid; "
                "only the human owner can approve."
            )

    if decision == "bid_with_partner":
        fallback = str(data.get("fallback", "")).lower()
        if not fallback:
            errors.append("fallback is required for bid_with_partner.")
        elif "no-bid" not in fallback and "no bid" not in fallback and "no_bid" not in fallback:
            errors.append("fallback must state the default no-bid outcome.")

    requirements = data.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        errors.append("requirements must be a non-empty list.")
    else:
        seen_ids: set[str] = set()
        for index, requirement in enumerate(requirements, start=1):
            item = f"requirements[{index}]"
            if not isinstance(requirement, dict):
                errors.append(f"{item} must be an object.")
                continue
            for field in ("id", "text", "status", "evidence"):
                if field not in requirement:
                    errors.append(f"{item} missing field: {field}")
            req_id = requirement.get("id")
            if req_id in seen_ids:
                errors.append(f"{item} duplicate requirement id: {req_id}")
            if isinstance(req_id, str):
                seen_ids.add(req_id)
            if requirement.get("status") not in REQUIREMENT_STATUSES:
                errors.append(
                    f"{item} invalid status: {requirement.get('status')!r}."
                )
            if not _present(requirement.get("evidence")):
                errors.append(f"{item} requires evidence or a gap note.")
        if seen_ids != EXPECTED_REQUIREMENTS:
            errors.append(
                "requirements must contain exactly M1-M6; "
                f"got {sorted(seen_ids)}."
            )

    base_requirements = data.get("base_requirements")
    if not isinstance(base_requirements, list) or not base_requirements:
        errors.append("base_requirements must be a non-empty list.")
    else:
        base_seen_ids: set[str] = set()
        base_statuses: set[str] = set()
        for index, requirement in enumerate(base_requirements, start=1):
            item = f"base_requirements[{index}]"
            if not isinstance(requirement, dict):
                errors.append(f"{item} must be an object.")
                continue
            for field in ("id", "text", "status", "evidence"):
                if field not in requirement:
                    errors.append(f"{item} missing field: {field}")
            req_id = requirement.get("id")
            if req_id in base_seen_ids:
                errors.append(f"{item} duplicate requirement id: {req_id}")
            if isinstance(req_id, str):
                base_seen_ids.add(req_id)
            if requirement.get("status") not in REQUIREMENT_STATUSES:
                errors.append(f"{item} invalid status: {requirement.get('status')!r}.")
            else:
                base_statuses.add(requirement["status"])
            if not _present(requirement.get("evidence")):
                errors.append(f"{item} requires evidence or a gap note.")
        if base_seen_ids != EXPECTED_REQUIREMENTS:
            errors.append(
                "base_requirements must contain exactly M1-M6; "
                f"got {sorted(base_seen_ids)}."
            )
        if "partner_covered" in base_statuses:
            errors.append(
                "base_requirements must describe Meridian alone; partner_covered "
                "belongs only in the decision path."
            )

    scores = data.get("scores")
    computed_score = 0.0
    total_weight = 0.0
    if not isinstance(scores, dict):
        errors.append("scores must be an object.")
    else:
        unknown_scores = set(scores) - set(SCORE_KEYS)
        if unknown_scores:
            errors.append(f"Unknown score criteria: {sorted(unknown_scores)}.")
        for key in SCORE_KEYS:
            entry = scores.get(key)
            item = f"scores.{key}"
            if not isinstance(entry, dict):
                errors.append(f"{item} must be an object.")
                continue
            weight = entry.get("weight")
            score = entry.get("score")
            if not _is_number(weight) or weight <= 0:
                errors.append(f"{item}.weight must be a positive number.")
            else:
                total_weight += float(weight)
                if abs(float(weight) - EXPECTED_WEIGHTS[key]) > 0.01:
                    errors.append(
                        f"{item}.weight must be {EXPECTED_WEIGHTS[key]} for the RFP policy."
                    )
            if not _is_number(score) or not (1 <= float(score) <= 5):
                errors.append(f"{item}.score must be a number from 1 to 5.")
            else:
                if _is_number(weight):
                    computed_score += float(score) * float(weight)
            if not _present(entry.get("evidence")):
                errors.append(f"{item} requires evidence.")

        if abs(total_weight - 100) > 0.01:
            errors.append(f"Score weights must sum to 100; got {total_weight:g}.")

        computed_score = computed_score / 5.0
        total_score = data.get("total_score")
        if not _is_number(total_score):
            errors.append("total_score must be a number.")
        elif abs(float(total_score) - computed_score) > 0.1:
            errors.append(
                f"total_score {total_score:g} does not match computed "
                f"{computed_score:.1f}."
            )
        elif decision in {"bid", "bid_with_partner"} and float(total_score) < 65:
            errors.append(
                "A bid decision requires total_score at least 65; "
                f"got {float(total_score):g}."
            )

    base_scores = data.get("base_scores")
    base_computed = 0.0
    base_weight_total = 0.0
    if not isinstance(base_scores, dict):
        errors.append("base_scores must be an object.")
    else:
        unknown_base_scores = set(base_scores) - set(SCORE_KEYS)
        if unknown_base_scores:
            errors.append(f"Unknown base score criteria: {sorted(unknown_base_scores)}.")
        for key in SCORE_KEYS:
            entry = base_scores.get(key)
            item = f"base_scores.{key}"
            if not isinstance(entry, dict):
                errors.append(f"{item} must be an object.")
                continue
            weight = entry.get("weight")
            score = entry.get("score")
            if not _is_number(weight) or weight <= 0:
                errors.append(f"{item}.weight must be a positive number.")
            else:
                base_weight_total += float(weight)
                if abs(float(weight) - EXPECTED_WEIGHTS[key]) > 0.01:
                    errors.append(
                        f"{item}.weight must be {EXPECTED_WEIGHTS[key]} for the RFP policy."
                    )
            if not _is_number(score) or not (1 <= float(score) <= 5):
                errors.append(f"{item}.score must be a number from 1 to 5.")
            elif _is_number(weight):
                base_computed += float(score) * float(weight)
            if not _present(entry.get("evidence")):
                errors.append(f"{item} requires evidence.")
        if abs(base_weight_total - 100) > 0.01:
            errors.append(
                f"Base score weights must sum to 100; got {base_weight_total:g}."
            )
        base_computed = base_computed / 5.0

    base_total_score = data.get("base_total_score")
    if not _is_number(base_total_score):
        errors.append("base_total_score must be a number.")
    elif isinstance(base_scores, dict) and abs(float(base_total_score) - base_computed) > 0.1:
        errors.append(
            f"base_total_score {base_total_score:g} does not match computed "
            f"{base_computed:.1f}."
        )

    gate_exceptions = data.get("gate_exceptions", [])
    if not isinstance(gate_exceptions, list):
        errors.append("gate_exceptions must be a list when present.")
        gate_exceptions = []
    exception_ids: set[str] = set()
    for index, exception in enumerate(gate_exceptions, start=1):
        item = f"gate_exceptions[{index}]"
        if not isinstance(exception, dict):
            errors.append(f"{item} must be an object.")
            continue
        for field in (
            "gate_id",
            "approved_by",
            "approved_by_role",
            "reason",
            "date",
            "record_ref",
        ):
            if not _present(exception.get(field)):
                errors.append(f"{item} requires {field}.")
        if exception.get("gate_id") not in EXPECTED_GATES:
            errors.append(f"{item}.gate_id must be one of G1-G6.")
        if exception.get("approved_by_role") != "Pursuit Lead + Accountable Executive":
            errors.append(
                f"{item}.approved_by_role must be 'Pursuit Lead + Accountable Executive'."
            )
        if not _is_meaningful_reference(exception.get("record_ref")):
            errors.append(f"{item}.record_ref must identify a real record.")
        if _is_placeholder(exception.get("approved_by")) or _looks_like_agent(
            exception.get("approved_by")
        ):
            errors.append(f"{item}.approved_by must name a human approver.")
        if len(str(exception.get("reason", "")).strip()) < 10:
            errors.append(f"{item}.reason must be a substantive explanation.")
        if exception.get("date") and not _is_iso_date(exception.get("date")):
            errors.append(f"{item}.date must be an ISO date.")
        if (
            exception.get("gate_id") in EXPECTED_GATES
            and _present(exception.get("approved_by"))
            and not _is_placeholder(exception.get("approved_by"))
            and not _looks_like_agent(exception.get("approved_by"))
            and exception.get("approved_by_role") == "Pursuit Lead + Accountable Executive"
            and _present(exception.get("reason"))
            and _is_iso_date(exception.get("date"))
            and _is_meaningful_reference(exception.get("record_ref"))
        ):
            exception_ids.add(exception["gate_id"])

    base_gates = data.get("base_gates")
    errors.extend(
        _validate_gate_list(
            base_gates,
            "base_gates",
            decision=decision,
            exception_ids=exception_ids,
            enforce_bid_block=False,
        )
    )
    base_margin = data.get("base_margin_percent")
    if not _is_number(base_margin):
        errors.append("base_margin_percent must be a number.")
    if isinstance(base_gates, list) and _is_number(base_total_score):
        base_by_id = {
            gate.get("id"): gate
            for gate in base_gates
            if isinstance(gate, dict) and gate.get("id")
        }
        base_g2 = base_by_id.get("G2")
        if base_g2:
            if float(base_total_score) < 65 and base_g2.get("status") != "fail":
                errors.append("Base G2 must be fail when base_total_score is below 65.")
            if float(base_total_score) >= 65 and base_g2.get("status") == "fail":
                errors.append("Base G2 cannot be fail when base_total_score is at least 65.")

        base_requirement_statuses = {
            requirement.get("status")
            for requirement in base_requirements
            if isinstance(requirement, dict)
        } if isinstance(base_requirements, list) else set()

        base_g1 = base_by_id.get("G1")
        if (
            base_g1
            and base_g1.get("status") in {"pass", "pass_with_conditions"}
            and base_requirement_statuses & {"missing", "conflicting", "not_assessed"}
        ):
            errors.append(
                "Base G1 cannot be pass while a mandatory requirement is missing, "
                "conflicting, or not assessed."
            )

        base_g3 = base_by_id.get("G3")
        policy_min = data.get("policy_min_margin_percent")
        if (
            base_g3
            and _is_number(base_margin)
            and _is_number(policy_min)
            and float(base_margin) < float(policy_min)
            and base_g3.get("status") == "pass"
        ):
            errors.append(
                "Base G3 cannot be pass when base_margin_percent is below the policy minimum."
            )

        base_m4_status = next(
            (
                requirement.get("status")
                for requirement in base_requirements
                if isinstance(requirement, dict) and requirement.get("id") == "M4"
            ),
            None,
        ) if isinstance(base_requirements, list) else None
        base_g4 = base_by_id.get("G4")
        if (
            base_g4
            and base_g4.get("status") == "pass"
            and base_m4_status in {"missing", "conflicting", "not_assessed"}
        ):
            errors.append(
                "Base G4 cannot be pass while base M4 is missing, conflicting, or not assessed."
            )

    gates = data.get("gates")
    errors.extend(
        _validate_gate_list(
            gates,
            "gates",
            decision=decision,
            exception_ids=exception_ids,
            enforce_bid_block=True,
        )
    )

    if isinstance(gates, list):
        by_id = {
            gate.get("id"): gate
            for gate in gates
            if isinstance(gate, dict) and gate.get("id")
        }
        requirement_statuses = {
            requirement.get("status")
            for requirement in requirements
            if isinstance(requirement, dict)
        } if isinstance(requirements, list) else set()

        g1 = by_id.get("G1")
        if (
            g1
            and g1.get("status") in {"pass", "pass_with_conditions"}
            and requirement_statuses & {"missing", "conflicting", "not_assessed"}
        ):
            errors.append(
                "G1 cannot be pass while a mandatory requirement is missing, "
                "conflicting, or not assessed."
            )

        g2 = by_id.get("G2")
        if g2 and _is_number(data.get("total_score")):
            score = float(data["total_score"])
            if score < 65 and g2.get("status") != "fail":
                errors.append("G2 must be fail when total_score is below 65.")
            if score >= 65 and g2.get("status") == "fail":
                errors.append("G2 cannot be fail when total_score is at least 65.")

        g3 = by_id.get("G3")
        margin = data.get("margin_percent")
        policy_min = data.get("policy_min_margin_percent")
        if g3 and _is_number(margin) and _is_number(policy_min):
            if float(margin) < float(policy_min) and g3.get("status") == "pass":
                errors.append(
                    "G3 cannot be pass when margin is below the policy minimum."
                )

        m4_status = next(
            (
                requirement.get("status")
                for requirement in requirements
                if isinstance(requirement, dict) and requirement.get("id") == "M4"
            ),
            None,
        ) if isinstance(requirements, list) else None
        g4 = by_id.get("G4")
        if (
            g4
            and g4.get("status") == "pass"
            and m4_status in {"missing", "conflicting", "not_assessed"}
        ):
            errors.append(
                "G4 cannot be pass while M4 is missing, conflicting, or not assessed."
            )

        g6 = by_id.get("G6")
        if g6 and g6.get("status") == "fail":
            errors.append(
                "G6 cannot be fail when human_signoff is true; record the human approval "
                "or mark the gate conditional."
            )

    margin = data.get("margin_percent")
    policy_min = data.get("policy_min_margin_percent")
    if not _is_number(margin):
        errors.append("margin_percent must be a number.")
    if not _is_number(policy_min):
        errors.append("policy_min_margin_percent must be a number.")
    elif abs(float(policy_min) - POLICY_MIN_MARGIN) > 0.01:
        errors.append(
            f"policy_min_margin_percent must be {POLICY_MIN_MARGIN:g} for the bid policy."
        )
    if (
        _is_number(margin)
        and _is_number(policy_min)
        and decision in {"bid", "bid_with_partner"}
        and float(margin) < float(policy_min)
    ):
        exception = data.get("margin_exception")
        if not isinstance(exception, dict):
            errors.append(
                "margin is below policy; margin_exception is required for a bid decision."
            )
        else:
            if _is_placeholder(exception.get("approved_by")) or _looks_like_agent(
                exception.get("approved_by")
            ):
                errors.append(
                    "margin_exception.approved_by must name a human approver."
                )
            if exception.get("approved_by_role") != "VP of Finance":
                errors.append("margin_exception.approved_by_role must be 'VP of Finance'.")
            if len(str(exception.get("reason", "")).strip()) < 10:
                errors.append("margin_exception.reason must be a substantive explanation.")
            if not _is_iso_date(exception.get("date")):
                errors.append("margin_exception.date must be an ISO date.")
            if not _is_meaningful_reference(exception.get("record_ref")):
                errors.append(
                    "margin_exception.record_ref must identify a real record."
                )

    for list_name in ("conditions", "actions"):
        items = data.get(list_name)
        if not isinstance(items, list):
            errors.append(f"{list_name} must be a list.")
            continue
        for index, item in enumerate(items, start=1):
            label = f"{list_name}[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{label} must be an object.")
                continue
            for field in ("text", "owner", "due_date"):
                if not _present(item.get(field)) or _is_placeholder(item.get(field)):
                    errors.append(f"{label}.{field} must be substantive.")
            if len(_normalise(item.get("text"))) < 10:
                errors.append(f"{label}.text must be a substantive description.")
            if _looks_like_agent(item.get("owner")):
                errors.append(
                    f"{label}.owner must name a human or accountable role, not an agent."
                )
            if item.get("due_date") and not _is_iso_date(item.get("due_date")):
                errors.append(f"{label}.due_date must be an ISO date.")
            if item.get("status") is not None and item.get("status") not in ITEM_STATUSES:
                errors.append(
                    f"{label}.status must be one of {sorted(ITEM_STATUSES)} when present."
                )

    if decision == "bid_with_partner":
        conditions = data.get("conditions")
        if not isinstance(conditions, list) or len(conditions) < 9:
            errors.append(
                "bid_with_partner requires the full nine-condition set."
            )
        elif isinstance(conditions, list):
            missing_categories = _missing_condition_categories(conditions)
            if missing_categories:
                errors.append(
                    "bid_with_partner conditions must cover: "
                    + "; ".join(missing_categories)
                    + "."
                )

    if decision in {"bid", "bid_with_partner"} and not data.get("actions"):
        errors.append("A bid decision requires at least one action.")

    data_note = str(data.get("data_note", "")).lower()
    if "fictional" not in data_note and "synthetic" not in data_note:
        errors.append("data_note must confirm the data is fictional or synthetic.")
    for negative in (
        "not fictional",
        "not synthetic",
        "real customer",
        "real client",
        "real data",
        "confidential client",
        "confidential data",
    ):
        if negative in data_note:
            errors.append(
                "data_note must affirm synthetic data, not negate it or claim real data."
            )
            break

    return errors


def _render_gate_table(title: str, gates: list[dict[str, Any]]) -> list[str]:
    lines = [
        f"## {title}",
        "",
        "| Gate | Status | Evidence |",
        "|---|---|---|",
    ]
    for gate in gates:
        lines.append(
            "| {id} - {text} | {status} | {evidence} |".format(
                id=_escape(gate.get("id", "")),
                text=_escape(gate.get("text", "")),
                status=_escape(gate.get("status", "")),
                evidence=_escape(gate.get("evidence", "")),
            )
        )
    lines.append("")
    return lines


def _render_items(title: str, items: list[dict[str, Any]]) -> list[str]:
    lines = [f"## {title}", ""]
    if not items:
        lines.extend(["None.", ""])
        return lines
    lines.extend(["| Item | Owner | Due | Status |", "|---|---|---|---|"])
    for item in items:
        lines.append(
            "| {text} | {owner} | {due} | {status} |".format(
                text=_escape(item.get("text", "")),
                owner=_escape(item.get("owner", "")),
                due=_escape(item.get("due_date", "")),
                status=_escape(item.get("status", "open")),
            )
        )
    lines.append("")
    return lines


def render_markdown(data: dict[str, Any]) -> str:
    decision = DECISION_LABELS.get(data["decision"], data["decision"])
    if data["decision"] == "bid_with_partner" and _present(data.get("fallback")):
        decision += " (conditional)"
    lines: list[str] = [
        f"# Bid Decision Record - {data['pursuit']}",
        "",
        f"**RFP:** {data['rfp']}  ",
        f"**Decision:** {decision}  ",
        f"**Human owner:** {data['human_owner']}  ",
        f"**Decision date:** {data['decision_date']}  ",
        f"**Data note:** {data['data_note']}",
        "",
    ]
    if _present(data.get("human_approval_ref")):
        lines.extend([f"**Human approval reference:** {data['human_approval_ref']}", ""])

    lines.extend(
        [
            "## Requirements and evidence",
            "",
            "| ID | Requirement | Status | Evidence / gap |",
            "|---|---|---|---|",
        ]
    )
    for requirement in data["requirements"]:
        lines.append(
            "| {id} | {text} | {status} | {evidence} |".format(
                id=_escape(requirement.get("id", "")),
                text=_escape(requirement.get("text", "")),
                status=_escape(requirement.get("status", "")),
                evidence=_escape(requirement.get("evidence", "")),
            )
        )
    lines.append("")

    lines.extend(_render_gate_table("Base gates", data["base_gates"]))
    lines.extend(
        [
            "## Base score",
            "",
            "| Criterion | Weight | Score | Weighted | Evidence |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for key in SCORE_KEYS:
        entry = data["base_scores"][key]
        weighted = float(entry["score"]) * float(entry["weight"]) / 5.0
        lines.append(
            "| {criterion} | {weight:g} | {score:g} | {weighted:g} | {evidence} |".format(
                criterion=key.replace("_", " ").title(),
                weight=float(entry["weight"]),
                score=float(entry["score"]),
                weighted=weighted,
                evidence=_escape(entry.get("evidence", "")),
            )
        )
    lines.extend(
        [
            f"| **Base total** | **100** |  | **{float(data['base_total_score']):g}** |  |",
            "",
        ]
    )
    gate_title = "Partner gates" if data["decision"] == "bid_with_partner" else "Decision gates"
    lines.extend(_render_gate_table(gate_title, data["gates"]))

    gate_exceptions = data.get("gate_exceptions", [])
    if isinstance(gate_exceptions, list) and gate_exceptions:
        lines.extend(
            [
                "## Gate exceptions",
                "",
                "| Gate | Approved by | Date | Record reference | Reason |",
                "|---|---|---|---|---|",
            ]
        )
        for exception in gate_exceptions:
            lines.append(
                "| {gate} | {approved} | {date} | {ref} | {reason} |".format(
                    gate=_escape(exception.get("gate_id", "")),
                    approved=_escape(exception.get("approved_by", "")),
                    date=_escape(exception.get("date", "")),
                    ref=_escape(exception.get("record_ref", "")),
                    reason=_escape(exception.get("reason", "")),
                )
            )
        lines.append("")

    lines.extend(
        [
            "## Partner score" if data["decision"] == "bid_with_partner" else "## Decision score",
            "",
            "| Criterion | Weight | Score | Weighted | Evidence |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for key in SCORE_KEYS:
        entry = data["scores"][key]
        weighted = float(entry["score"]) * float(entry["weight"]) / 5.0
        lines.append(
            "| {criterion} | {weight:g} | {score:g} | {weighted:g} | {evidence} |".format(
                criterion=key.replace("_", " ").title(),
                weight=float(entry["weight"]),
                score=float(entry["score"]),
                weighted=weighted,
                evidence=_escape(entry.get("evidence", "")),
            )
        )
    lines.extend(
        [
            f"| **Total** | **100** |  | **{float(data['total_score']):g}** |  |",
            "",
            f"**Margin:** {float(data['margin_percent']):g}% "
            f"(policy minimum {float(data['policy_min_margin_percent']):g}%)",
            "",
        ]
    )
    exception = data.get("margin_exception")
    if isinstance(exception, dict):
        lines.extend(
            [
                "**Margin exception:**  ",
                f"- Approved by: {exception.get('approved_by', '')}  ",
                f"- Role: {exception.get('approved_by_role', '')}  ",
                f"- Date: {exception.get('date', '')}  ",
                f"- Record reference: {exception.get('record_ref', '')}  ",
                f"- Reason: {exception.get('reason', '')}",
                "",
            ]
        )

    if _present(data.get("fallback")):
        lines.extend([f"**Fallback:** {data['fallback']}", ""])

    lines.extend(["## Uncertainty", "", str(data["uncertainty"]), "", "## Rationale", "", str(data["rationale"]), ""])
    lines.extend(_render_items("Conditions", data["conditions"]))
    lines.extend(_render_items("Actions", data["actions"]))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a BidRoom decision record and optionally emit markdown."
    )
    parser.add_argument("input", help="Path to decision JSON")
    parser.add_argument("--md", help="Optional path for the markdown decision record")
    args = parser.parse_args(argv)

    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"ERROR: could not read {args.input}: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate(payload)
    if errors:
        print("INVALID decision record:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if args.md:
        try:
            Path(args.md).write_text(render_markdown(payload), encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: could not write {args.md}: {exc}", file=sys.stderr)
            return 2

    print(
        f"VALID: {payload['pursuit']} | {payload['decision']} | "
        f"{float(payload['total_score']):g}/100"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
