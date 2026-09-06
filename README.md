# Codex agent configuration

## Project family

- [codex-agent-config](https://github.com/coredo-eu/codex-agent-config) — Codex instructions and native specialist profiles.
- [claude-agent-config](https://github.com/coredo-eu/claude-agent-config) — standalone Claude Code instructions and specialist agents.
- [codex-claude-orchestrator](https://github.com/coredo-eu/codex-claude-orchestrator) — Codex plugin that delegates local tasks to Claude Code and returns results for Codex verification.

Together, these projects form the **COREDO agent tools family**: two
configuration packages and one installable Codex plugin. Use each on its own
or combine them. The orchestrator requires Claude Code, but does not require
`claude-agent-config`; it supplies its own worker instructions and roles.

## What it does

This package gives Codex global instructions, seven native specialist agent
profiles, and an example configuration for delegating work, checking results,
and recovering from interrupted tasks. Copying these files makes the profiles
available for delegation; it does not start agents, install plugins, or
change your selected main-session model.

## What's included

| Path | Purpose |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | How Codex owns a task, delegates it, and verifies completion. |
| [`agents/`](agents) | Seven specialist profiles for discovery, implementation, tests, review, and local diagnostics. |
| [`config.example.toml`](config.example.toml) | Settings to review and merge into your own configuration. |
| [`policy/repair-lifecycle.md`](policy/repair-lifecycle.md) | Recovery rules loaded when a task needs durable state or safe retries. |

### Agent roles

| Role | Configured model | Effort | Configured sandbox | Intended use |
| --- | --- | --- | --- | --- |
| `source_explorer` | `gpt-5.6-luna` | `medium` | read-only | Direct repository reconstruction and impact evidence. |
| `codeindexer_explorer` | `gpt-5.6-luna` | `medium` | read-only | Indexed semantic, symbol, and dependency discovery. |
| `mech_executor` | `gpt-5.6-terra` | `medium` | workspace-write | One bounded implementation after explicit edit-custody transfer. |
| `test_runner` | `gpt-5.6-luna` | `low` | workspace-write | Tests, builds, linters, and smoke checks without source edits. |
| `reviewer` | `gpt-5.6-terra` | `high` | read-only | Independent correctness and regression review. |
| `security_reviewer` | `gpt-5.6-sol` | `high` | read-only | Focused security, privacy, credential, and authorization review. |
| `scout` | `gpt-5.6-luna` | `medium` | read-only | Local runtime and operational-state observation. |

The sandbox column records the values in the files; a parent's live permission
settings can override those defaults. The test runner's ban on source edits is
an instruction, not an enforced restriction — `workspace-write` still permits
filesystem writes for test artifacts. All seven files explicitly set both
model and effort for the selected role. Profiles without those overrides can
inherit the parent session's settings; explicit spawn settings and agent
defaults can also affect inheritance.

### Example settings

The configuration template includes:

- a limit of four concurrent native child threads and one level of nesting;
- `service_tier = "default"` and a delegation hint for hosts using
  `multi_agent_v2` (the hint does not enable that feature);
- optional MCP entries for OpenAI documentation and a local CodeIndexer
  endpoint, which must already be running;
- nine optional plugin entries, which enable plugins already installed in
  their named marketplaces.

Merge only the entries you use.

## Installation

Use a Codex version that supports `AGENTS.md` and custom native agents.
Review these files before installing, and for an existing setup compare and
merge your local changes first — run the copy commands only for files you
intend to replace.

```sh
git clone https://github.com/coredo-eu/codex-agent-config.git
cd codex-agent-config

codex_config_dir="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$codex_config_dir/agents" "$codex_config_dir/policy"
install -m 0644 AGENTS.md "$codex_config_dir/AGENTS.md"
install -m 0644 policy/repair-lifecycle.md "$codex_config_dir/policy/repair-lifecycle.md"
install -m 0644 agents/*.toml "$codex_config_dir/agents/"
```

The commands use `CODEX_HOME` when set, otherwise `~/.codex`. Separately merge
the settings you need from `config.example.toml` into that directory's
`config.toml`, preserving existing account, marketplace, and project settings.
For updates, pull the existing checkout and review the diff before copying
files again, then start a new Codex session to load the changes.

## Usage

Once installed, ask Codex to delegate work; `AGENTS.md` governs how it owns a
task, chooses a profile from `agents/`, and verifies the result before calling
it complete. The main session uses the model and reasoning level selected in Codex.
The example contains these commented settings; they do not select a model
unless you enable them:

```toml
model = "gpt-6-astra"
model_reasoning_effort = "ultra"
```

Enable those two lines only if your installation actually supports that model
and effort. Explicit spawn settings and `[agents]` defaults also affect
inheritance — see
[Codex custom-agent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents).

## Validation

With Python 3.11 or newer:

```sh
python3 scripts/validate.py
```

The validator checks TOML, the seven profiles, the matching README table, and
the shared task contract. It does not test model access, plugin installation,
MCP connectivity, or runtime permission enforcement.

## Further reading

- [codex-claude-orchestrator](https://github.com/coredo-eu/codex-claude-orchestrator): runs Claude workers under Codex and returns results for verification.
- [claude-agent-config](https://github.com/coredo-eu/claude-agent-config): instructions and specialist agents for standalone Claude Code.
- [Codex custom-agent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)
