"""Command-line interface for BidRoom."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .engine import render_markdown, validate
from .policy import PolicyError, load_policy


def _read_decision(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"ERROR: could not read {path}: {exc}", file=sys.stderr)
        raise SystemExit(2)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        raise SystemExit(2)


def _load_policy(path: str):
    try:
        return load_policy(path)
    except PolicyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)


def _validate(args: argparse.Namespace) -> int:
    policy = _load_policy(args.policy)
    data = _read_decision(args.decision)
    errors = validate(data, policy)
    if errors:
        print("INVALID decision record:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if args.md:
        try:
            Path(args.md).write_text(render_markdown(data, policy), encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: could not write {args.md}: {exc}", file=sys.stderr)
            return 2

    print(
        f"VALID: {data['pursuit']} | {data['decision']} | "
        f"{float(data['total_score']):g}/100"
    )
    return 0


def _check(args: argparse.Namespace) -> int:
    policy = _load_policy(args.policy)
    print(
        f"POLICY: {policy.policy_id} {policy.policy_version} | "
        f"{len(policy.gates)} gates | {len(policy.criteria)} criteria | "
        f"{len(policy.requirement_ids)} requirements | "
        f"{len(policy.condition_categories)} condition categories"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bidroom",
        description="Policy-driven bid/no-bid decision records.",
    )
    parser.add_argument("--version", action="version", version=f"bidroom {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="Validate a decision JSON against a policy."
    )
    validate_parser.add_argument("--policy", required=True, help="Path to policy JSON.")
    validate_parser.add_argument("decision", help="Path to decision JSON.")
    validate_parser.add_argument("--md", help="Optional path for rendered markdown.")
    validate_parser.set_defaults(func=_validate)

    render_parser = subparsers.add_parser(
        "render", help="Render a decision JSON as markdown."
    )
    render_parser.add_argument("--policy", required=True, help="Path to policy JSON.")
    render_parser.add_argument("decision", help="Path to decision JSON.")
    render_parser.add_argument("--md", required=True, help="Path for rendered markdown.")
    render_parser.set_defaults(func=_validate)

    check_parser = subparsers.add_parser(
        "check", help="Check that a policy file loads and summarize it."
    )
    check_parser.add_argument("--policy", required=True, help="Path to policy JSON.")
    check_parser.set_defaults(func=_check)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
