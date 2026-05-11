# Step V-09: Completeness Validation

## Goal
Final comprehensive completeness check — no template variables remaining, all required sections have substantive content.

## Process

### 1. Scan for Template Variables

Search the entire document for unfilled placeholders:
- `{variable}` patterns
- `{{variable}}` patterns
- `[placeholder]` patterns
- `<TODO>` or `<TBD>` markers
- `TBD`, `TODO`, `PLACEHOLDER`, `TO BE DETERMINED` (as standalone text)
- `...` used as placeholder content (not in prose)
- `N/A` in mandatory fields

For each found, record:
- Location (section + approximate line)
- The placeholder text
- What content is needed there

### 2. Validate Section Completeness

Check that each required section has substantive content (not just a header with a placeholder):

**Product Scope:**
- Contains **Design Purpose (设计目的)**: clearly states WHY this feature/system is being built — the business motivation, player pain point being solved, or strategic goal it serves. This is not a restatement of scope; it answers "why are we doing this at all?" A Product Scope section without a design purpose is incomplete because readers (designers, developers, QA) need to understand the intent behind the feature to make correct trade-off decisions during implementation.
- Defines in-scope features (what IS in the game)
- Defines out-of-scope items (what is NOT in this version)
- Describes MVP vs. full vision (if applicable)

**User Journeys:**
- At least 2 player journeys documented
- Each journey has step-by-step flow
- Journeys cover key game interactions (onboarding, core loop, endgame)

**Functional Requirements:**
- At least 5 FRs listed
- Each FR follows `[Actor] can [capability]` format
- FRs cover all major features described in user journeys

**Non-Functional Requirements:**
- Performance targets present (FPS, load times, memory)
- Platform targets defined
- Scale targets present (if applicable: concurrent players, save data size)

**Game-Specific Sections:**
- Game Mechanics: Core loop described, not just named
- Progression: Specific targets, not just "players progress"
- Reminders & Onboarding: Red dot logic and tutorial structure defined

### 3. Classify Severity

**Critical:**
- Template variables in core requirements sections
- Mandatory sections have only placeholders (no real content)
- Product Scope missing **Design Purpose (设计目的)** — no explanation of why the feature is being built

**Warning:**
- Template variables in non-critical sections
- Some sections have thin content (present but minimal)

**Pass:**
- No template variables found
- All sections have substantive content

## Append to Report

```
## Completeness Validation (Step 9)

**Template Variables Found:** {count}
{If count > 0:}
- Section X: "{placeholder text}" — Needs: {what should go here}
- Section Y: "{placeholder text}" — Needs: {what should go here}

**Section Completeness:**
- Product Scope: {✓/⚠/❌}
- User Journeys: {✓/⚠/❌}
- Functional Requirements: {✓/⚠/❌}
- Non-Functional Requirements: {✓/⚠/❌}
- Game Mechanics: {✓/⚠/❌}
- Progression & Balance: {✓/⚠/❌}
- Reminders & Onboarding: {✓/⚠/❌}

**Overall Completeness:** {X}% sections fully complete

**Severity:** {CRITICAL | WARNING | PASS}
**Status:** ✓ Proceeding to Report Generation
```

## Output

- ✓ Full document scanned for template variables
- ✓ All required sections checked for content
- ✓ Completeness percentage calculated
- ✓ Severity classified
- ✓ Findings appended to report

## Next Step

→ Execute `step-v-10-report-complete.md`

## Important Constraints

- **Do NOT** load step-v-10 before completing this step
- **Do NOT** modify the document
- **Do** scan the full document — don't sample
- **Do** distinguish "thin but real content" (Warning) from "placeholder only" (Critical)
