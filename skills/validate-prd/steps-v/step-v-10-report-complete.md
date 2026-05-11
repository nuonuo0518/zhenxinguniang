# Step V-10: Report Complete

## Goal
Finalize validation report — run completeness checks, consolidate all findings from Steps 1–9, and present actionable next steps.

## Process

### 1. Load Complete Report

Read the validation report file created in Step 1 (same directory as the validated PRD/GDD):
```
{same directory as PRD}/doc-validation-{YYYY-MM-DD}-{系统名}.md
```

### 2. Calculate Overall Status

Aggregate findings from all 9 steps:

**Critical Issues Count:**
- Count all "Critical" severity violations from all steps
- If Critical count > 0: Overall Status = **CRITICAL**

**Warning Issues Count:**
- Count all "Warning" severity violations
- If Critical = 0 AND Warning > 0: Overall Status = **WARNING**

**Pass Condition:**
- If Critical = 0 AND Warning = 0: Overall Status = **PASS**

### 3. Extract Quality Rating

From Step 8 (Holistic Quality Assessment), extract the 1-5 quality rating:
- 5/5: Excellent, production-ready
- 4/5: Good, ready with minor fixes
- 3/5: Adequate, needs revision
- 2/5: Needs work, significant gaps
- 1/5: Problematic, major rework needed

### 4. Build Findings Summary

Create a summary section that lists:

**Overall Status:** {CRITICAL | WARNING | PASS}  
**Quality Rating:** {X}/5  
**Critical Issues:** {count}  
**Warnings:** {count}  

**Critical Issues List** (if any):
- Issue 1: {description} [from which step]
- Issue 2: ...

**Top 3 Improvements** (prioritized by impact):
1. {Improvement} (impacts {which checks})
2. {Improvement} (impacts {which checks})
3. {Improvement} (impacts {which checks})

**Strengths:**
- Strength 1: {what the document does well}
- Strength 2: ...

### 5. Update Report Frontmatter

Update the validation report frontmatter with final status:
```yaml
---
title: PRD/GDD Validation Report
validationDate: {timestamp}
prdPath: {path}
inputDocuments: [loaded docs]
validationStatus: COMPLETE
stepsCompleted: 
  - step-v-01-discovery
  - step-v-02-format-detection
  - step-v-03-density-validation
  - step-v-04-brief-coverage-validation
  - step-v-05-traceability-validation
  - step-v-06-implementation-leakage-validation
  - step-v-07-game-compliance-validation
  - step-v-08-holistic-quality-validation
  - step-v-09-completeness-validation
  - step-v-10-report-complete
overallStatus: {PASS | WARNING | CRITICAL}
holisticQualityRating: {X}/5
---
```

### 6. Add Final Summary Section to Report

Append to report:
```
## Final Summary

**Overall Status:** {CRITICAL | WARNING | PASS}
**Quality Rating:** {X}/5

### Critical Issues
{count} critical issues found:
1. Issue 1
2. Issue 2
...

(If no critical issues: "✓ No critical issues found")

### Warnings
{count} warnings found:
1. Warning 1
2. Warning 2
...

(If no warnings: "✓ No warnings found")

### Top 3 Improvements
1. {Improvement} (Priority: HIGH)
2. {Improvement} (Priority: MEDIUM)
3. {Improvement} (Priority: MEDIUM)

### Strengths
- {Strength 1}
- {Strength 2}
- {Strength 3}

### Recommendations

**If Status is CRITICAL:**
Fix the critical issues before proceeding to design/implementation:
{List which critical issues to fix first}

**If Status is WARNING:**
Recommended improvements before design phase:
{List top 3 improvements in priority order}

**If Status is PASS:**
✓ Document is ready for design and implementation phase
Consider implementing suggested improvements in next iteration

### Next Steps

**For Document Improvements:**
1. Review the detailed findings in sections above
2. Fix issues in priority order (critical → warnings → improvements)
3. Re-run validation to confirm improvements (optional)

**For Design/Implementation:**
- Document is ready for design system creation (Step 3 in brainstorming skill)
- Share this validation report with design and dev teams
- Reference the requirements traceability matrix for mapping FRs to stories

**For Project Management:**
- Track critical issues in project backlog
- Consider sprint planning around document improvement work
- Monitor requirements stability

---

**Validation Report Generated:** {timestamp}  
**Document File:** {path}  
**Report Saved To:** {path to this report file}
```

### 7. Display Summary to User

Present validation findings conversationally (in Chinese):

```
✓ 验证完成

整体状态：{PASS | WARNING | CRITICAL}
质量评分：{X}/5

关键问题：{count} 个
警告：{count} 个
改进建议：3 个

📊 主要问题：
{List top issues}

✨ 优势：
{List strengths}

📝 建议优先改进：
{Top 3 improvements}

完整验证报告已保存到：
{same directory as PRD}/doc-validation-{YYYY-MM-DD}-{系统名}.md

下一步建议：
{Specific recommendations based on status}
```

## Menu Options

Present user with menu:

```
验证完成。您想：

[R] Review Detailed Findings - 逐步查看验证结果（建议）
[C] Copy Report Path - 复制报告文件路径
[X] Exit - 退出验证

请选择 [R/C/X]：
```

**Option R (Review Detailed):**
- Display the full report findings (scroll through step by step)
- Explain each section
- Answer any clarification questions
- After review, offer menu again

**Option C (Copy Path):**
- Display the exact file path to report
- Confirm: "Report path copied: {path}"
- Ask: "Ready to fix issues? (Y/N)"
- If Y: Offer guidance on improvements
- If N: Exit with "Good luck with your document!"

**Option X (Exit):**
- Display message: "验证报告已保存到 {path}。祝您设计顺利！"
- End validation workflow

## Output

- ✓ Validation report complete with all findings
- ✓ Overall status determined (CRITICAL | WARNING | PASS)
- ✓ Quality rating assigned (1-5)
- ✓ Report saved to `{same directory as PRD}/doc-validation-{YYYY-MM-DD}-{系统名}.md`
- ✓ Summary displayed to user
- ✓ Menu presented for next actions

## Checkpoint

Before presenting the user menu, output this line verbatim (fill in the values):

```
✅ Checkpoint Step V-10: stepsCompleted {completed_count}/10, overall-status {PASS|WARNING|CRITICAL}, critical-issues {critical_count}, warnings {warning_count}, quality-rating {X}/5, report-saved {yes/no}
```

Completion conditions:
- `completed_count == 10` (all steps tracked in report frontmatter)
- `report-saved == yes` (file exists at the expected path before showing the menu)
- If `report-saved == no`, write the report file before proceeding

## Important Notes

**This step does NOT:**
- Modify the original document
- Call other skills or workflows
- Generate design documents
- Create implementation plans

**This step IS:**
- The final validation step
- The end of the validation workflow
- A stopping point for user to review and make decisions
- A checkpoint before design/implementation work begins

## Termination

Validation workflow ends after Step 10 (Report Complete) with user's menu choice.
