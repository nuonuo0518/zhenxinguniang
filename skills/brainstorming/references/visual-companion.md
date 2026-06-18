# Visual Companion

Use this reference when the current brainstorming question is easier to answer visually than textually.

## Goal

Visual companion is a **lightweight 视觉辅助分支** for brainstorming. Its job is to help the user quickly make decisions about layout, hierarchy, flow, or UI direction. It is **not** a replacement for the main text conversation, the required design sections, or the final written spec approval.

## When to use it

Only enter this branch after the current slice is already narrowed and the unresolved question is clearly spatial. In practice, this usually means the design has reached a non-trivial UI surface where seeing alternatives could help; trivial confirmation-style UI usually does not need this branch unless the user explicitly asks for visuals.

Use a visual round when the user will understand the trade-off faster by **seeing** it:

- 页面布局对比
- 界面信息层级
- 页面流转 / 弹窗 vs 全屏
- 入口位置或导航结构
- 1-3 个视觉方向的快速比较
- 对用户截图、录屏、竞品图做结构化改写或抽象

A good trigger question is:

> 用户看图会不会比看文字更快做出决定？

If the answer is yes, a visual round may help.

## When NOT to use it

Do **not** use visual companion for primarily textual decisions:

- 需求范围澄清
- 业务规则 / 数值规则
- 生命周期 / 边界条件
- 技术方案 / 架构 / 接口
- 配置结构
- 任何可以靠一段清晰文字更快说清的问题

If the core question is conceptual rather than spatial, stay in terminal.

## Fidelity order

The goal is decision-making, not presentation polish. Default to SVG for low-fidelity visuals — it renders inline in most editors, scales without blur, and is far more readable than ASCII for spatial comparisons involving UI elements, icons, overlays, or directional relationships.

1. **SVG 低保真草图** — default choice for any visual round. Write SVG inline and save to a temp file, then open it so the user can see it immediately. Keep it schematic: flat shapes, minimal color, no decoration. This is what "低保真图片草稿" means in practice.
2. **静态 HTML 线框** — when the comparison involves interactive states, hover behavior, or layout that benefits from CSS flow (e.g. flexbox, grid)
3. **ASCII 草图** — only as a fallback when the environment cannot render SVG or HTML (e.g. plain terminal output with no file system access)
4. **基于用户素材的改图** — when the user has already supplied screenshots, mocks, or recordings to annotate or restructure

Do not use ASCII when SVG is available — ASCII loses spatial precision for anything beyond the simplest flow diagram, and the user has already seen that it falls short for UI element placement and directional relationships.

## Visual round workflow

### 1. Isolate one visual decision

Each visual round should answer exactly **one** question, for example:

- 顶部 Tab 还是左侧导航？
- 任务详情放抽屉还是二级页？
- 结算后是弹窗承接还是跳转独立页？

If multiple questions exist, split them across multiple rounds.

### 2. Show 1-3 options max

Present a small number of clearly different directions.

- Label them clearly: A / B / C
- Tell the user what to compare
- Keep the differences focused
- Do not generate many minor variants

### 3. Keep artifacts lightweight

Default assumption: the visual artifact is **static**.

That means:

- no persistent browser server assumption
- no click-event tracking assumption
- no dependency on a custom interaction runtime
- feedback can come back in plain terminal text

If the environment supports richer visual tooling, you may use it. But the skill must still work without it.

### 4. Collect feedback in terminal

Ask the user to respond with the decision or adjustment in text, for example:

- “选 B，但把 CTA 挪到右下角”
- “A 的信息层级对，但入口太深”
- “保留弹窗承接，不要跳全屏页”

Treat terminal feedback as the source of truth.

### 5. Translate the result back into text constraints

After a visual round, summarize the result as explicit design constraints before continuing brainstorming.

Examples:

- 采用顶部 Tab 切换，不使用左侧导航
- 详情区使用右侧抽屉承接，不新增独立二级页
- 结算后通过确认弹窗导向活动，不直接强跳全屏

This step is mandatory. A visual direction that is not written back into text will be lost later.

## Boundaries

Visual companion must respect these limits:

- It does not replace clarifying questions
- It does not replace required design sections
- It does not replace the final Markdown spec
- It does not count as approval by itself
- It should reduce ambiguity, not introduce new scope

## Practical guidance

- Prefer low fidelity over high fidelity
- Prefer comparison over decoration
- Prefer one focused question over a full screen system
- Return to terminal as soon as the visual decision is made
- If the user is already decisive from text alone, skip the visual round entirely
- Do not use warm-up phrases or tool narration around the visual branch
- Show at most 1-3 clearly different options; do not generate cosmetic variants
- If the spatial evidence is still weak, keep the branch `tentative` and return to text clarification instead of forcing visuals

## Example usage patterns

### Pattern A: layout choice
- Produce 2 wireframes: top tabs vs left nav
- Ask user which better matches scanning behavior
- Convert answer into a layout rule

### Pattern B: flow choice
- Produce 2 flow sketches: modal continuation vs full-page continuation
- Ask user which better fits interruption cost and context retention
- Convert answer into a flow rule

### Pattern C: screenshot abstraction
- User supplies竞品截图
- Extract layout blocks and interaction rhythm
- Produce simplified wireframe / flow summary
- Bring the result back into the main design discussion

## Anti-patterns

Avoid these mistakes:

- Using visuals for questions that are really about rules or scope
- Generating many cosmetic variants that do not change the decision
- Spending too much effort polishing mockups before the concept is settled
- Letting the conversation stay in visual mode for too long
- Forgetting to capture the visual decision in the written design
