"""Policy loading and validation for BidRoom.

The policy is the source of truth for gates, requirements, scoring, thresholds,
condition categories, and decision rules. The engine must not contain
scenario-specific constants.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class PolicyError(ValueError):
    """Raised when a policy file is malformed."""


@dataclass(frozen=True)
class Criterion:
    id: str
    label: str
    weight: float


@dataclass(frozen=True)
class Gate:
    id: str
    text: str
    type: str


@dataclass(frozen=True)
class ConditionCategory:
    id: str
    label: str
    keywords: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class Policy:
    policy_id: str
    policy_version: str
    description: str
    decision_options: tuple[str, ...]
    bid_decisions: frozenset[str]
    no_bid: str
    fallback_required_for: frozenset[str]
    requirement_ids: tuple[str, ...]
    requirement_statuses: frozenset[str]
    base_partner_status: str
    blocking_statuses: frozenset[str]
    criteria: tuple[Criterion, ...]
    min_score: float
    score_formula: str
    gates: tuple[Gate, ...]
    requirements_gate: str | None
    score_gate: str | None
    margin_gate: str | None
    capacity_gate: str | None
    capacity_requirement: str | None
    human_approval_gate: str | None
    min_margin: float
    gate_exception_role: str
    margin_exception_role: str
    condition_categories: tuple[ConditionCategory, ...]
    min_conditions: int
    data_note_required: tuple[str, ...]
    data_note_forbidden: tuple[str, ...]
    raw: dict[str, Any]

    @property
    def gate_ids(self) -> frozenset[str]:
        return frozenset(gate.id for gate in self.gates)

    @property
    def criterion_ids(self) -> tuple[str, ...]:
        return tuple(criterion.id for criterion in self.criteria)

    @property
    def weights(self) -> dict[str, float]:
        return {criterion.id: criterion.weight for criterion in self.criteria}

    @property
    def criterion_labels(self) -> dict[str, str]:
        return {criterion.id: criterion.label for criterion in self.criteria}

    @property
    def gate_labels(self) -> dict[str, str]:
        return {gate.id: gate.text for gate in self.gates}


def _require(mapping: dict[str, Any], key: str, kind: type, context: str) -> Any:
    if key not in mapping:
        raise PolicyError(f"{context} missing required field: {key}")
    value = mapping[key]
    if not isinstance(value, kind):
        raise PolicyError(f"{context}.{key} has the wrong type")
    return value


def _unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        raise PolicyError(f"{label} contains duplicate ids")


def policy_from_dict(data: dict[str, Any]) -> Policy:
    if not isinstance(data, dict):
        raise PolicyError("policy must be a JSON object")

    decision = _require(data, "decision", dict, "policy")
    requirements = _require(data, "requirements", dict, "policy")
    scoring = _require(data, "scoring", dict, "policy")
    gates_data = _require(data, "gates", list, "policy")
    gate_rules = _require(data, "gate_rules", dict, "policy")

    thresholds = _require(data, "thresholds", dict, "policy")
    conditions = _require(data, "conditions", dict, "policy")
    data_note = _require(data, "data_note", dict, "policy")

    criteria = tuple(
        Criterion(
            id=str(_require(item, "id", str, "scoring.criteria[]")),
            label=str(_require(item, "label", str, "scoring.criteria[]")),
            weight=float(_require(item, "weight", (int, float), "scoring.criteria[]")),
        )
        for item in scoring.get("criteria", [])
    )
    if not criteria:
        raise PolicyError("scoring.criteria must not be empty")
    _unique([criterion.id for criterion in criteria], "scoring.criteria")
    if abs(sum(criterion.weight for criterion in criteria) - 100) > 0.01:
        raise PolicyError("scoring.criteria weights must sum to 100")

    gates = tuple(
        Gate(
            id=str(_require(item, "id", str, "gates[]")),
            text=str(_require(item, "text", str, "gates[]")),
            type=str(_require(item, "type", str, "gates[]")),
        )
        for item in gates_data
    )
    if not gates:
        raise PolicyError("gates must not be empty")
    _unique([gate.id for gate in gates], "gates")

    categories = []
    for item in conditions.get("categories", []):
        keywords = item.get("keywords")
        if not isinstance(keywords, list) or not keywords:
            raise PolicyError("conditions.categories[].keywords must be a non-empty list")
        normalized = tuple(tuple(str(part).lower() for part in group) for group in keywords)
        categories.append(
            ConditionCategory(
                id=str(_require(item, "id", str, "conditions.categories[]")),
                label=str(_require(item, "label", str, "conditions.categories[]")),
                keywords=normalized,
            )
        )
    if not categories:
        raise PolicyError("conditions.categories must not be empty")
    _unique([category.id for category in categories], "conditions.categories")

    requirement_ids = tuple(str(item) for item in requirements.get("ids", []))
    if not requirement_ids:
        raise PolicyError("requirements.ids must not be empty")
    _unique(list(requirement_ids), "requirements.ids")

    gate_ids = {gate.id for gate in gates}

    def optional_gate(rule: str) -> str | None:
        value = gate_rules.get(rule)
        if value is None:
            return None
        if not isinstance(value, str):
            raise PolicyError(f"gate_rules.{rule} must be a string or null")
        if value not in gate_ids:
            raise PolicyError(f"gate_rules.{rule} references unknown gate: {value}")
        return value

    requirements_gate = optional_gate("requirements_gate")
    score_gate = optional_gate("score_gate")
    margin_gate = optional_gate("margin_gate")
    capacity_gate = optional_gate("capacity_gate")
    human_approval_gate = optional_gate("human_approval_gate")

    capacity_requirement_value = gate_rules.get("capacity_requirement")
    if capacity_requirement_value is not None:
        if not isinstance(capacity_requirement_value, str):
            raise PolicyError("gate_rules.capacity_requirement must be a string or null")
        if capacity_requirement_value not in requirement_ids:
            raise PolicyError(
                "gate_rules.capacity_requirement references unknown requirement: "
                f"{capacity_requirement_value}"
            )
    capacity_requirement = capacity_requirement_value
    if capacity_gate is not None and capacity_requirement is None:
        raise PolicyError("gate_rules.capacity_gate requires capacity_requirement")
    if capacity_gate is None and capacity_requirement is not None:
        raise PolicyError("gate_rules.capacity_requirement requires capacity_gate")

    return Policy(
        policy_id=str(_require(data, "policy_id", str, "policy")),
        policy_version=str(_require(data, "policy_version", str, "policy")),
        description=str(data.get("description", "")),
        decision_options=tuple(str(item) for item in _require(decision, "options", list, "decision")),
        bid_decisions=frozenset(str(item) for item in _require(decision, "bid_options", list, "decision")),
        no_bid=str(_require(decision, "no_bid", str, "decision")),
        fallback_required_for=frozenset(
            str(item) for item in decision.get("fallback_required_for", [])
        ),
        requirement_ids=requirement_ids,
        requirement_statuses=frozenset(
            str(item) for item in _require(requirements, "statuses", list, "requirements")
        ),
        base_partner_status=str(
            _require(requirements, "base_partner_status", str, "requirements")
        ),
        blocking_statuses=frozenset(
            str(item) for item in _require(requirements, "blocking_statuses", list, "requirements")
        ),
        criteria=criteria,
        min_score=float(_require(scoring, "minimum_score", (int, float), "scoring")),
        score_formula=str(scoring.get("formula", "weighted_sum_div_5")),
        gates=gates,
        requirements_gate=requirements_gate,
        score_gate=score_gate,
        margin_gate=margin_gate,
        capacity_gate=capacity_gate,
        capacity_requirement=capacity_requirement,
        human_approval_gate=human_approval_gate,
        min_margin=float(
            _require(thresholds, "minimum_margin_percent", (int, float), "thresholds")
        ),
        gate_exception_role=str(
            _require(thresholds, "gate_exception_role", str, "thresholds")
        ),
        margin_exception_role=str(
            _require(thresholds, "margin_exception_role", str, "thresholds")
        ),
        condition_categories=tuple(categories),
        min_conditions=int(_require(conditions, "minimum_count", int, "conditions")),
        data_note_required=tuple(
            str(item) for item in _require(data_note, "required_any", list, "data_note")
        ),
        data_note_forbidden=tuple(
            str(item) for item in _require(data_note, "forbidden_any", list, "data_note")
        ),
        raw=data,
    )


def load_policy(path: str | Path) -> Policy:
    policy_path = Path(path)
    try:
        data = json.loads(policy_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise PolicyError(f"could not read policy {policy_path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise PolicyError(f"invalid policy JSON in {policy_path}: {exc}") from exc
    return policy_from_dict(data)
