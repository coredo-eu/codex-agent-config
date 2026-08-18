#!/usr/bin/env python3
"""Validate the portable semantic role and goal-contract SSOT."""

from __future__ import annotations

import pathlib
import re
import sys
import tomllib


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED_ROLES = {
    "source_explorer": ("gpt-5.6-luna", "medium", "read-only"),
    "codeindexer_explorer": ("gpt-5.6-luna", "medium", "read-only"),
    "mech_executor": ("gpt-5.6-terra", "medium", "workspace-write"),
    "test_runner": ("gpt-5.6-luna", "low", "workspace-write"),
    "reviewer": ("gpt-5.6-terra", "high", "read-only"),
    "security_reviewer": ("gpt-5.6-sol", "high", "read-only"),
    "scout": ("gpt-5.6-luna", "medium", "read-only"),
}
CONTRACT_FIELDS = (
    "Outcome",
    "Done when",
    "Boundaries",
    "Authoritative context",
    "Non-goals",
    "Known evidence",
    "Required handoff",
)
MULTI_AGENT_MODE_HINT = (
    "Applicable AGENTS.md and skill executor-selection rules are explicit delegation "
    "instructions. Follow them without requiring the user to repeat a Claude request. "
    "Codex-owned Claude PTY transport is not native sub-agent fan-out. Otherwise, do "
    "not spawn native Codex sub-agents proactively."
)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_toml() -> None:
    try:
        config = tomllib.loads((ROOT / "config.example.toml").read_text())
    except (OSError, tomllib.TOMLDecodeError) as error:
        fail(f"config.example.toml is not valid TOML: {error}")

    mode_hint = config.get("features", {}).get("multi_agent_v2", {}).get(
        "multi_agent_mode_hint_text"
    )
    if mode_hint != MULTI_AGENT_MODE_HINT:
        fail("config.example.toml must pin the bounded multi-agent runtime hint")

    paths = sorted((ROOT / "agents").glob("*.toml"))
    found = {path.stem for path in paths}
    if found != set(EXPECTED_ROLES):
        fail(f"agent inventory differs: expected {sorted(EXPECTED_ROLES)}, found {sorted(found)}")

    for path in paths:
        try:
            role = tomllib.loads(path.read_text())
        except (OSError, tomllib.TOMLDecodeError) as error:
            fail(f"{path.relative_to(ROOT)} is not valid TOML: {error}")
        expected = EXPECTED_ROLES[path.stem]
        actual = tuple(role.get(key) for key in ("model", "model_reasoning_effort", "sandbox_mode"))
        if role.get("name") != path.stem:
            fail(f"{path.relative_to(ROOT)} name must match its filename")
        if actual != expected:
            fail(f"{path.relative_to(ROOT)} expected {expected}, found {actual}")
        if not role.get("description") or not role.get("developer_instructions"):
            fail(f"{path.relative_to(ROOT)} must have a description and developer instructions")


def validate_docs() -> None:
    agents = (ROOT / "AGENTS.md").read_text()
    contract_start = agents.find("compact contract with these ordered fields:")
    contract_end = agents.find(". A small read-only evidence child", contract_start)
    contract = agents[contract_start:contract_end]
    positions = [contract.find(f"`{field}`") for field in CONTRACT_FIELDS]
    if contract_start == -1 or contract_end == -1 or -1 in positions or positions != sorted(positions):
        fail("AGENTS.md must state the canonical seven-field goal contract in order")
    routing = "`scout` for local operational observation"
    if routing not in agents:
        fail("AGENTS.md native routing must include scout")
    if "without requiring the user to repeat \"use Claude\"" not in agents:
        fail("AGENTS.md must make its Claude routing instruction self-activating")

    readme = (ROOT / "README.md").read_text()
    table_roles = set(re.findall(r"^\| `([a-z_]+)` \| `gpt-", readme, re.MULTILINE))
    if table_roles != set(EXPECTED_ROLES):
        fail(f"README.md role table inventory differs: {sorted(table_roles)}")
    for role, (model, effort, sandbox) in EXPECTED_ROLES.items():
        row = f"| `{role}` | `{model}` | `{effort}` | {sandbox} |"
        if row not in readme:
            fail(f"README.md role table is inconsistent for {role}")
    if "canonical semantic taxonomy" not in readme or "intentionally not byte-identical" not in readme:
        fail("README.md must describe surface-specific adapters without byte-identical claims")


def main() -> None:
    validate_toml()
    validate_docs()
    print(f"validation: OK ({len(EXPECTED_ROLES)} roles, {len(CONTRACT_FIELDS)} contract fields)")


if __name__ == "__main__":
    main()
