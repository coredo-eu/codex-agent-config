# Repair-line lifecycle and failure recovery

For multi-stage or replay-sensitive implementation, use one durable lifecycle
when it materially improves continuity or recovery. It is evidence for the
owning model, not a prerequisite for tools or effects. Use the smallest
project-native representation: routine single-pass local work may keep
identities in-session and must not create tracking as ceremony. Persist useful
state before custody/window transfer and after ambiguous effects when doing so
improves recovery.

- Keep identity layers separate: `goal_id` identifies the terminal user
  outcome; `repair_line_id` identifies the current implementation line;
  `artifact_digest` identifies immutable exact bytes; and `attempt_id`
  identifies one execution. A nonce, approval, namespace, receipt, session, or
  attempt identifier is never a semantic version.
- Preserve the transition semantics
  `PLANNED -> PREPARED -> EFFECT_IN_PROGRESS -> VERIFYING -> SUCCEEDED`.
  A pre-effect failure returns the same repair line to `REPAIRING`. A failure or
  ambiguity after intent/effect enters `RECOVERING` and reaches an independently
  checked `ROLLED_BACK` or other terminal state before repair or retry. Projects
  may use native state names, but `FAILED -> NEW_VERSION` is not a valid
  transition.
- A rollback closes an attempt, not the goal or repair line. Released artifact
  bytes remain immutable: fixing the current version means minimally changing
  the same repair line and recording a new digest only when bytes changed, not
  overwriting an old digest and not inventing a semantic successor.
- Classify the failure before another effect: candidate code/config defect,
  operator/readiness-contract defect, transient environment failure, ambiguous
  effect state, or business-acceptance failure. Record the evidence and causal
  change that makes the next action different.
  - For a candidate or operator defect, repair the same line, add a targeted
    regression that falsifies that failure class, and reseal only changed bytes.
  - For a transient failure, reuse the same digest and create only a new attempt
    identity when evidence shows retry is safe; rebuilding is not recovery.
  - After ambiguous intent or effect, perform record-bound readback/recovery;
    never blindly replay the effect.
  - A business-acceptance failure remains failed until the same line meets the
    acceptance criteria or the user intentionally changes the goal.
- The same failure class with no new causal evidence is a stop-the-line
  condition: do not rebuild, reseal, retry, deploy, or create another version.
  Continue diagnosis or report the real blocker under the normal goal rules.
- Create a semantic successor only when the authoritative goal, product, API,
  schema, or acceptance contract intentionally changed, or when an explicitly
  chosen material redesign makes the current line obsolete. A byte change that
  repairs the same contract remains on the same line. Record the causal change
  and `supersedes` relation. Concurrency, a new window, timeout, rollback,
  consumed approval, or failed attempt is not such a change.
- Reuse the project's existing connector, roadmap/card, journal, or receipt as
  the durable continuation record; do not create a competing SSOT. It must make
  discoverable the goal and repair-line identities, current digest and attempt,
  lifecycle state, failure class, causal change, owner/lease, terminal receipt,
  `next_allowed_action`, and any `supersedes` relation.
- A new window may use the recorded `next_allowed_action` to avoid repeating
  completed work, but first matches the record to the current goal and live
  state. It may choose a different action whenever current evidence supports
  that judgment. Record changes when useful for continuity; the record is not a
  permission gate.
