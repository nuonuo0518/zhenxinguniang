# Step V-05: Traceability Validation

## Goal
Validate the requirements chain: Vision → User Journeys → Functional Requirements. Identify broken chains and orphan requirements.

## Process

### 1. Build Traceability Map

Read the following sections from the document:
- User Journeys (extract: each journey, who does what)
- Functional Requirements (extract: each FR, labeled or numbered)
- Product Scope (extract: in-scope items)

### 2. Validate Chain: User Journeys → Functional Requirements

Ask: Is each step in every User Journey backed by at least one FR?

- For each User Journey step, identify the FR(s) that enable it
- Flag orphan journey steps: journey steps with no supporting FR
- Flag orphan FRs: FRs that don't support any user journey or business goal
- Flag journey gaps: implied journeys that should exist but are missing

### 3. Validate Chain: Product Scope → FRs

Ask: Is each in-scope item from Product Scope covered by at least one FR?

- Check in-scope list against FRs
- Flag scope items with no corresponding FR

### 4. Count Orphans

Total orphan count:
- Orphan FRs (no traceable source): ___
- Journey steps without FRs: ___
- Scope items without FRs: ___

### 7. Classify Severity

**Critical (>5 orphan FRs):**
- Requirements chain is broken
- Design work will produce features with no clear purpose
- Must fix traceability before proceeding

**Warning (2-5 orphans):**
- Some gaps in requirements chain
- Risk of building features without clear justification
- Should improve before development

**Pass (0-1 orphans):**
- Requirements chain is intact
- Each requirement traces back to a user need or business goal

## Append to Report

```
## Traceability Validation (Step 5)

**Chain Validation:**
- User Journeys → FRs: {✓/⚠/❌}
- Product Scope → FRs: {✓/⚠/❌}

**Orphan FRs ({count}):**
- FR: "..." — No user journey or business goal traces to this

**Journey Steps Without FRs ({count}):**
- Journey X, Step Y: "..." — No FR enables this action

**Total Orphans:** {count}

**Severity:** {CRITICAL | WARNING | PASS}
**Status:** ✓ Proceeding to Implementation Leakage Validation
```

## Output

- ✓ Full traceability matrix built
- ✓ All chains validated
- ✓ Orphans identified with specific references
- ✓ Severity classified
- ✓ Findings appended to report

## Next Step

→ Execute `step-v-06-implementation-leakage-validation.md`

## Checkpoint

Before proceeding to Step 6, output this line verbatim (fill in the numbers):

```
✅ Checkpoint Step V-05: FRs traced {traced_fr_count}/{total_fr_count}, journey steps checked {checked_journey_steps}/{total_journey_steps}, orphan count {orphan_count}
```

Completion conditions:
- `traced_fr_count == total_fr_count` (every FR has been evaluated for traceability — no skipping)
- `checked_journey_steps == total_journey_steps` (every journey step has been checked against FRs)
- `orphan_count == orphan_fr_count + journey_gap_count + scope_gap_count`

If any condition fails, re-examine the skipped items before continuing.

## Important Constraints

- **Do NOT** load step-v-06 before completing this step
- **Do NOT** modify the document
- **Do** trace every FR — no skipping
- **Do** be specific about which FR/journey is orphaned
