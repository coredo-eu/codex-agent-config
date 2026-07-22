# Codex agent configuration

## Repository family

- [Codex Claude Orchestrator](https://github.com/coredo-eu/codex-claude-orchestrator) — local Codex-to-Claude worker transport, ownership policy, and lifecycle controls.
- [Codex agent configuration](https://github.com/coredo-eu/codex-agent-config) — portable Codex guidance, native-agent roles, and configuration template.
- [Claude agent configuration](https://github.com/coredo-eu/claude-agent-config) — portable standalone Claude guidance, agents, permissions, and CodeIndexer hook.

This repository is a portable, public snapshot of an opinionated Codex
agent-working setup. It captures the policy and role definitions that determine
how work is owned, delegated, verified, and handed back. It contains no Codex
runtime, account data, or machine state.

## Operating model

- Codex remains the owner of user intent, architecture decisions, authority,
  conflict resolution, independent verification, and the final verdict.
- Work is delegated only when isolation or parallelism lowers total cost or
  elapsed time without weakening correctness or safety.
- A worktree has one edit-capable owner at a time. Parallel writers use isolated
  roots and return custody explicitly.
- Native agents and Codex-owned Claude workers are bounded executors. They do
  not gain commit, push, deploy, credential, destructive, or production
  authority from their role definition.
- Verification effort follows consequence and uncertainty rather than a fixed
  checklist or task-size label.
- CodeIndexer is an optional discovery and impact-analysis surface. Its index is
  derived evidence; authoritative source and observed runtime remain the SSOT.

The full contract is in [`AGENTS.md`](AGENTS.md).

## Repository contents

| Path | Purpose |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Global authority, delegation, ownership, safety, and verification policy. |
| [`agents/`](agents) | Native Codex role definitions with model, reasoning, sandbox, and bounded instructions. |
| [`config.example.toml`](config.example.toml) | Sanitized, portable subset of the active Codex configuration. |

## Native agent roles

| Role | Default model | Effort | Sandbox | Intended use |
| --- | --- | --- | --- | --- |
| `source_explorer` | `gpt-5.6-luna` | `medium` | read-only | Direct repository reconstruction and impact evidence. |
| `codeindexer_explorer` | `gpt-5.6-luna` | `medium` | read-only | Indexed semantic, symbol, and dependency discovery. |
| `mech_executor` | `gpt-5.6-terra` | `medium` | workspace-write | One bounded implementation after explicit edit-custody transfer. |
| `test_runner` | `gpt-5.6-luna` | `low` | workspace-write | Tests, builds, linters, and smoke checks without source edits. |
| `reviewer` | `gpt-5.6-terra` | `high` | read-only | Independent correctness and regression review. |
| `security_reviewer` | `gpt-5.6-sol` | `high` | read-only | Focused security, privacy, credential, and authorization review. |
| `scout` | `gpt-5.6-luna` | `medium` | read-only | Local runtime and operational-state observation. |

Model identifiers reflect the source environment. Replace them with models
available in the target Codex installation when necessary.

## Configuration snapshot

The example records these current choices without copying generated state:

- no top-level model or reasoning-effort override: the main session keeps the
  model and effort selected by the user;
- up to four native agent threads and one level of child delegation;
- official OpenAI developer-documentation MCP;
- loopback CodeIndexer MCP at `http://127.0.0.1:8978/mcp`;
- document, PDF, spreadsheet, presentation, browser, sites, visualization, and
  Codex-Claude orchestrator plugins enabled;
- JS REPL disabled.

The current high-trust `approval_policy` and `sandbox_mode` values are preserved
as comments. They are intentionally not activated by copying the example.

## Installation

Requirements:

- a Codex installation supporting `AGENTS.md` and native agent definitions;
- CodeIndexer only if the indexed explorer or MCP endpoint is used;
- `codex-claude-orchestrator` only if Codex-owned Claude PTY workers are used.

Clone the repository, review differences against the current local files, and
then install only the parts you want:

```bash
git clone https://github.com/coredo-eu/codex-agent-config.git
cd codex-agent-config

mkdir -p ~/.codex/agents
install -m 0644 AGENTS.md ~/.codex/AGENTS.md
install -m 0644 agents/*.toml ~/.codex/agents/
```

Merge `config.example.toml` into `~/.codex/config.toml` manually. Do not replace
generated marketplace, browser, notification, project-trust, or MCP runtime
entries wholesale.

## Validation

The tracked TOML files can be parsed with Python 3.11 or newer:

```bash
python3 - <<'PY'
import pathlib, tomllib

tomllib.loads(pathlib.Path("config.example.toml").read_text())
for path in pathlib.Path("agents").glob("*.toml"):
    tomllib.loads(path.read_text())
print("configuration: OK")
PY
```

## Deliberate exclusions

This repository does not contain credentials, licenses, trusted-client
fingerprints, project trust entries, absolute home paths, notifications,
sessions, caches, logs, plugin caches, MCP OAuth state, or generated runtime
files. Those remain owned by each local Codex installation.
