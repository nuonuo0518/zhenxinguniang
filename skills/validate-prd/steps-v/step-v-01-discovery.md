# Step V-01: Discovery

## Goal
Handle fresh context validation by confirming PRD/GDD path, loading input documents, and initializing validation report. Do not get hung up on whether the user calls it a PRD or GDD.

## Process

### 1. Discover PRD/GDD Path

**Option A: Auto-discovery** (if running from game project root)
- Search current directory for `.../docs/prd.md`, `.../docs/gdd.md`, `prd.md`, or `gdd.md`
- Search for files matching pattern `*prd*.md` or `*gdd*.md`

**Option B: User provides path**
- If auto-discovery fails, ask user: "What is the path to your game PRD or GDD file?"
- Example answers: `docs/prd.md`, `design/game-prd.md`, `docs/gdd.md`, `./prd.md`

### 2. Load and Validate Document

- Read file from the provided path
- Check if file exists; if not, ask user to provide correct path
- Read first 200 characters to confirm it's a requirements/design document (should contain "success criteria", "requirements", "gameplay", "design", etc.)

### 3. Check for Input Documents

- Ask user via AskUserQuestion: "Do you have any reference documents to load (e.g., Product Brief, Vision Doc) for cross-checking? If yes, provide paths."
- Example user answers: "docs/product-brief.md, docs/vision.md" OR "No"
- If user provides paths:
  - Check if path exists
  - Load each document into context
  - Track in report

### 4. Initialize Validation Report

Determine the report save path:
- Extract the **system name** from the PRD/GDD file path. Use the parent directory name or the filename stem (strip `.md`).
  - Example: `raw/design/pending/交易行系统/设计案.md` → system name = `交易行系统`
  - Example: `docs/task-system-prd.md` → system name = `task-system-prd`
- Report path: **same directory as the validated file**, filename: `doc-validation-{YYYY-MM-DD}-{系统名}.md`
  - Example: `raw/design/pending/交易行系统/doc-validation-2026-04-08-交易行系统.md`
- If a report file already exists at that path, generate a new filename with the current timestamp to avoid overwriting: `doc-validation-{YYYY-MM-DD}-{系统名}-{HH-MM-SS}.md`

Create the validation report file at the resolved path.

Report frontmatter:
```yaml
---
title: PRD Validation Report
validationDate: {current timestamp in YYYY-MM-DD HH:MM:SS format}
prdPath: {absolute path to document file}
inputDocuments: 
  - {list of loaded reference documents, or "none"}
validationStatus: IN_PROGRESS
stepsCompleted: [step-v-01-discovery]
overallStatus: PENDING
holisticQualityRating: PENDING
---
```

Report body (first section):
```
# PRD/GDD Validation Report

## Discovery (Step 1)

**Document Path:** {path}
**Input Documents Loaded:** {list or "none"}
**Discovery Status:** ✓ Success

### Next Step
Proceeding to Format Detection (Step 2)...
```

### 5. Report Summary

**Display to user (conversationally in Chinese):**
```
✓ 发现阶段完成

发现的内容：
- 文档文件：{path}
- 参考文档：{loaded docs or "无"}
- 验证状态：已初始化

现在进行第2步：格式检测
```

## Output

- ✓ Validation report file created at `{same directory as PRD}/doc-validation-{YYYY-MM-DD}-{系统名}.md`
- ✓ Document loaded into memory
- ✓ Input documents loaded (if present)
- ✓ Report frontmatter initialized
- ✓ Discovery findings appended to report

## Next Step

→ Execute `step-v-02-format-detection.md`

## Error Handling

| Error | Action |
|-------|--------|
| Document file not found | Ask user for correct path, retry |
| Document file is empty | Report error, ask user to check file |
| Reference document not found | Note in report as "Missing: {path}", continue |
| Permission denied reading file | Report error, ask user to check file permissions |

## Important Constraints

- **Do NOT** read future step files
- **Do NOT** try to validate the document yet (that's later steps)
- **Do NOT** modify the document (only read it)
- **Do NOT** skip this step even if document seems obviously malformed
- **Do ONLY** discover, load, and initialize

## Troubleshooting

**User doesn't know their document path:**
- Ask them to find it: "Where did you save your PRD/GDD? Look in /docs or /design folders"
- Accept relative paths: `docs/prd.md` or `docs/gdd.md` will be resolved from project root

**Reference documents missing:**
- This is OK! Note it and continue
- Validation doesn't require reference documents; they're just helpful for cross-checking
