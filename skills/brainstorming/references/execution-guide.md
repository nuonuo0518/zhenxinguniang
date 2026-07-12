# Execution Guide

Follow this guide during brainstorming execution. Do not skip steps.

## Dependency contract

- Step 2 input = Step 1 confirmed context sources. If `context_sources_read == 0`, Step 2 may narrow scope only from explicit user-provided context and must keep missing repo facts unresolved.
- Step 3 input = Step 2 output where `current_slice_count == 1`. If the slice is still broad, keep `visual_mode=deferred` and continue clarifying instead of branching visually.
- Step 5 input = unresolved questions from Steps 2-3. Do not reopen already confirmed boundaries unless new evidence appears.
- Step 6 input = Step 5 output where `open_core_questions == 0` and `visual_mode != deferred`. Do not manufacture approaches before those gates pass.
- Step 7 input = approved approach directions and confirmed constraints from Steps 3-6. Reuse those confirmed constraints instead of regenerating them from memory.
- Step 8 input = Step 7 approved sections + `approved_doc_path_count == 1`.
- Step 9 input = the written spec produced in Step 8, not a fresh rewrite from memory.
- Step 10 input = the self-reviewed Step 9 spec. `approval_gates_passed == 2` must equal `(conversation design approval + written spec approval)`.
- Step 11 input = Step 10 passed state only. Do not invoke `writing-plans` early.
- Cross-check before moving on:
  - before Step 6: `open_core_questions == 0` and `visual_mode != deferred`
  - before Step 8: `approved_required_sections == planned_required_sections`
  - before Step 10: `written_required_sections == template_required_sections`
  - before Step 11: `approval_gates_passed == 2`

## Evidence and zero-result handling

- If reads/searches return no useful project evidence, state what is missing and continue with explicit user-provided context instead of inventing facts.
- If evidence is partial, keep the recommendation or scope cut `tentative`.
- If evidence is blocked or missing, keep the state `unresolved`.
- Use `💡 general pattern` only for reusable advice that is not being claimed as a project fact.
- Do not turn a signal-only impression into a final recommendation; first collect evidence and do the downside counter-check.
- Result labels:
  - confirmed facts / approved constraints: no label
  - partial evidence: `tentative`
  - blocked or missing evidence: `unresolved`
  - reusable general advice: `💡 general pattern`

| Situation | Correct response | Do not do |
|---|---|---|
| Missing project artifact or repo context | State what is missing and continue with user-provided context | Invent project-specific flows or architecture |
| Scope signal without enough evidence | Ask one clarifying question or keep the scope decision `tentative` | Force a slice as if already confirmed |
| Visual branch lacks spatial evidence | Stay in terminal text mode until the spatial question is clear | Force a visual round because UI words appeared |
| Recommendation lacks downside counter-check | Present it as `tentative` and keep probing | Present it as the final choice |

## Step 1: Explore project context
- Read the current project artifacts first: relevant files, docs, and recent commits when available.
- Completion condition: `context_sources_read >= 1` unless the user provided all needed context directly.
- Failure path: if the repo/context is too thin, state what is missing and continue with user-provided context instead of guessing.
- ✅ Checkpoint: `Step 1 complete: read X context sources`

## Step 2: Assess scope boundaries
- Decide whether the request spans multiple low-coupling subsystems, multiple phases, or multiple user journeys.
- If yes, narrow the current slice with one `AskUserQuestion` before going deeper.
- Completion condition: `current_slice_count == 1` for this round.
- Failure path: if the user keeps the scope intentionally broad, mark the extra areas as later design items instead of merging them into one oversized spec.
- ✅ Checkpoint: `Step 2 complete: slice_count=1, deferred_items=Y`

## Step 3: Decide whether a visual round helps
- Treat this as a gated decision, not an early guess.
- Only branch into visual aid when seeing the options would help more than reading text.
- Before asking about a visual round, confirm the **minimum decision context**:
  1. `current_slice_count == 1`
  2. You can name the target surface being designed (for example: list/detail layout, entry placement, modal vs page)
  3. The remaining uncertainty contains **any** spatial/visual dimension — even if the primary question is about config structure or rules, a secondary visual dimension counts. See the visual signal checklist below.
- **Visual signal checklist** — fire `ui_presence_probe` if ANY of these are true:
  - The request includes screenshots, mockups, or reference images (even as examples or context)
  - The request describes on-screen elements with visual behavior: overlays, highlights, rings, tooltips, text boxes, animations, transitions, popups
  - The request mentions layout, position, direction, size, or anchor relationships between UI elements
  - The system being designed renders something the player sees and interacts with visually
  - Note: config structure, API contracts, business rules, and number values alone are NOT visual signals — but if they coexist with any of the above, the visual signal still fires
- Then classify UI complexity:
  - **trivial UI**: a simple confirmation dialog, a single lightweight popup, a one-field action, or another surface with no meaningful spatial trade-off
  - **non-trivial UI**: list/detail, multi-area layout, modal vs page, multiple states, branching flow, or 1-3 UI directions worth comparing; any system with multiple on-screen elements whose spatial relationship is a design decision
- If the minimum decision context is not ready, set `visual_mode=deferred`, continue clarifying in text, and revisit this step before proposing approaches.
- Once the minimum decision context is ready:
  - if the UI is **non-trivial**, use the UI-presence probe and visual signal table in `references/questioning-guide.md`, then ask one `AskUserQuestion` to confirm whether the user wants a visual round
  - if the UI is **trivial**, you may set `visual_mode=no` without asking unless the user explicitly wants a visual round
- Read `references/visual-companion.md` only when the user explicitly wants the visual branch.
- Completion condition:
  - `visual_mode in {yes,no,deferred}`
  - if `ui_presence_probe_fired == true`, then `asked_visual_round_question == true`
  - before Step 4 and Step 6, `visual_mode in {yes,no}`
- Failure path: if `ui_presence_probe_fired == true` and you have not asked the visual-round question yet, stop and ask one explicit visual-round question before proceeding.
- ✅ Checkpoint: `Step 3 complete: visual_mode={yes|no|deferred}, asked_visual_round_question={true|false}`

## Step 4: Confirm doc save location
- Ask where the design doc should be saved before drafting it.
- Do not confirm doc save location while `visual_mode == deferred`.
- Completion condition: `approved_doc_path_count == 1`.
- Failure path: if the user does not care, propose one concrete default path and wait for confirmation before writing.
- ✅ Checkpoint: `Step 4 complete: approved_doc_path=...`

## Step 5: Ask clarifying questions
- Ask one `AskUserQuestion` per turn.
- **For every question, include your recommended answer.** State it as a concrete recommendation (e.g., "我建议：独立页面，原因是……"), not a hedge. The user can agree, modify, or reject — but they should never face a blank question.
- **Respect dependency order.** Upstream decisions must be confirmed before asking downstream questions that depend on them. If a question's answer changes depending on something still unresolved, hold that question until the upstream decision is settled.
- **Check the codebase before asking.** If the answer can be derived from reading code or project files (e.g., existing entry points, current data structures, related systems), read first and cite what you found in your recommendation. Do not ask the user something you can look up yourself.
- Resolve purpose, constraints, success criteria, and any still-open boundary questions.
- If Step 3 was deferred, use this step to gather the minimum decision context, then revisit Step 3 before proposing approaches.
- Load `references/questioning-guide.md` when rewriting an existing doc or when entrance/game-system/trap/UI-presence signals appear.
- Completion condition: `open_core_questions == 0` and `visual_mode != deferred` before Step 6.
- Failure path: if uncertainty remains, do not recommend an approach yet; keep the state tentative and ask the next highest-value question.
- ✅ Checkpoint: `Step 5 complete: open_core_questions=0, visual_mode!=deferred`

## Step 6: Propose 2-3 approaches
- Present 2-3 distinct approaches unless only one is actually viable.
- Evaluate each approach from 4 angles: technical, UX, business, edge cases.
- Completion condition: `2 <= approach_count <= 3`, or `approach_count == 1` with an explicit reason the others are not viable.
- Failure path: if evidence is too weak to compare approaches, ask another clarifying question instead of manufacturing options.
- ✅ Checkpoint: `Step 6 complete: approach_count=X`

## Step 7: Present the design in sections
- Present the design in scoped sections and get user confirmation as you go.
- The minimum required design coverage is: 产品范围, 用户旅程, 功能需求.
- Completion condition: `approved_required_sections == planned_required_sections`.
- Failure path: if the user rejects a section, revise that section before moving to the next one.
- ✅ Checkpoint: `Step 7 complete: approved_sections=X/Y`

## Step 8: Write the design doc
- Write the draft only after the path is confirmed.
- Read `references/design-doc-template.md` before drafting.
- Completion condition: `written_required_sections == template_required_sections`.
- Failure path: if the approved path becomes invalid, pause and reconfirm the save path instead of writing elsewhere.
- ✅ Checkpoint: `Step 8 complete: written_sections=X/Y`

## Step 9: Self-review the written spec
- Check at least these categories: placeholders/TODOs, contradictions, ambiguity, scope creep, and whether the spec is still small enough for the next planning step.
- Completion condition: `review_categories_checked == 5` and `blocking_issues_remaining == 0`.
- Failure path: if review finds issues, fix them inline before showing the doc to the user.
- ✅ Checkpoint: `Step 9 complete: blocking_issues_remaining=0`

## Step 10: Get final spec approval
- The written Markdown spec needs its own explicit approval gate.
- Completion condition: `approval_gates_passed == 2` where the two gates are `(conversation design approval, written spec approval)`.
- Failure path: if the user spots a mismatch, update the doc first and ask for approval again.
- ✅ Checkpoint: `Step 10 complete: approval_gates_passed=2`

## Step 11: Transition to implementation
- Only after Step 10 is complete, commit the design doc and invoke `writing-plans` if available.
- Completion condition: `ready_for_implementation == true`.
- Failure path: if `writing-plans` is unavailable, end gracefully and state that the approved design is ready for implementation planning.
- ✅ Checkpoint: `Step 11 complete: ready_for_implementation=true`
