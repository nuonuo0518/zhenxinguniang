# Questioning Guide

Use this reference during the questioning phase when the default flow is not enough.

## Existing design doc rewrite audit

When the user asks to rewrite an existing design doc to match the required format, compare it against `references/design-doc-template.md` before rewriting.

| Section | What to check |
|------|---------|
| 产品范围 | 是否包含「设计目的」和「系统概述」两个子标题？ |
| 用户旅程 | 每条旅程是否同时包含①界面流转示意（ASCII）②关键步骤表格？ |
| 用户旅程 | 是否残留「目标」「前置条件」等元数据字段？有则删除。 |
| 功能需求 | 是否按模块拆分为小节展开描述？ |
| 功能需求 | 是否按两步法推导：先从用户旅程归纳，再补入数值、限制、生命周期、边界情况等系统内在逻辑？ |
| 功能需求 | 各模块描述是否覆盖了用户旅程中的功能点？ |
| 功能需求 | 是否保留「红点和提醒」固定子模块？无内容时也要写「无」。 |
| 配置结构 | 是否列出涉及的配置表职责与需配置内容，且未写具体表名/字段名？ |
| 决策记录 | 产品范围里写明的 out-of-scope 项，是否在决策记录中有对应条目？ |

输出差距清单后再动笔，不要直接重写。

## AskUserQuestion discipline

- Ask one question per turn.
- **Always include a recommended answer.** State your recommendation concretely ("我建议：X，原因是……") so the user can agree, modify, or reject rather than answer from scratch. This applies to every question — including multiple-choice ones, where you should mark your preferred option.
- **Respect dependency order.** If answering question B depends on knowing the answer to question A, ask A first. Don't ask downstream questions while upstream decisions are still open.
- **Check the codebase before asking.** If the answer is derivable from code or project files, read first and incorporate the finding into your recommendation. Cite what you found (e.g., "查了现有入口，目前只有大厅主按钮，建议……").
- Prefer multiple choice when practical.
- If one topic needs multiple follow-ups, split them across turns.
- Focus on purpose, constraints, success criteria, and missing boundary rules.

## UI-presence probe

Use this probe before silently deciding `visual_mode=no`.

**Precondition: minimum decision context exists first.** Before firing the probe, confirm all three:
1. The current slice is already narrowed enough for this round.
2. You can name the target surface or decision point being designed.
3. What remains unresolved is spatial/visual, not just product rules.

Then check whether the UI is non-trivial. If the surface is already complex enough that seeing options could materially help (for example list/detail, multi-area layout, modal vs page, multiple states, branching flow), ask the visual-round question. If the UI is only a trivial confirmation-style surface with no real layout trade-off, do not force the question unless the user asks for visuals.

- Fire it when the current design already includes UI elements such as `页面` `界面` `弹窗` `抽屉` `Tab` `列表` `详情` `入口` `导航` `卡片` `浮层`, and at least one spatial decision is still open.
- Open spatial decisions include: 页面布局、信息层级、弹窗 vs 全屏、抽屉 vs 二级页、入口位置、或需要 1-3 个 UI 方向快速比较。
- Do **not** fire it when the remaining questions are only about rules, boundaries, numbers, API contracts, or config structure.
- Do **not** fire it just because the user mentioned `列表`/`详情`/`入口` once. If you still do not know what is actually undecided, keep clarifying in text.
- Do **not** silently skip it once all context is ready and the UI is clearly non-trivial; in that case, you should explicitly ask whether the user wants a visual round.
- Suggested follow-up: 「这个点你更想直接用文字定，还是我先给你 2-3 个轻量草图 / ASCII 方案再定？」

### 视觉信号词表

| 信号类型 | 常见词/表达 | 建议动作 |
|---|---|---|
| 布局结构 | `左右分栏` `上下布局` `双栏` `宫格` `卡片列表` `顶部工具栏` `底部操作栏` | 询问是否需要 2-3 个布局草图 |
| 承接形态 | `弹窗` `抽屉` `二级页` `全屏` `浮层` `半屏` | 询问是否要对比承接方式 |
| 导航入口 | `入口` `导航` `Tab` `侧栏` `快捷入口` `悬浮球` `跳转位置` | 询问是否要比较入口/导航位置 |
| 信息层级 | `列表+详情` `概览+详情` `信息层级` `先看什么` `主次信息` | 询问是否要比较信息组织方式 |
| 状态表达 | `状态标签` `状态图标` `红点` `徽标` `禁用态` `空态` | 询问是否要比较视觉表达方案 |
| 方向比较 | `A方案/B方案` `两种布局` `三版草图` `哪个更顺手` `哪个更清晰` | 直接建议开一轮 lightweight visual round |

命中词表本身不等于必须画图；仍需同时满足「当前已有 UI 元素」且「还有未决空间型问题」。纯规则、数值、接口、配置问题不触发 visual round。

## Entrance awareness

Track all confirmed entry paths, not just the obvious main entry. If the user hints at extra entry paths, ask a follow-up.

Signals:
- 场景词：`结算后` `完成任务后` `收到通知/Push` `活动入口` `从其他界面跳转` `快捷方式`
- 状态词：`红点点击进来` `弹窗引导` `系统提示` `新手流程结束后`
- 位置词：`大厅` `主界面` `底栏` `悬浮球` `邮件` `公告`
- 数量暗示：`主要入口是 X，但也可以从 Y 进` `一般都走 X 流程`

Follow-up examples:
- 「你提到结算界面，那从结算界面是否可以直接跳转进入本功能？」
- 「Push 通知点击后会落在哪个界面？」
- 「除了大厅主入口，是否有其他界面也有进入本功能的快捷按钮？」

## Game-system checks

When the target is a game system, confirm these if the user has not already covered them:
- **红点提醒**：触发条件、出现入口、是否穿透上级入口、消除条件、邮件/Push 是否联动
- **新手引导**：是否需要引导，覆盖哪些操作；如果没有，原因是什么
- **经济影响**：是否涉及货币产出/消耗，以及整体经济影响预期

Ask each item with a separate `AskUserQuestion`. If the user says the system does not involve it or will decide later, record that as a decision/open item and stop probing it.

## Document trap probes

Use these probes only when the trigger signal appears.

| Trap | Trigger signal | Follow-up direction |
|---|---|---|
| 流程与底层机制脱节 | 用户默认“重新打开才看到结果” | 「这个进度/状态是实时推送到界面，还是需要玩家重新打开才能看到？」 |
| 规则遗漏 | 多阶段/多轮次/周期机制未提重置 | 「周期重置时，这个机制从哪里重新开始？进度如何处理？」 |
| 边界场景缺失 | 异步服务器事件、只描述“下次登录” | 「如果玩家正在界面上时这个事件发生，界面会即时刷新还是等下次打开才更新？有没有预警提示？」 |
| 只定义正向 | 只说满足条件 A 时怎样 | 「不满足该条件时，系统的行为是什么？」 |
| 措辞歧义 | `各自` `分别` `独立` `每个` 无限定语 | 「这里的‘各自’是指按同一套规则，还是不同类型有不同标准？」 |
| 内部矛盾 | 同一机制前后描述冲突 | 先整理已确认版本，再让用户确认哪个版本准确 |
| 排序规则缺失 | 列表/网格/排行/队列无排序依据 | 追问初始排序、优先级、状态变化是否重排、同优先级内顺序 |
| 跨周期表现缺失 | 每日/每周/每月刷新、限时活动、版本内容 | 追问周期结束处理、在线切换表现、倒计时预警、跨段内容重置点 |
| 奖励图标交互缺失 | 图标+数量的奖励/道具展示 | 「这些奖励/道具图标是否需要支持悬停或点击显示通用 Tip？复用全局规范还是单独定义？」 |

If the answer already covers the probe, skip it.
