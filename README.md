# Codex agent configuration

Global instructions, seven native Codex agent profiles, and an example configuration.

Use this package to give Codex consistent rules for delegating work, checking
results, and recovering from interrupted tasks. The profiles become available
for delegation; copying the files does not start agents or install plugins.

## What's included

- [`AGENTS.md`](AGENTS.md): how Codex owns a task, delegates it, and verifies completion.
- [`agents/`](agents): specialist profiles for discovery, implementation, tests, review, and local diagnostics.
- [`config.example.toml`](config.example.toml): settings to review and merge into your own configuration.
- [`policy/repair-lifecycle.md`](policy/repair-lifecycle.md): recovery rules loaded when a task needs durable state or safe retries.

## Install or update

Use a Codex version that supports `AGENTS.md` and custom native agents. Review
these files before installing. For an existing setup, compare and merge your
local changes first; run the copy commands only for files you intend to replace.

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
`config.toml`; preserve existing account, marketplace, and project settings.
For updates, pull the existing checkout and review the diff before copying
files. Start a new Codex session to load the changes.

## Model selection

The main session uses the model and reasoning level selected in your Codex
configuration or UI. These lines are commented out in the example, so copying
it does not select Astra. Enable them only if your installation supports them:

```toml
model = "gpt-6-astra"
model_reasoning_effort = "ultra"
```

All seven files in `agents/` explicitly set both model and effort, as listed
below. Those file settings take precedence when that custom agent is selected.
Native agents without such overrides can inherit the parent's settings;
explicit spawn settings and `[agents]` defaults also affect that inheritance.
See [Codex custom-agent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents).

## Optional agents

| Role | Configured model | Effort | Configured sandbox | Intended use |
| --- | --- | --- | --- | --- |
| `source_explorer` | `gpt-5.6-luna` | `medium` | read-only | Direct repository reconstruction and impact evidence. |
| `codeindexer_explorer` | `gpt-5.6-luna` | `medium` | read-only | Indexed semantic, symbol, and dependency discovery. |
| `mech_executor` | `gpt-5.6-terra` | `medium` | workspace-write | One bounded implementation after explicit edit-custody transfer. |
| `test_runner` | `gpt-5.6-luna` | `low` | workspace-write | Tests, builds, linters, and smoke checks without source edits. |
| `reviewer` | `gpt-5.6-terra` | `high` | read-only | Independent correctness and regression review. |
| `security_reviewer` | `gpt-5.6-sol` | `high` | read-only | Focused security, privacy, credential, and authorization review. |
| `scout` | `gpt-5.6-luna` | `medium` | read-only | Local runtime and operational-state observation. |

The sandbox column records the values in the files. A parent's live permission
settings can override those defaults. The test runner's ban on source edits is
an instruction; `workspace-write` permits filesystem writes for test artifacts.

## Example settings and integrations

- Native delegation is limited to four concurrent child threads and one level
  of nesting. These are native Codex limits, separate from Claude worker capacity.
- The example sets `service_tier = "default"`. Its delegation hint is for
  hosts using `multi_agent_v2`; the template does not enable that feature.
- The two MCP entries configure OpenAI documentation and a local CodeIndexer
  endpoint. Keep only the entries you use; CodeIndexer must already be running
  at the configured address for indexed discovery.
- Nine plugin entries enable artifact tools, browser tools, and the Claude
  orchestrator. They assume those plugins are installed in their named
  marketplaces; the entries do not install them. Merge only the ones you use.

Claude Code workers are provided and configured by the separate
[orchestrator plugin](https://github.com/coredo-eu/codex-claude-orchestrator).
This repository's seven TOML profiles describe native Codex agents.

## Validate

With Python 3.11 or newer:

```sh
python3 scripts/validate.py
```

The validator checks TOML, the seven profiles, the matching README table, and
the shared task contract. It does not test model access, plugin installation,
MCP connectivity, or runtime permission enforcement.

## Related repositories

- [Codex Claude Orchestrator](https://github.com/coredo-eu/codex-claude-orchestrator): runs Claude workers under Codex and returns results for verification.
- [Claude agent configuration](https://github.com/coredo-eu/claude-agent-config): instructions and specialist agents for standalone Claude Code.
