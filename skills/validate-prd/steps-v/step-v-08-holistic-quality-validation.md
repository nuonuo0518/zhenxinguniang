# Step V-08: Holistic Quality Assessment

## Goal
Assess the document as a cohesive, compelling piece of work across multiple perspectives. This is a qualitative judgment step — assign a 1-5 quality rating and identify the top 3 improvements that would have the most impact.

## Why This Step Exists
Individual validation checks (density, traceability) catch specific violations. But a document can pass all checks and still be a poor piece of work — unclear narrative, inconsistent tone, confusing structure, or missing the "so what?" for stakeholders.

This step looks at the whole picture.

## Process

### 1. Read the Entire Document

Read the document from beginning to end as a reader, not as a checker. Try to understand:
- What game is being built?
- Who plays it?
- Why would they care?
- Could a developer build this from the document alone?

### 2. Evaluate: Document Flow & Coherence (Rate 1-5)

Ask:
- Does the document tell a coherent story from vision to requirements?
- Are transitions between sections clear and logical?
- Is terminology consistent throughout (same terms used for same concepts)?
- Is the document organized in a way that serves the reader's mental model?
- Can you read it front-to-back without confusion?

**功能需求章节专项检查（三原则）：**

检查功能需求下的每个模块是否违反以下任一原则：

- **原则一：引导段落缺失** — 模块标题后直接跟表格或列表，中间没有说明该模块是什么、边界在哪里的引导文字。读者在没有框架的情况下被迫消化规格细节。
- **原则二：子层级缺失** — 模块内有多个可独立命名的子能力（超过一张表格或三个段落），但没有用子标题拆分，导致读者无法从目录定位，只能靠滚动发现。
- **原则三：交叉引用替代了就地说明** — 提到其他模块的规则时，只写「见模块X」，没有在当前位置给出一句核心概述，读者必须跳转才能理解当前内容。

每发现一处违反，记录为 Warning；功能需求章节内超过 3 处违反，升级为 Critical 并在 Top 3 Improvements 中列出。

| Score | Meaning |
|-------|---------|
| 5 | Flows beautifully; reads as a unified vision；功能需求每个模块均有引导段落，层级清晰，无强制跳转 |
| 4 | Minor inconsistencies; mostly coherent；功能需求偶有引导段落缺失，但不影响整体理解 |
| 3 | Some sections feel disconnected or repetitive；功能需求多处直接跳入表格，读者需要自行建立上下文 |
| 2 | Significant structural issues; hard to follow；功能需求普遍缺少引导，层级混乱，交叉引用堆叠 |
| 1 | Incoherent; contradictions, missing context；功能需求无任何引导段落，模块间全靠跳转，无法独立阅读 |

### 3. Evaluate: Dual Audience Effectiveness (Rate 1-5)

A game PRD/GDD serves two audiences:
- **Humans**: Producers, designers, developers, stakeholders
- **LLMs**: AI coding tools, AI design tools, AI agents building from this spec

Ask for Human readability:
- Would a non-technical stakeholder understand the game vision?
- Would a designer know what to wireframe?
- Would a developer know what to build?

Ask for LLM readability:
- Are requirements unambiguous enough for an LLM to act on?
- Is the structure machine-parseable (clear sections, consistent formatting)?
- Would an AI generate consistent outputs across multiple reads of this document?
- **流程与机制脱节**：用户旅程的「系统响应」描述是否隐含了特定技术假设（如"返回界面后看到"暗含需手动刷新）？这类描述会让 LLM 生成与实际机制不符的实现。
- **只定义正向、遗漏反向**：规则描述是否只说了"满足条件时怎样"，没有说"不满足时怎样"？单向规则会让 LLM 无法处理边界情况。
- **措辞歧义**：是否存在使用"各自""分别""独立"等词但未说明各自标准的表述？歧义描述会让 LLM 在不同位置生成矛盾实现。

| Score | Meaning |
|-------|---------|
| 5 | Crystal clear for both humans and LLMs |
| 4 | Good for one audience, minor gaps for other |
| 3 | Adequate for humans, LLMs may misinterpret |
| 2 | Confusing for at least one audience |
| 1 | Would produce inconsistent outputs from either audience |

### 4. Evaluate: Writing Quality Compliance (Rate 1-5)

Check overall document quality:
- Information density (minimal fluff across full document)
- Traceability (chain intact from user journeys to FRs)
- Domain awareness (game-specific content is thorough)
- Zero anti-patterns (no subjective claims, vague terms)
- Dual audience optimization (humans and LLMs)
- Markdown formatting (clean, consistent, scannable)

| Score | Meaning |
|-------|---------|
| 5 | Exemplary quality across all dimensions |
| 4 | Strong quality, minor deviations |
| 3 | Acceptable; several dimensions partially met |
| 2 | Significant gaps in quality |
| 1 | Poor quality document |

### 5. Calculate Overall Quality Rating

Overall Rating = weighted synthesis of all three perspectives:

**5/5 — Excellent:**
- All three scores ≥ 4
- Document is production-ready
- Could be used as template for future documents

**4/5 — Good:**
- All three scores ≥ 3, at least one ≥ 4
- Ready for design with minor improvements
- Top 3 improvements would be "nice to have"

**3/5 — Adequate:**
- All three scores ≥ 2, some gaps
- Usable but needs revision before development
- Top 3 improvements are "should have"

**2/5 — Needs Work:**
- One or more scores = 1-2
- Significant gaps blocking effective use
- Top 3 improvements are "must have before design"

**1/5 — Problematic:**
- Multiple scores = 1
- Major structural or content issues
- Requires near-complete rewrite

### 6. Identify Top 3 Improvements

Based on all validation findings (steps 3-7) AND this holistic assessment, identify the 3 improvements that would have the biggest positive impact on overall quality:

Prioritize improvements that:
- Fix Critical severity issues from earlier steps
- Raise quality rating by at least 0.5 points
- Are actionable (author can implement without a design decision)
- Address the biggest gaps in dual-audience effectiveness

Format each improvement as:
1. **{Section or aspect}**: {Specific actionable change} → {Expected impact}

## Append to Report

```
## Holistic Quality Assessment (Step 8)

**Multi-Perspective Ratings:**

### Document Flow & Coherence
Rating: {X}/5
Observations: {1-2 sentences on what works and what doesn't}

#### 功能需求三原则违反
- 原则一（引导段落缺失）：{N} 处
- 原则二（子层级缺失）：{N} 处
- 原则三（交叉引用替代就地说明）：{N} 处
- Severity: {WARNING（1-3 处）/ CRITICAL（>3 处）}

### Dual Audience Effectiveness
Rating: {X}/5
Observations: {Human clarity and LLM-readiness assessment}

### Writing Quality Compliance
Rating: {X}/5
Observations: {Where quality is strong and where it falls short}

---

**Overall Quality Rating: {X}/5**

### Top 3 Improvements (Prioritized by Impact)
1. **{Section}**: {Specific change} → {Expected outcome}
2. **{Section}**: {Specific change} → {Expected outcome}
3. **{Section}**: {Specific change} → {Expected outcome}

### Strengths
- {Specific thing the document does well}
- {Specific thing the document does well}
- {Specific thing the document does well}

**Status:** ✓ Proceeding to Completeness Validation
```

## Output

- ✓ All three dimensions rated 1-5
- ✓ Overall quality rating assigned
- ✓ Top 3 improvements identified with impact explanation
- ✓ Strengths documented
- ✓ Findings appended to report

## Next Step

→ Execute `step-v-09-completeness-validation.md`

## Checkpoint

Before proceeding to Step 9, output this line verbatim (fill in the values):

```
✅ Checkpoint Step V-08: flow {flow_score}/5, dual-audience {audience_score}/5, writing-quality {writing_score}/5, overall {overall_rating}/5, top-3-improvements listed {yes/no}
```

Completion conditions:
- All three dimension scores assigned (1–5 each)
- Overall quality rating assigned (1–5)
- `top-3-improvements listed == yes` (specific actionable items, not "add more detail")

## Important Constraints

- **Do NOT** load step-v-09 before completing this step
- **Do NOT** just average the scores mechanically — use judgment
- **Do** read the entire document before rating, not just flagged sections
- **Do** make improvements specific and actionable, not generic ("add more detail")
