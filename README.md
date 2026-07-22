# Codex agent configuration

Portable snapshot of the current Codex agent-working policy and native agent
roles. This repository contains declarative configuration only.

## Contents

- `AGENTS.md` — global authority, delegation, safety, and verification policy.
- `agents/` — native Codex role definitions.
- `config.example.toml` — portable subset of the active Codex configuration.

## Use

1. Review and copy `AGENTS.md` to `~/.codex/AGENTS.md`.
2. Merge the relevant sections of `config.example.toml` into
   `~/.codex/config.toml`; do not overwrite machine-generated MCP or browser
   settings.
3. Install `codex-claude-orchestrator` from its own repository when Claude PTY
   workers are required.

The high-trust approval and sandbox values are documented but commented out in
the example. Enabling them is a deliberate local decision.

Credentials, licenses, trusted-client fingerprints, project trust entries,
absolute machine paths, sessions, caches, logs, and plugin runtime state are
intentionally excluded.
