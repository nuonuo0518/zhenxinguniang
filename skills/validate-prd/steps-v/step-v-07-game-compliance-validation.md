# Step V-07: Game Compliance Validation

## Goal
Validate that the document includes all game-specific sections required for a production-ready game PRD/GDD. This step replaces the standard domain and project-type validation with game-specific rules.

## Required Sections

Read `data/game-requirements.md` for the full standards. Summary of required sections:

| Section | Required? | Condition |
|---------|-----------|-----------|
| Game Mechanics & Gameplay | Mandatory | Always |
| Progression & Balance | Mandatory | Always |
| Reminders & Onboarding | Mandatory | Always |

## Process

### 1. Load Game Requirements Standards

Read `data/game-requirements.md` to get:
- Required section checklist
- Quality criteria for each section
- Anti-pattern examples
- Severity thresholds

### 2. Check Section Presence

For each required section, scan the document for matching content. Section names may vary — look for semantic content, not exact header matches:

- "Game Mechanics" might be titled "Core Gameplay", "Gameplay Systems", "How It Plays"
- "Progression & Balance" might be "Progression System", "Economy & Balance", "Player Growth"
- "Reminders & Onboarding" might be "Tutorials", "Notifications", "Player Onboarding"

### 3. Evaluate Section Quality

For each section that IS present, check quality:

**Game Mechanics:**
- ✓ Core loop described with timing (e.g., "repeats every X minutes")
- ✓ Specific mechanics named (not just "combat and exploration")
- ✓ Controls documented (or reference to separate control doc)
- ❌ Vague: "The game features engaging combat and exploration"

**Progression & Balance:**
- ✓ Progression path clearly defined (levels/chapters/unlocks)
- ✓ Balance targets include specific numbers
- ✓ Economy sources and sinks described
- ❌ Vague: "Difficulty should feel balanced and rewarding"

**Reminders & Onboarding:**
- ✓ Tutorial structure outlined (interactive vs. passive)
- ✓ Red dot/notification logic defined (triggers and clear conditions)
- ✓ Per-tutorial learning objectives listed
- ✓ Skip conditions defined
- ❌ Vague: "Game includes helpful tutorials and red dots"

### 4. Apply Game-Specific Anti-Pattern Check

Flag these common game document anti-patterns (see `data/game-requirements.md` for full list):
- Subjective game-feel claims ("engaging", "fun", "immersive")
- Vague economy descriptions ("players earn coins to buy things")
- No endgame definition

### 5. List Sorting Completeness Check

扫描文档中所有描述「列表型界面」的功能模块，检查是否定义了排序规则。

**扫描信号词**：列表、清单、展示所有、滚动列表、显示、界面内展示

**对每个命中模块判断**：
- 是否说明了默认排序字段？（如：按时间、按状态、按配置字段）
- 若存在多种状态的条目，是否说明了状态间的优先级？（如：完成的置顶、过期的置底）
- 若有动态变化（状态切换触发重排），是否有说明？

**判定规则**：
- 只要排序规则存在且可被开发人员理解，即为 Pass（不要求复杂）
- 功能模块明确描述了列表，但完全没有提及任何排序信息 → Warning
- 多个列表模块均无排序说明 → 酌情升级为较高优先级的 Warning

**输出**：列出每个被检查的列表模块及其判定结果。

### 6. Periodic Content Cross-Boundary Behavior Check

扫描文档中所有含更新周期的内容（日任务、周任务、限时活动、版本内容等），检查是否定义了跨周期边界的完整行为。

**扫描信号词**：每日、每周、每月、刷新、重置、限时、活动期间、版本内、到期

**对每个命中模块判断**：
- 周期结束时，未完成/未领取的内容如何处理（进度保留、清零、奖励作废）？
- 玩家**在线时**恰好经历周期切换，界面是否即时刷新？是否有提示？
- 跨段式内容（链式/轮式任务、多阶段活动）遭遇重置时，从哪个阶段重新开始？

**判定规则**：
- 文档明确描述了上述三点之一且可被开发人员理解 → Pass（不要求全覆盖）
- 文档有周期性内容，但完全没有提及任何跨周期行为 → Warning
- 多个周期模块均无跨周期行为说明 → 酌情升级为较高优先级的 Warning

**输出**：列出每个被检查的周期模块及其判定结果。

### 7. Internal Consistency Check

扫描文档中同一机制在不同位置的描述，识别是否存在相互矛盾或隐含假设不一致的表述。

**重点扫描以下场景**：
- 用户旅程（UJ）中对某功能的操作步骤描述，与功能需求（FR）或模块说明中的行为描述是否一致？
- 同一界面元素（如按钮、图标、分组）在不同章节是否有矛盾描述（如一处说"可折叠"，另一处说"始终展开"）？
- 用户旅程步骤表格的「系统响应」列中，是否存在暗含特定技术实现的描述（如"返回界面后看到更新"暗含需手动刷新，但功能需求说实时推送）？

**判定规则**：
- 发现同一机制有两处以上相互矛盾的表述 → Critical，列出矛盾位置和矛盾内容（矛盾描述会直接导致开发和测试理解不一致，产出不可预期的实现）
- 用户旅程步骤与功能模块描述存在隐含假设不一致 → Critical（隐含矛盾比显式矛盾更危险，往往到开发后期才暴露）
- 未发现矛盾 → Pass

**输出**：列出发现的矛盾对（位置A vs. 位置B，各自的描述内容）。

### 8. Reward/Item Display Hover Interaction Check

扫描文档中所有以「图标 + 数量」形式展示物品的内容，检查是否定义了悬停（或点击）交互行为。

**扫描信号词**：奖励预览、奖励图标、道具图标、礼包、图标 + 数量、奖励列表、展示奖励

**对每个命中模块判断**：
- 是否说明了悬停/点击图标时是否显示 Tip？
- 若支持 Tip，是复用全局道具悬停规范，还是单独定义了内容？

**判定规则**：
- 文档有奖励/道具展示内容，且明确说明了悬停行为（支持或明确不支持均可）→ Pass
- 文档有奖励/道具展示内容，但完全未提及悬停行为 → Warning

**输出**：列出每个被检查的奖励展示模块及其判定结果。

### 9. Classify Severity

**Critical:**
- 2+ mandatory sections missing entirely
- Core gameplay loop not described

**Warning:**
- 1 mandatory section missing
- Present sections contain mostly vague language
- Anti-patterns found in 2+ sections

**Pass:**
- All 3 mandatory sections present
- Sections contain specific numbers and targets
- Game-specific anti-patterns absent or minimal (≤1)

## Append to Report

```
## Game Compliance Validation (Step 7)

**Required Sections (3/3):**
- Game Mechanics & Gameplay: {✓ Present & specific | ⚠ Present but vague | ❌ Missing}
- Progression & Balance: {✓/⚠/❌}
- Reminders & Onboarding: {✓/⚠/❌}

**Section Quality Issues:**
- Mechanics: {Specific issue if any}
- Balance: {Specific issue if any}
- {etc.}

**Game Anti-Patterns Found:** {count}
- "{Quote}" → {Why it's an anti-pattern} → {Suggested fix}

**List Sorting Completeness:**
- {模块名}：{✓ 排序规则已定义 | ⚠ 未定义排序规则}
- ...
- 判定：{PASS / WARNING}

**Periodic Content Cross-Boundary Behavior:**
- {模块名}：{✓ 跨周期行为已定义 | ⚠ 未定义跨周期行为}
- ...
- 判定：{PASS / WARNING}

**Reward/Item Display Hover Interaction:**
- {模块名}：{✓ 悬停行为已定义 | ⚠ 未定义悬停行为}
- ...
- 判定：{PASS / WARNING}

**Internal Consistency:**
- {矛盾对1}：位置A「...」vs. 位置B「...」
- ...
- 判定：{PASS / CRITICAL}

**Severity:** {CRITICAL | WARNING | PASS}
**Status:** ✓ Proceeding to Holistic Quality Assessment
```

## Output

- ✓ All 3 required game sections checked for presence
- ✓ Present sections evaluated for quality
- ✓ Game-specific anti-patterns identified
- ✓ List sorting completeness checked
- ✓ Periodic content cross-boundary behavior checked
- ✓ Reward/item display hover interaction checked
- ✓ Internal consistency checked
- ✓ Findings appended to report

## Next Step

→ Execute `step-v-08-holistic-quality-validation.md`

## Checkpoint

Before proceeding to Step 8, output this line verbatim (fill in the numbers):

```
✅ Checkpoint Step V-07: required sections {sections_present}/3, anti-patterns {antipattern_count}, list-sorting modules checked {list_modules_checked}, periodic modules checked {periodic_modules_checked}, hover modules checked {hover_modules_checked}, consistency issues {consistency_issue_count}
```

Completion conditions:
- `sections_present` is one of 0, 1, 2, or 3 (not skipped)
- All list modules with sorting signals have been evaluated (`list_modules_checked >= 0`)
- Consistency check was performed (even if no issues found)

## Important Constraints

- **Do NOT** load step-v-08 before completing this step
- **Do NOT** modify the document
- **Do** read `data/game-requirements.md` for full checklist before evaluating
- **Do** look for semantic content, not exact header matches
- **Do** distinguish between "missing" and "present but vague"
