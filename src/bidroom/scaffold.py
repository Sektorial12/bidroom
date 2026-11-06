"""Project scaffolding and project checks."""

from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path

from .policy import PolicyError, load_policy

TEMPLATES = Path(__file__).resolve().parent / "templates"


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "bidroom-project"


def _replace(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def _write_template(source: Path, target: Path, values: dict[str, str]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_replace(source.read_text(encoding="utf-8"), values), encoding="utf-8")


def init_project(
    target: str | Path,
    *,
    name: str,
    owner: str,
    force: bool = False,
) -> Path:
    target_path = Path(target)
    if target_path.exists() and any(target_path.iterdir()) and not force:
        raise FileExistsError(f"{target_path} already exists and is not empty; use --force to overwrite")

    project_id = _slug(name)
    values = {
        "project_id": project_id,
        "project_name": name,
        "decision_owner": owner,
        "date": date.today().isoformat(),
    }

    target_path.mkdir(parents=True, exist_ok=True)
    (target_path / "sources").mkdir(exist_ok=True)
    (target_path / "rooms").mkdir(exist_ok=True)
    (target_path / "agents").mkdir(exist_ok=True)
    (target_path / "records").mkdir(exist_ok=True)

    _write_template(TEMPLATES / "project" / "README.md", target_path / "README.md", values)
    _write_template(TEMPLATES / "project" / "policy.json", target_path / "policy.json", values)
    _write_template(
        TEMPLATES / "project" / "sources" / "README.md",
        target_path / "sources" / "README.md",
        values,
    )
    for template in sorted((TEMPLATES / "rooms").glob("*.md")):
        _write_template(template, target_path / "rooms" / template.name, values)
    for template in sorted((TEMPLATES / "agents").glob("*.md")):
        _write_template(template, target_path / "agents" / template.name, values)

    (target_path / "sources" / "rfp.md").write_text(
        f"# {name} — Source document\n\nReplace this file with the solicitation or opportunity document.\n",
        encoding="utf-8",
    )
    (target_path / "sources" / "capabilities.md").write_text(
        f"# {name} — Bidder evidence\n\nReplace this file with the bidder's capability, reference, capacity, and commercial evidence.\n",
        encoding="utf-8",
    )
    (target_path / "sources" / "policy.md").write_text(
        f"# {name} — Bid policy\n\nReplace this file with the human-readable policy. Keep `policy.json` in sync.\n",
        encoding="utf-8",
    )
    (target_path / "records" / "README.md").write_text(
        "# Records\n\nValidated decision records and rendered markdown live here.\n",
        encoding="utf-8",
    )

    manifest = {
        "schema_version": "1.0",
        "project_id": project_id,
        "project_name": name,
        "decision_owner": owner,
        "policy": "policy.json",
        "rooms": {
            "intake": "bid-intake",
            "review": "bid-review",
            "record": "bid-record",
        },
        "sources": {
            "intake": ["sources/rfp.md", "sources/capabilities.md"],
            "review": ["sources/policy.md", "sources/capabilities.md"],
            "record": [],
        },
    }
    (target_path / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return target_path


def check_project(project: str | Path) -> list[str]:
    project_path = Path(project)
    manifest_path = project_path / "manifest.json"
    if not manifest_path.exists():
        return [f"missing manifest: {manifest_path}"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid manifest JSON: {exc}"]

    errors: list[str] = []
    policy_path = project_path / str(manifest.get("policy", ""))
    try:
        load_policy(policy_path)
    except PolicyError as exc:
        errors.append(str(exc))

    for group, paths in manifest.get("sources", {}).items():
        for relative in paths:
            if not (project_path / relative).exists():
                errors.append(f"missing source for {group}: {relative}")

    for room, room_name in manifest.get("rooms", {}).items():
        if not room_name:
            errors.append(f"missing room name for {room}")
    return errors
