"""Policy-driven validation and markdown rendering for BidRoom decision records."""

from __future__ import annotations

import re
from datetime import date
from typing import Any

from .policy import Policy

GATE_STATUSES = {"pass", "pass_with_conditions", "fail"}
ITEM_STATUSES = {"open", "done", "blocked", "cancelled"}

CORE_REQUIRED_FIELDS = (
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
OPTIONAL_FIELDS = (
    "human_approval_ref",
    "fallback",
    "gate_exceptions",
    "margin_exception",
    "policy_id",
    "policy_version",
)
ALLOWED_FIELDS = set(CORE_REQUIRED_FIELDS) | set(OPTIONAL_FIELDS)

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
AGENT_MARKERS = ("bid-analyst", "bid-critic", "room-auditor")
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


def _matches_condition(text: str, keywords: tuple[tuple[str, ...], ...]) -> bool:
    return any(all(keyword in text for keyword in group) for group in keywords)


def _missing_condition_categories(
    conditions: list[Any], policy: Policy
) -> list[str]:
    texts = [
        _normalise(condition.get("text"))
        for condition in conditions
        if isinstance(condition, dict)
    ]
    used: set[int] = set()

    def assign(index: int) -> bool:
        if index == len(policy.condition_categories):
            return True
        category = policy.condition_categories[index]
        for text_index, text in enumerate(texts):
            if text_index in used or not _matches_condition(text, category.keywords):
                continue
            used.add(text_index)
            if assign(index + 1):
                return True
            used.remove(text_index)
        return False

    if assign(0):
        return []
    return [
        category.label
        for category in policy.condition_categories
        if not any(_matches_condition(text, category.keywords) for text in texts)
    ]


def _gate_list(
    gates: Any,
    label: str,
    policy: Policy,
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
    if set(gate_ids) != set(policy.gate_ids):
        errors.append(f"{label} must contain exactly {sorted(policy.gate_ids)}; got {sorted(set(gate_ids))}.")
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
            and decision in policy.bid_decisions
            and gate.get("id") not in exception_ids
        ):
            errors.append(
                f"{item} failed; a bid decision requires a recorded human gate exception."
            )
    return errors


def _requirement_list(
    requirements: Any,
    label: str,
    policy: Policy,
    *,
    base: bool,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(requirements, list) or not requirements:
        return [f"{label} must be a non-empty list."]

    seen: set[str] = set()
    statuses: set[str] = set()
    for index, requirement in enumerate(requirements, start=1):
        item = f"{label}[{index}]"
        if not isinstance(requirement, dict):
            errors.append(f"{item} must be an object.")
            continue
        for field in ("id", "text", "status", "evidence"):
            if field not in requirement:
                errors.append(f"{item} missing field: {field}")
        requirement_id = requirement.get("id")
        if requirement_id in seen:
            errors.append(f"{item} duplicate requirement id: {requirement_id}")
        if isinstance(requirement_id, str):
            seen.add(requirement_id)
        status = requirement.get("status")
        if status not in policy.requirement_statuses:
            errors.append(f"{item} invalid status: {status!r}.")
        else:
            statuses.add(status)
        if not _present(requirement.get("evidence")):
            errors.append(f"{item} requires evidence or a gap note.")

    if seen != set(policy.requirement_ids):
        errors.append(
            f"{label} must contain exactly {sorted(policy.requirement_ids)}; got {sorted(seen)}."
        )
    if base and policy.base_partner_status in statuses:
        errors.append(
            f"{label} must describe the bidder alone; {policy.base_partner_status} "
            "belongs only in the decision path."
        )
    return errors


def _score_block(
    scores: Any,
    label: str,
    policy: Policy,
) -> tuple[list[str], float, set[str]]:
    errors: list[str] = []
    computed = 0.0
    weights_total = 0.0
    seen: set[str] = set()
    if not isinstance(scores, dict):
        return [f"{label} must be an object."], 0.0, set()

    for key, entry in scores.items():
        if key not in policy.criterion_ids:
            errors.append(f"Unknown score criteria in {label}: {key}.")
            continue
        seen.add(key)
        item = f"{label}.{key}"
        if not isinstance(entry, dict):
            errors.append(f"{item} must be an object.")
            continue
        weight = entry.get("weight")
        score = entry.get("score")
        if not _is_number(weight) or weight <= 0:
            errors.append(f"{item}.weight must be a positive number.")
        else:
            weights_total += float(weight)
            expected = policy.weights[key]
            if abs(float(weight) - expected) > 0.01:
                errors.append(f"{item}.weight must be {expected:g} for this policy.")
        if not _is_number(score) or not (1 <= float(score) <= 5):
            errors.append(f"{item}.score must be a number from 1 to 5.")
        elif _is_number(weight):
            computed += float(score) * float(weight)
        if not _present(entry.get("evidence")):
            errors.append(f"{item} requires evidence.")

    missing = set(policy.criterion_ids) - seen
    if missing:
        errors.append(f"{label} missing criteria: {sorted(missing)}.")
    if abs(weights_total - 100) > 0.01:
        errors.append(f"{label} weights must sum to 100; got {weights_total:g}.")
    return errors, computed / 5.0, seen


def validate(data: Any, policy: Policy) -> list[str]:
    """Return validation errors for a decision record against a policy."""

    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Decision record must be a JSON object."]

    for field in CORE_REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    if errors:
        return errors

    unknown = set(data) - ALLOWED_FIELDS
    if unknown:
        errors.append(f"Unknown top-level fields: {sorted(unknown)}.")

    for field in ("pursuit", "rfp", "human_owner", "rationale", "uncertainty"):
        if not _present(data.get(field)):
            errors.append(f"Field must not be empty: {field}")

    human_owner = data.get("human_owner")
    if _is_placeholder(human_owner) or _looks_like_agent(human_owner):
        errors.append("human_owner must name a human decision owner, not an agent or placeholder.")

    decision = data.get("decision")
    if decision not in policy.decision_options:
        errors.append(
            f"Invalid decision: {decision!r}. Expected one of {sorted(policy.decision_options)}."
        )

    if not _is_iso_date(data.get("decision_date")):
        errors.append("decision_date must be an ISO date (YYYY-MM-DD).")

    if data.get("human_signoff") is not True:
        errors.append("human_signoff must be true; a human must own the decision.")

    if decision in policy.bid_decisions and not _is_meaningful_reference(
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

    if decision in policy.fallback_required_for:
        fallback = str(data.get("fallback", "")).lower()
        if not fallback:
            errors.append(f"fallback is required for {decision}.")
        elif policy.no_bid not in fallback and policy.no_bid.replace("_", "-") not in fallback:
            errors.append("fallback must state the default no-bid outcome.")

    errors.extend(
        _requirement_list(data.get("requirements"), "requirements", policy, base=False)
    )
    errors.extend(
        _requirement_list(
            data.get("base_requirements"), "base_requirements", policy, base=True
        )
    )

    score_errors, computed_score, _ = _score_block(data.get("scores"), "scores", policy)
    errors.extend(score_errors)
    total_score = data.get("total_score")
    if not _is_number(total_score):
        errors.append("total_score must be a number.")
    elif abs(float(total_score) - computed_score) > 0.1:
        errors.append(
            f"total_score {float(total_score):g} does not match computed {computed_score:.1f}."
        )
    elif decision in policy.bid_decisions and float(total_score) < policy.min_score:
        errors.append(
            f"A bid decision requires total_score at least {policy.min_score:g}; got {float(total_score):g}."
        )

    base_errors, base_computed, _ = _score_block(
        data.get("base_scores"), "base_scores", policy
    )
    errors.extend(base_errors)
    base_total_score = data.get("base_total_score")
    if not _is_number(base_total_score):
        errors.append("base_total_score must be a number.")
    elif abs(float(base_total_score) - base_computed) > 0.1:
        errors.append(
            f"base_total_score {float(base_total_score):g} does not match computed {base_computed:.1f}."
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
        if exception.get("gate_id") not in policy.gate_ids:
            errors.append(f"{item}.gate_id must be one of {sorted(policy.gate_ids)}.")
        if exception.get("approved_by_role") != policy.gate_exception_role:
            errors.append(
                f"{item}.approved_by_role must be {policy.gate_exception_role!r}."
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
            exception.get("gate_id") in policy.gate_ids
            and _present(exception.get("approved_by"))
            and not _is_placeholder(exception.get("approved_by"))
            and not _looks_like_agent(exception.get("approved_by"))
            and exception.get("approved_by_role") == policy.gate_exception_role
            and _present(exception.get("reason"))
            and _is_iso_date(exception.get("date"))
            and _is_meaningful_reference(exception.get("record_ref"))
        ):
            exception_ids.add(exception["gate_id"])

    errors.extend(
        _gate_list(
            data.get("base_gates"),
            "base_gates",
            policy,
            decision=decision,
            exception_ids=exception_ids,
            enforce_bid_block=False,
        )
    )
    errors.extend(
        _gate_list(
            data.get("gates"),
            "gates",
            policy,
            decision=decision,
            exception_ids=exception_ids,
            enforce_bid_block=True,
        )
    )

    base_margin = data.get("base_margin_percent")
    if not _is_number(base_margin):
        errors.append("base_margin_percent must be a number.")

    base_by_id = {
        gate.get("id"): gate
        for gate in data.get("base_gates", [])
        if isinstance(gate, dict) and gate.get("id")
    }
    by_id = {
        gate.get("id"): gate
        for gate in data.get("gates", [])
        if isinstance(gate, dict) and gate.get("id")
    }

    base_statuses = {
        requirement.get("status")
        for requirement in data.get("base_requirements", [])
        if isinstance(requirement, dict)
    }
    statuses = {
        requirement.get("status")
        for requirement in data.get("requirements", [])
        if isinstance(requirement, dict)
    }

    requirements_gate = base_by_id.get(policy.requirements_gate)
    if (
        requirements_gate
        and requirements_gate.get("status") in {"pass", "pass_with_conditions"}
        and base_statuses & set(policy.blocking_statuses)
    ):
        errors.append(
            f"Base {policy.requirements_gate} cannot be pass while a mandatory requirement is "
            "missing, conflicting, or not assessed."
        )

    requirements_gate = by_id.get(policy.requirements_gate)
    if (
        requirements_gate
        and requirements_gate.get("status") in {"pass", "pass_with_conditions"}
        and statuses & set(policy.blocking_statuses)
    ):
        errors.append(
            f"{policy.requirements_gate} cannot be pass while a mandatory requirement is "
            "missing, conflicting, or not assessed."
        )

    base_score_gate = base_by_id.get(policy.score_gate)
    if base_score_gate and _is_number(base_total_score):
        if float(base_total_score) < policy.min_score and base_score_gate.get("status") != "fail":
            errors.append(
                f"Base {policy.score_gate} must be fail when base_total_score is below {policy.min_score:g}."
            )
        if float(base_total_score) >= policy.min_score and base_score_gate.get("status") == "fail":
            errors.append(
                f"Base {policy.score_gate} cannot be fail when base_total_score is at least {policy.min_score:g}."
            )

    score_gate = by_id.get(policy.score_gate)
    if score_gate and _is_number(total_score):
        if float(total_score) < policy.min_score and score_gate.get("status") != "fail":
            errors.append(
                f"{policy.score_gate} must be fail when total_score is below {policy.min_score:g}."
            )
        if float(total_score) >= policy.min_score and score_gate.get("status") == "fail":
            errors.append(
                f"{policy.score_gate} cannot be fail when total_score is at least {policy.min_score:g}."
            )

    base_margin_gate = base_by_id.get(policy.margin_gate)
    policy_min = data.get("policy_min_margin_percent")
    if not _is_number(policy_min):
        errors.append("policy_min_margin_percent must be a number.")
    elif abs(float(policy_min) - policy.min_margin) > 0.01:
        errors.append(
            f"policy_min_margin_percent must be {policy.min_margin:g} for this policy."
        )
    if (
        base_margin_gate
        and _is_number(base_margin)
        and _is_number(policy_min)
        and float(base_margin) < float(policy_min)
        and base_margin_gate.get("status") == "pass"
    ):
        errors.append(
            f"Base {policy.margin_gate} cannot be pass when base_margin_percent is below the policy minimum."
        )

    margin = data.get("margin_percent")
    if not _is_number(margin):
        errors.append("margin_percent must be a number.")
    if (
        _is_number(margin)
        and _is_number(policy_min)
        and decision in policy.bid_decisions
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
                errors.append("margin_exception.approved_by must name a human approver.")
            if exception.get("approved_by_role") != policy.margin_exception_role:
                errors.append(
                    f"margin_exception.approved_by_role must be {policy.margin_exception_role!r}."
                )
            if len(str(exception.get("reason", "")).strip()) < 10:
                errors.append("margin_exception.reason must be a substantive explanation.")
            if not _is_iso_date(exception.get("date")):
                errors.append("margin_exception.date must be an ISO date.")
            if not _is_meaningful_reference(exception.get("record_ref")):
                errors.append("margin_exception.record_ref must identify a real record.")

    margin_gate = by_id.get(policy.margin_gate)
    if (
        margin_gate
        and _is_number(margin)
        and _is_number(policy_min)
        and float(margin) < float(policy_min)
        and margin_gate.get("status") == "pass"
    ):
        errors.append(
            f"{policy.margin_gate} cannot be pass when margin_percent is below the policy minimum."
        )

    capacity_gate = base_by_id.get(policy.capacity_gate)
    capacity_status = next(
        (
            requirement.get("status")
            for requirement in data.get("base_requirements", [])
            if isinstance(requirement, dict)
            and requirement.get("id") == policy.capacity_requirement
        ),
        None,
    )
    if (
        capacity_gate
        and capacity_gate.get("status") == "pass"
        and capacity_status in policy.blocking_statuses
    ):
        errors.append(
            f"Base {policy.capacity_gate} cannot be pass while {policy.capacity_requirement} "
            "is missing, conflicting, or not assessed."
        )

    capacity_gate = by_id.get(policy.capacity_gate)
    capacity_status = next(
        (
            requirement.get("status")
            for requirement in data.get("requirements", [])
            if isinstance(requirement, dict)
            and requirement.get("id") == policy.capacity_requirement
        ),
        None,
    )
    if (
        capacity_gate
        and capacity_gate.get("status") == "pass"
        and capacity_status in policy.blocking_statuses
    ):
        errors.append(
            f"{policy.capacity_gate} cannot be pass while {policy.capacity_requirement} "
            "is missing, conflicting, or not assessed."
        )

    human_gate = by_id.get(policy.human_approval_gate)
    if human_gate and human_gate.get("status") == "fail":
        errors.append(
            f"{policy.human_approval_gate} cannot be fail when human_signoff is true; "
            "record the human approval or mark the gate conditional."
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

    if decision in policy.fallback_required_for:
        conditions = data.get("conditions")
        if not isinstance(conditions, list) or len(conditions) < policy.min_conditions:
            errors.append(
                f"{decision} requires at least {policy.min_conditions} conditions."
            )
        elif isinstance(conditions, list):
            missing = _missing_condition_categories(conditions, policy)
            if missing:
                errors.append(
                    f"{decision} conditions must cover: " + "; ".join(missing) + "."
                )

    if decision in policy.bid_decisions and not data.get("actions"):
        errors.append("A bid decision requires at least one action.")

    data_note = str(data.get("data_note", "")).lower()
    if not any(term.lower() in data_note for term in policy.data_note_required):
        errors.append("data_note must confirm the data is fictional or synthetic.")
    for forbidden in policy.data_note_forbidden:
        if forbidden.lower() in data_note:
            errors.append(
                "data_note must affirm synthetic data, not negate it or claim real or "
                "confidential data."
            )
            break

    return errors


def _decision_label(decision: str) -> str:
    return decision.replace("_", " ").replace("-", " ").title()


def _render_gate_table(title: str, gates: list[dict[str, Any]]) -> list[str]:
    lines = [f"## {title}", "", "| Gate | Status | Evidence |", "|---|---|---|"]
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


def render_markdown(data: dict[str, Any], policy: Policy) -> str:
    decision = _decision_label(str(data["decision"]))
    lines = [
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
    for key in policy.criterion_ids:
        entry = data["base_scores"][key]
        weighted = float(entry["score"]) * float(entry["weight"]) / 5.0
        lines.append(
            "| {criterion} | {weight:g} | {score:g} | {weighted:g} | {evidence} |".format(
                criterion=policy.criterion_labels[key],
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
    for key in policy.criterion_ids:
        entry = data["scores"][key]
        weighted = float(entry["score"]) * float(entry["weight"]) / 5.0
        lines.append(
            "| {criterion} | {weight:g} | {score:g} | {weighted:g} | {evidence} |".format(
                criterion=policy.criterion_labels[key],
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

    lines.extend(
        [
            "## Uncertainty",
            "",
            str(data["uncertainty"]),
            "",
            "## Rationale",
            "",
            str(data["rationale"]),
            "",
        ]
    )
    lines.extend(_render_items("Conditions", data["conditions"]))
    lines.extend(_render_items("Actions", data["actions"]))
    return "\n".join(lines)
