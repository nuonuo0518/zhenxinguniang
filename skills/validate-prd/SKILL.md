---
name: 设计文档审查
description: >
  Validates an existing game project PRD or GDD for production readiness. Runs a comprehensive
  10-step review covering information density, clarity & ambiguity, traceability, implementation
  leakage, game-domain compliance, and holistic quality. Use when the user asks to validate,
  review, audit, check, score, or verify a game PRD, GDD, requirements doc, or design spec —
  especially phrases like "验证设计案", "检查PRD质量", "审查需求文档", "这份文档能不能进开发",
  "PRD写得怎么样", "review this GDD", "is this PRD production-ready", "check requirements doc".
  Do not use for: drafting or writing a new PRD/GDD from scratch; general writing polish or
  grammar fixes; validating non-game PRDs (SaaS, enterprise, mobile apps without game mechanics);
  code review; UX specification; implementation planning; or discussing what a good PRD looks like
  in the abstract.
---

# Validate Game PRD/GDD

## Overview

Validate an existing game project PRD (Product Requirements Document) or GDD (Game Design Document) through a comprehensive 10-step review process. This skill ensures the document is clear, traceable, and ready for design and implementation. (Note: Do not get hung up on whether the document is called a PRD or GDD—treat them equally.)

The workflow automatically performs:
- Information density check (no fluff)
- Clarity & ambiguity check (no vague or contradictory expressions)
- Traceability chain verification
- Domain-specific game requirements
- Holistic quality assessment

## Checklist

You MUST complete these 10 steps in order:

1. **Discovery** — Load PRD/GDD and input documents
2. **Format Detection** — Verify document structure
3. **Density Validation** — Check for fluff and wordy phrases
4. **Clarity & Ambiguity** — Detect vague, contradictory, or underspecified expressions
5. **Brief Coverage** — Validate coverage of product brief (if provided)
6. **Traceability** — Validate requirement chains (User Journeys → FRs)
7. **Implementation Leakage** — Ensure no implementation details in FRs/NFRs
8. **Domain Compliance** — Validate game-specific requirements present
9. **Holistic Quality** — Multi-perspective assessment of document
10. **Report Complete** — Final completeness check + comprehensive validation report

## Process Flow

```
Step 1: Discovery (Load PRD/GDD)
   ↓
Step 2: Format Detection (Check structure)
   ↓
Step 3: Density Validation (Scan for fluff)
   ↓
Step 4: Clarity & Ambiguity (Scan for vague/contradictory expressions)
   ↓
Step 5: Brief Coverage (Cross-check with brief, if exists)
   ↓
Step 6: Traceability (User Journeys → FRs)
   ↓
Step 7: Implementation Leakage (No technology names in FRs)
   ↓
Step 8: Game Domain Compliance (Game-specific sections)
   ↓
Step 9: Holistic Quality (Cohesion, audience effectiveness)
   ↓
Step 10: Report Complete (Completeness check + summarize findings)
```

## The Process

**Starting validation:**
- Ask user for PRD/GDD file path (or auto-discover from current directory)
- Load document and check if it's a valid document
- Ask if user has referenced documents (product brief, vision doc, etc.) to load for cross-checking
- Initialize validation report

**Running 9 validation checks (Steps 2–9):**
- Each check runs automatically without user interaction
- Each check appends findings to the validation report
- Checks identify violations, categorize severity (Critical/Warning/Pass), and suggest improvements

**Generating final report (Step 10):**
- Run completeness check (template variables, missing sections, Design Purpose)
- Consolidate all findings from Steps 2–9
- Calculate overall status (Pass/Warning/Critical)
- Summarize: top strengths, critical issues, top 3 improvements
- Save report to the **same directory as the validated file**, filename: `doc-validation-{YYYY-MM-DD}-{系统名}.md`
  - Example: validating `raw/design/pending/交易行系统/设计案.md` → saves to `raw/design/pending/交易行系统/doc-validation-2026-04-08-交易行系统.md`
- Display report summary and save location
- **Report language: Chinese (中文)**

## Validation Checks

Full criteria, examples, and severity rules for each check are in `references/checks-overview.md`. Read it when the user asks what the skill checks, or before answering questions about specific validation criteria.

Quick summary: Steps 2–9 cover format, density, ambiguity, brief coverage, traceability, implementation leakage, game compliance, and holistic quality. Step 10 runs completeness checks and generates the final report.

## Output

Validation report saved to the same directory as the validated PRD/GDD file:
`doc-validation-{YYYY-MM-DD}-{系统名}.md`

Report language: **Chinese (中文)**. Contains: Overall Status, Quick Results Table, Critical Issues, Warnings, Strengths, Quality Rating (1–5), Top 3 Improvements, Full Findings per step.

## Game PRD/GDD Standards

See `references/checks-overview.md` for full standards and tips. In brief: include Game Mechanics, Progression & Balance, and Reminders & Onboarding with specific numbers — not vague descriptions.

## Key Principles

- ❗ **Complete file reading** — Read entire step file before executing; never execute a step from memory
- ❗ **Sequential execution** — No skipping steps, no reordering; output Checkpoint before loading next step
- **Auto-proceeding** — Each check runs without user interaction between steps
- **Clear findings** — All violations include line numbers and specific suggestions
- **Actionable output** — Severity levels and prioritized improvements guide fixes
- **No implementation details** — Document stays at WHAT level, never HOW

## Before You Run This Skill

**Have ready:**
- PRD or GDD file (in Markdown)
- Optional: Product Brief or Vision document for cross-reference
- Optional: Existing design docs

**Document should include:**
- All 4 required sections (Product Scope, User Journeys, FRs, NFRs)
- **Design Purpose (设计目的)** in the Product Scope section
- Game-specific sections (Mechanics, Balance, Reminders & Onboarding, etc.)

## After Validation

- **PASS**: Ready for design phase. Proceed to design system or architecture planning.
- **WARNINGS**: Fix top 3 improvements, then optionally re-run to confirm.
- **CRITICAL**: Fix blocking issues before proceeding. Re-run to verify fixes.

See `references/checks-overview.md` for authoring tips.
