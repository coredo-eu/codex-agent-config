# Codex agent configuration

This repository is a portable configuration package for Codex. It provides an
authority and ownership contract plus seven optional specialist role
definitions. It is not an orchestration runtime, and it does not define a
seven-agent pipeline.

## Seven roles, not seven running agents

The role files are a capability catalog. Installing all seven makes them
available to Codex; it does not make Codex launch all seven for every task.

- Most routine tasks should stay with the main Codex session and use no native
  agent at all.
- When delegation has clear value, a task will normally use one bounded
  specialist. Independent read-only investigations may run in parallel when
  that reduces total cost or elapsed time.
- `source_explorer` and `codeindexer_explorer` are alternative discovery paths,
  not consecutive stages.
- `reviewer` and `security_reviewer` are selected only when the consequence and
  uncertainty justify independent review; they are not automatic gates.
- `scout`, `mech_executor`, and `test_runner` cover distinct runtime, edit, and
  verification boundaries. Their availability is not a requirement to invoke
  them.

The intended topology is therefore the smallest useful one: direct Codex by
default, then only the role or roles that materially improve the outcome. Role
count describes available boundaries, not concurrency or workflow length.

## Repository family

- [Codex Claude Orchestrator](https://github.com/coredo-eu/codex-claude-orchestrator) — local Codex-to-Claude worker transport, ownership policy, and lifecycle controls.
- [Codex agent configuration](https://github.com/coredo-eu/codex-agent-config) — portable Codex guidance, native-agent roles, and configuration template.
- [Claude agent configuration](https://github.com/coredo-eu/claude-agent-config) — portable standalone Claude guidance, agents, permissions, and CodeIndexer hook.

The snapshot captures the policy and role definitions that determine how work
is owned, delegated, verified, and handed back. It contains no Codex runtime,
account data, or machine state.

## Operating model

- Codex remains the owner of user intent, architecture decisions, authority,
  conflict resolution, independent verification, and the final verdict.
- An implementation request authorizes the actions necessary to reach its
  unambiguous outcome inside the repositories, remotes, services, environments,
  and accounts already in scope. Codex continues through intermediate stages
  without duplicate confirmation and asks only for a material scope expansion
  or a target or end state that cannot be determined safely.
- Work is delegated only when isolation or parallelism lowers total cost or
  elapsed time without weakening correctness or safety.
- A worktree has one edit-capable owner at a time. Parallel writers use isolated
  roots and return custody explicitly.
- Native agents and Codex-owned Claude workers are bounded executors. They do
  not gain commit, push, deploy, credential, destructive, or production
  authority from their role definition. After edit custody returns, the owning
  Codex session performs any shared or external action already authorized by the
  active goal.
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

These seven roles are the canonical semantic taxonomy for this repository
family. Each product surface supplies an adapter for its own agent names,
tools, permissions, and configuration format: native Codex definitions live in
this repository, while Claude-facing configuration is maintained in its own
repository. The adapters preserve role intent and the goal-contract vocabulary;
they are intentionally not byte-identical configuration files.

## Configuration snapshot

The example records these current choices without copying generated state:

- no top-level model or reasoning-effort override: the main session keeps the
  model and effort selected by the user;
- up to four native agent threads and one level of child delegation;
- official OpenAI developer-documentation MCP;
- loopback CodeIndexer MCP at `http://127.0.0.1:8978/mcp`;
- document, PDF, spreadsheet, presentation, browser, sites, visualization, and
  Codex-Claude orchestrator plugins enabled;
- a bounded `multi_agent_v2` mode hint that treats applicable AGENTS/skill
  routing as sufficient authority for Claude transport without enabling
  proactive native-agent fan-out;
- JS REPL disabled.

The current high-trust `approval_policy` and `sandbox_mode` values are preserved
as comments. They are intentionally not activated by copying the example.
The mode hint customizes a v2 runtime when that runtime is active; it does not
set `features.multi_agent_v2.enabled` or change the selected reasoning effort.
Start a new Codex session after changing global instructions or this setting.

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

Run the deterministic repository validator with Python 3.11 or newer:

```bash
python3 scripts/validate.py
```

It validates the exact seven-role TOML inventory, each role's model, reasoning
effort, and sandbox, plus the canonical goal-contract and README role table.

## Deliberate exclusions

This repository does not contain credentials, licenses, trusted-client
fingerprints, project trust entries, absolute home paths, notifications,
sessions, caches, logs, plugin caches, MCP OAuth state, or generated runtime
files. Those remain owned by each local Codex installation.
