# Validate Game PRD/GDD - Workflow

## Overview

This workflow validates an existing game PRD or GDD through 10 sequential validation checks. Each check is self-contained and auto-proceeds without user intervention. Do not get hung up on terminology (PRD vs GDD); treat them interchangeably.

## Behavioral Rules

These rules apply for the entire session and must not relax as the conversation grows longer.

1. ❗ **Every finding must cite a source** — quote the exact line or section from the PRD/GDD that triggered the finding. No source = do not output the finding. Check this before every output.
2. ❗ **Never skip or reorder steps** — execute steps 1–10 in strict sequence; output the Checkpoint line at the end of each step before loading the next step file. Check this before every step transition.
3. ❗ **Never modify the PRD/GDD** — all writes go to the validation report only. Check this before any Write or Edit call.

## Output Constraints

These constraints apply to every response during a validation session.

**Prohibited output:**
- Opening phrases: "让我来分析…" / "首先我们需要…" / "好的，我来帮您…" / "I'll now analyze…"
- Tool call narration: "我将使用 Read 工具读取…" / "Now I will run Grep to search for…"
- Restating what the user just said or what was already in the report
- Padding text between steps: "以上就是第 N 步的分析结果，接下来我们进入第 N+1 步"
- Inventing example violations when no real violations were found
- Expanding a finding beyond what the quoted source supports

**Required for every finding output:**
- Exact quote or section reference from the PRD/GDD (file path + section heading or line number)
- Severity label: `Critical` / `Warning` / `Pass` / `(tentative)`
- One concrete fix suggestion (not "add more detail")

**Step transition output:**
- Output the Checkpoint line verbatim, then load the next step file
- No commentary between Checkpoint and the next step's execution

## Configuration

**Language Configuration (Hardcoded for simplicity):**
- Communication Language: Chinese (中文)
- Document Output Language: Chinese (中文)
- Planning Artifacts: Enabled (生成规划产物)
- Default Complexity: Game projects only

**Note:** This skill is specialized for game projects. If you need to validate non-game PRDs, use the standard `bmad-validate-prd` skill instead.

## Activation Sequence

1. **Initialize validation context:**
   - Language: Chinese
   - Role: Validation Architect & QA Specialist
   - Scope: Game PRD/GDD validation only
   - Report output: **same directory as the validated file**, filename `doc-validation-{YYYY-MM-DD}-{系统名}.md`

2. **Step 1: Discovery**
   - Ask user for PRD/GDD file path
   - Auto-discover from current directory if possible
   - Load document
   - Ask user if there are reference documents
   - Initialize validation report with metadata

3. **Steps 2-9: Validation Checks**
   - Each step is self-contained in its own file
   - Read entire step file before executing
   - Execute step, append findings to report
   - Auto-proceed to next step
   - Never batch multiple steps

4. **Step 10: Report Complete**
   - Run completeness check (template variables, missing sections, Design Purpose)
   - Consolidate all findings from Steps 2–9
   - Generate comprehensive summary
   - Save report to the **same directory as the validated file**, filename: `doc-validation-{YYYY-MM-DD}-{系统名}.md`
     - Example: validating `raw/design/pending/交易行系统/设计案.md` → saves to `raw/design/pending/交易行系统/doc-validation-2026-04-08-交易行系统.md`
   - Display summary to user
   - Ask if user wants detailed findings or help with fixes

## Architecture

### File Organization
```
validate-prd/
├── SKILL.md (this file, defines the skill)
├── workflow.md (this workflow, execution plan)
├── data/
│   └── game-requirements.md (game-specific validation rules)
└── steps-v/
    ├── step-v-01-discovery.md
    ├── step-v-02-format-detection.md
    ├── step-v-03-density-validation.md
    ├── step-v-04-brief-coverage-validation.md
    ├── step-v-05-traceability-validation.md
    ├── step-v-06-implementation-leakage-validation.md
    ├── step-v-07-game-compliance-validation.md
    ├── step-v-08-holistic-quality-validation.md
    ├── step-v-09-completeness-validation.md
    └── step-v-10-report-complete.md
```

### Micro-File Architecture Principles

**Never load multiple steps simultaneously:**
- Load only the current step file
- Read it completely before executing
- Execute and append findings to report
- Move to next step file

**State Management:**
- Validation report frontmatter tracks progress
- Each step appends to the report
- No side effects between steps
- Report file grows incrementally

**No mental todo lists:**
- Don't read future steps and plan ahead
- Each step is fully self-contained
- The step file itself explains what to do
- Follow the step's instructions exactly

## Validation Report Structure

### Frontmatter
```yaml
---
title: PRD Validation Report
validationDate: {YYYY-MM-DD HH:MM:SS}
prdPath: {path to document being validated}
inputDocuments: [list of loaded reference docs]
validationStatus: IN_PROGRESS / COMPLETE
stepsCompleted: [list of completed steps]
overallStatus: PASS / WARNING / CRITICAL
holisticQualityRating: {1-5}
---
```

### Report Sections (Append-Only Building)
1. Validation Summary (updated at end)
2. Step 1: Discovery findings
3. Step 2: Format findings
4. Step 3: Density findings
5. Step 4: Brief Coverage findings
6. Step 5: Traceability findings
7. Step 6: Implementation Leakage findings
8. Step 7: Game Compliance findings
9. Step 8: Holistic Quality findings
10. Step 9: Completeness findings
11. Step 10: Final Summary (conclusions and next steps)

## Data Flow

Each step's input is the **complete output of the previous step** — never re-read the PRD/GDD file or re-search the document from scratch within a step that already has it in context.

| Step | Input source | Output passed to next step |
|------|-------------|---------------------------|
| Step 1 (Discovery) | User-provided path | PRD/GDD content in context + report file path |
| Steps 2–9 (Validation) | PRD/GDD content from Step 1 + report file from Step 1 | Findings appended to report; `stepsCompleted` updated |
| Step 10 (Report Complete) | Report file written by Steps 1–9 | Final report with `validationStatus: COMPLETE` |

**Hard rules:**
- Steps 2–9 must use the PRD/GDD content loaded in Step 1. Do not call Read/Glob/Grep on the PRD/GDD file again in Steps 2–9 unless the content was lost from context (in which case, re-read once and note it).
- Steps 3–10 must reference the **actual** report file path established in Step 1. Do not recompute the path.
- Before appending to the report in any step, verify the report file exists (created by Step 1). If missing, halt and surface the error rather than silently continuing.
- Step 10 must read the report file written by Steps 1–9 — it must not reconstruct findings from memory.

**Cross-step count chain:**
- Each Checkpoint outputs a count (e.g., `FRs traced {n}/{total}`).
- Step 10 Checkpoint verifies `stepsCompleted == 10` before writing COMPLETE status.
- If any count is inconsistent with the previous Checkpoint, surface the discrepancy rather than silently proceeding.

## Tool Priority

Always use the preferred tool first. Only downgrade when the preferred tool fails — and always annotate the downgrade in the report.

| Operation | Preferred | Downgrade Condition | Fallback |
|-----------|-----------|---------------------|---------|
| Read PRD/GDD or step files | Read | Read returns error | Bash `cat` |
| Find candidate PRD/GDD files | Glob | Glob returns 0 results and path is confirmed to exist | Bash `ls` |
| Search for keywords in document | Grep | Grep fails twice consecutively | Bash `grep` |
| Write validation report (new file) | Write | — | — |
| Update report frontmatter / append section | Edit | `old_string` not unique → expand context | Retry Edit with larger context |

**Rules:**
- A single timeout ≠ tool unavailable. Retry once before downgrading.
- When downgrading, append to the report: `⚠️ 降级: [工具] 不可用，原因: [原因]`
- Never use Bash `sed` or `awk` as a substitute for Edit.
- Never read the PRD/GDD file more than once per step — reuse the content already in context.

## Key Constraints

**Hard Rules:**
- NEVER skip steps
- NEVER batch multiple steps
- NEVER read multiple step files at once
- NEVER execute before reading entire step file
- NEVER load config.yaml (hardcoded values instead)
- NEVER call external skills or workflows
- NEVER write directly to PRD/GDD (only to validation report)

**Soft Guidelines:**
- Use Chinese for all communication and output
- Append findings incrementally to report
- Ask user one question at a time (via AskUserQuestion tool)
- Explain findings conversationally
- Suggest improvements in priority order

## Decision Gate

This skill outputs several types of strong conclusions (severity verdicts, quality ratings, orphan judgments, leakage flags). Each must follow the signal → evidence → counter-evidence → decision chain. A signal alone is never enough to output a finding.

**Core rule**: If evidence is missing or counter-evidence was not checked, the conclusion is at most `tentative` and must be labelled as such. Do not output `Critical` or `Warning` without quoted source evidence.

### Claim types and required evidence

| Claim type | Example conclusion | Required evidence | Counter-evidence to check |
|---|---|---|---|
| `structural` | Section missing / heading unnumbered | Exact heading list or absence confirmed by scanning the full document | Could it be present under a different title? (semantic match, not just exact header) |
| `semantic` | Requirement is ambiguous / contradictory | Quote both sides of the contradiction, or the specific vague term + why it's underspecified | Does surrounding context resolve the ambiguity? |
| `relational` | FR has no user journey trace / orphan FR | Map of all UJs → FRs showing the gap | Is there an implicit business goal in Product Scope that covers it? |
| `authority` | Technology term is implementation leakage | Exact quote of the term + section it appears in | Is it in a clearly labelled "Technical Notes" section where implementation detail is expected? |

### Severity assignment rules

- **Critical**: `evidence.completeness == complete` AND counter-evidence checked AND the issue directly blocks a developer from implementing correctly or safely.
- **Warning**: `evidence.completeness == partial` OR issue is present but context partially resolves it.
- **Pass**: No evidence of the issue found after full scan.
- **tentative**: Evidence exists but counter-evidence was not checked — must be labelled `(tentative)` in the report.

### Zero-result handling

| Situation | Correct output | Prohibited output |
|---|---|---|
| Scan found no violations | "扫描完成，未发现违规项" | Inventing example violations to seem thorough |
| Step file unreadable | "⚠️ 降级: step file 不可读，跳过该维度" | Guessing what the step would have found |
| FR count is zero | "文档未包含可识别的 FR 列表" | Treating all document text as FRs |

## Next Steps After Validation

**If validation PASSES:**
→ Document ready for design/implementation

**If validation has WARNINGS:**
→ User reviews top 3 improvements and fixes them
→ Optional: Re-run validation to confirm fixes

**If validation has CRITICAL issues:**
→ User fixes blocking issues
→ User may need to restructure sections
→ Optional: Re-run validation after major revisions

## Termination

Validation ends after Step 10 (Report Complete). The skill does NOT:
- Invoke other skills
- Modify the original document
- Create design documents
- Launch editing workflows

User receives a comprehensive report saved to the same directory as the validated PRD/GDD file (filename: `doc-validation-{YYYY-MM-DD}-{系统名}.md`) for reference during design and implementation phases.
