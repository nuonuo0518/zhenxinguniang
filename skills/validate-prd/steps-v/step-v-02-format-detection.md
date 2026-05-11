# Step V-02: Format Detection

## Goal
Detect document structure compliance and route appropriately (Standard/Variant/Non-Standard).

## Process

### 1. Extract PRD Structure

Extract all Level 2 headers (`##`) from the document:
```
Examples from Document:
## Product Scope
## User Journeys
## Functional Requirements
## Non-Functional Requirements
## Game Mechanics
## Balance & Progression
```

### 2. Check for Core Sections

Identify which of the 4 core sections are present:
1. Product Scope
2. User Journeys
3. Functional Requirements
4. Non-Functional Requirements

Count: ___ / 4 sections found

### 3. Classify Format

**Standard:** 3-4 core sections present
- ✓ Format is compliant with standards
- → Proceed to Step 3 (Density Validation)

**Variant:** 2 core sections present
- ⚠ Format is partially compliant
- Some core sections missing or combined
- → Proceed to Step 3 (Density Validation)
- Note in report: "Document follows variant structure (X/4 core sections)"

**Non-Standard:** <2 core sections present
- ❌ Format does not follow standard structure
- → Offer user menu choices (see below)

### 4. Non-Standard Route Menu (if applicable)

If format is Non-Standard, present menu:

```
您的文档（无论是称为 PRD 还是 GDD）不完全符合标准格式（少于 2 个核心章节）

选择以下选项：
[P] Parity Check: 分析距离标准还差什么
[A] As-Is: 继续验证当前格式（可能得分较低）
[X] Exit: 退出验证，返回编辑文档结构
```

**Option P (Parity Check):** 
→ Analyze gaps and suggest effort to reach parity
→ Proceed to Step 3 (Density Validation)

**Option A (As-Is):**
→ Note in report: "Validating non-standard document format"
→ Proceed to Step 3 (Density Validation)
→ Severity will be marked for missing sections in later steps

**Option X (Exit):**
→ Save report with findings so far
→ Display report path
→ Exit validation workflow

### 5. Section Heading Numbering Validation

All section headings in the document MUST have sequential numeric prefixes. This is not about Markdown `#` levels — it's about the **visible text** of headings having a hierarchical numbering scheme.

**Expected numbering pattern:**
- Level 1 (typically `#` or `##`): `1.标题名`, `2.标题名`, `3.标题名`
- Level 2 (one level deeper): `1.1.标题名`, `1.2.标题名`, `2.1.标题名`
- Level 3 (two levels deeper): `1.1.1.标题名`, `1.2.1.标题名`
- And so on for deeper levels

**How to validate:**

1. Extract all headings from the document (any Markdown `#`, `##`, `###`, etc.)
2. For each heading, check if the text begins with a valid numeric prefix matching pattern: `N.` (level 1), `N.N.` (level 2), `N.N.N.` (level 3), etc.
   - Regex pattern: `^\d+(\.\d+)*\.`
   - The prefix must end with a dot before the title text
3. Verify sequential numbering within each level:
   - Level 1: `1.`, `2.`, `3.` ... (sequential, no gaps)
   - Level 2 under `1.`: `1.1.`, `1.2.`, `1.3.` ...
   - Level 2 under `2.`: `2.1.`, `2.2.` ...
4. Verify parent-child consistency:
   - `2.3.标题` must be nested under a heading starting with `2.`
   - No orphan numbering (e.g., `3.2.1.` without a parent `3.2.`)

**Classification:**
- **Critical:** More than 50% of headings lack numbering, or numbering is chaotic (random numbers, mismatched hierarchy)
- **Warning:** Some headings lack numbering, or minor sequence gaps exist (e.g., jumps from `1.2.` to `1.4.`)
- **Pass:** All headings have correct sequential numbering with consistent hierarchy

**Examples:**

✅ Correct:
```
# 1.产品概述
## 1.1.产品背景
## 1.2.产品目标
# 2.用户旅程
## 2.1.新手引导流程
## 2.2.核心玩法循环
### 2.2.1.匹配系统
### 2.2.2.比赛流程
# 3.功能需求
```

❌ Incorrect (missing numbering):
```
# 产品概述
## 产品背景
## 产品目标
# 用户旅程
```

❌ Incorrect (inconsistent numbering):
```
# 1.产品概述
## 产品背景        ← missing numbering
## 1.2.产品目标
# 3.用户旅程       ← skipped number 2
```

### 6. Report Findings

Append to validation report:
```
## Format Detection (Step 2)

**Core Sections Found:** 4/4
- ✓ Product Scope
- ✓ User Journeys
- ✓ Functional Requirements
- ✓ Non-Functional Requirements

**Game-Specific Sections Found:** 3/3
- ✓ Game Mechanics
- ✓ Balance & Progression
- ✓ Reminders & Onboarding
- {other sections found}

**Heading Numbering:**
- Total headings scanned: {count}
- Correctly numbered: {count} / {total}
- Missing numbering: {list of headings without numeric prefix}
- Sequence errors: {list of numbering gaps or inconsistencies}
- Parent-child mismatches: {list of orphan sub-headings}
- **Numbering Status:** {✓ PASS | ⚠ WARNING | ❌ CRITICAL}

**Format Classification:** Variant (4/4 core sections)
**Status:** ✓ Proceeding to Density Validation
```

## Output

- ✓ Document structure analyzed
- ✓ Format classified
- ✓ Route decision made
- ✓ Findings appended to report

## Next Step

→ Execute `step-v-03-density-validation.md`

## Important Notes

- Game design documents (PRDs/GDDs) may have additional sections beyond the 4 core sections (Mechanics, Balance, Reminders & Onboarding, etc.)
- Standard 4 core sections are still required
- Extra game sections are validation check in Step 7 (Game Compliance), not format detection
