# Step V-04: Brief Coverage Validation

## Goal
Check if the document covers all Product Brief content (if brief exists).

## Process

### 1. Check for Product Brief

Look at inputDocuments loaded in Step 1. Identify if any document is a Product Brief, Vision Doc, or similar upstream planning document.

**If no brief found:**
- Mark step as: "N/A - No product brief provided"
- Skip to report append section
- Auto-proceed to Step 5

**If brief found:**
- Load brief content
- Extract brief sections (see below)
- Map each to document content

### 2. Extract Brief Sections

Read the Product Brief for these elements:
- **Vision statement** — What problem does this product solve? What future does it enable?
- **Target users** — Who is this for? Player personas?
- **Problem statement** — What pain point or opportunity is addressed?
- **Key features** — Core capabilities the product must have
- **Goals/objectives** — Business and user success criteria
- **Differentiators** — What makes this unique? Why build this vs. alternatives?

### 3. Map to Document Content

For each brief element, search the document for corresponding content:

| Brief Element | Coverage |
|---------------|----------|
| Vision statement | Fully Covered / Partially Covered / Not Found |
| Target users | Fully Covered / Partially Covered / Not Found |
| Problem statement | Fully Covered / Partially Covered / Not Found |
| Key features | Fully Covered / Partially Covered / Not Found |
| Goals/objectives | Fully Covered / Partially Covered / Not Found |
| Differentiators | Fully Covered / Partially Covered / Not Found |

**Coverage Definitions:**
- **Fully Covered** — Document explicitly addresses this element with sufficient detail
- **Partially Covered** — Document mentions it but lacks depth or specifics
- **Not Found** — Document does not address this at all
- **Intentionally Excluded** — Document notes this is out of scope (acceptable)

### 4. Classify Severity

**Critical:**
- Vision statement Not Found
- Goals/objectives Not Found
- More than 2 elements Not Found

**Warning:**
- Target users Partially Covered
- Key features Partially Covered
- 1-2 elements Not Found (non-critical)

**Pass:**
- All elements Fully Covered or Intentionally Excluded
- At most 1 element Partially Covered

## Append to Report

```
## Brief Coverage Validation (Step 4)

**Product Brief Status:** {Found at: path | Not Found — N/A}

{If brief found:}
**Coverage Map:**
- Vision statement: {✓ Fully Covered | ⚠ Partially | ❌ Not Found}
- Target users: {✓/⚠/❌}
- Problem statement: {✓/⚠/❌}
- Key features: {✓/⚠/❌}
- Goals/objectives: {✓/⚠/❌}
- Differentiators: {✓/⚠/❌}

**Gaps:**
- {Element}: {Why it's missing or incomplete}

**Severity:** {N/A | CRITICAL | WARNING | PASS}
**Status:** ✓ Proceeding to Traceability Validation
```

## Output

- ✓ Brief coverage assessed (or N/A confirmed)
- ✓ Gaps identified and documented
- ✓ Severity classified
- ✓ Findings appended to report

## Next Step

→ Execute `step-v-05-traceability-validation.md`

## Important Constraints

- **Do NOT** load step-v-05 before completing this step
- **Do NOT** modify the document or brief
- **Do** mark N/A and auto-proceed if no brief exists
- **Do** read entire step file before executing
