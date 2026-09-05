# Codex agent configuration

Reusable instructions and seven optional specialist agents for Codex.

Use this package to give Codex consistent rules for delegating work, checking
results, and recovering from interrupted tasks. Codex chooses only the agents
that help with the task; installing the catalog does not start them all.

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

mkdir -p ~/.codex/agents ~/.codex/policy
install -m 0644 AGENTS.md ~/.codex/AGENTS.md
install -m 0644 policy/repair-lifecycle.md ~/.codex/policy/repair-lifecycle.md
install -m 0644 agents/*.toml ~/.codex/agents/
```

For another profile, use its `CODEX_HOME` directory instead of `~/.codex`.
Merge the settings you need from `config.example.toml`; keep your account,
marketplace, and project settings. On updates, pull the repository, review the
differences, and copy only the intended changes. Start a new Codex session.

## Model selection

The example leaves the main model and reasoning level unchanged. It includes
this commented option for installations that offer GPT-6 Astra:

```toml
model = "gpt-6-astra"
model_reasoning_effort = "ultra"
```

Changing the main model does not change specialist models or Claude workers.
Each specialist keeps the settings in its own profile. Adjust those separately
if the model is unavailable in your installation.

## Optional agents

| Role | Default model | Effort | Sandbox | Intended use |
| --- | --- | --- | --- | --- |
| `source_explorer` | `gpt-5.6-luna` | `medium` | read-only | Direct repository reconstruction and impact evidence. |
| `codeindexer_explorer` | `gpt-5.6-luna` | `medium` | read-only | Indexed semantic, symbol, and dependency discovery. |
| `mech_executor` | `gpt-5.6-terra` | `medium` | workspace-write | One bounded implementation after explicit edit-custody transfer. |
| `test_runner` | `gpt-5.6-luna` | `low` | workspace-write | Tests, builds, linters, and smoke checks without source edits. |
| `reviewer` | `gpt-5.6-terra` | `high` | read-only | Independent correctness and regression review. |
| `security_reviewer` | `gpt-5.6-sol` | `high` | read-only | Focused security, privacy, credential, and authorization review. |
| `scout` | `gpt-5.6-luna` | `medium` | read-only | Local runtime and operational-state observation. |

This is the canonical semantic taxonomy for the repository family. The related
Claude package supplies equivalent roles in Claude's own format; those files
are intentionally not byte-identical.

CodeIndexer is needed only for indexed discovery. The
[Codex Claude Orchestrator](https://github.com/coredo-eu/codex-claude-orchestrator)
plugin is needed only when you want Codex to delegate work to Claude Code.

## Validate

With Python 3.11 or newer:

```sh
python3 scripts/validate.py
```

The validator checks TOML, the seven agent profiles, their model and permission
settings, and the shared task contract.

## Related repositories

- [Codex Claude Orchestrator](https://github.com/coredo-eu/codex-claude-orchestrator): runs Claude workers under Codex and returns results for verification.
- [Claude agent configuration](https://github.com/coredo-eu/claude-agent-config): instructions and specialist agents for standalone Claude Code.
