# Game-Specific PRD/GDD Validation Requirements

## Overview

This document defines game-specific validation rules for game project PRD/GDDs. These rules are applied in Step 7 (Game Compliance Validation) and inform the overall quality assessment in Step 8.

## Game Domain Characteristics

This skill is specialized for game projects.

Game projects differ from standard software in:
- **Player Experience** as primary focus (not system performance or enterprise features)
- **Balance & Economy** as critical success metric (not just functional correctness)
- **Progression & Engagement** as core business driver (retention, monetization)

## Required Sections for Game PRD/GDDs

A valid game PRD/GDD MUST contain all 3 of these sections (beyond standard structure requirements):
1. Game Mechanics & Gameplay
2. Progression & Balance
3. Reminders & Onboarding

---

### 1. Game Mechanics & Gameplay (Mandatory)
Describes the core loop and how players interact.

**Should contain:**
- Core gameplay loop (what players do repeatedly, the "fun" part)
- Game mechanics (jump, attack, collect, build, strategize, etc.)
- Controls & input handling
- Win/lose/progress conditions (how players succeed and fail)
- Single-player vs. multiplayer mode distinctions (both must be described)

**Quality checks:**
- Core loop must be repeatable and engaging
- Mechanics must support the core loop
- Controls must be clearly mapped to mechanics
- Win conditions must be unambiguous and measurable

**Example violation:**
- ❌ "The game is fun and engaging" (subjective, not measurable)
- ✅ "Core loop: explore → collect resources → craft → deploy. Players repeat this every 10-15 minutes of play."

### 2. Progression & Balance (Mandatory)
Describes how players advance and how the game maintains balance.

**Should contain:**
- Progression path (levels, chapters, unlocks, skill trees, etc.)
- Balance targets (difficulty curve, economy tuning, power creep prevention)
- Loot/economy distribution (if applicable: drop rates, resource sinks, inflation targets)
- Endgame content (final bosses, raids, competitive rankings, etc.)
- Replayability mechanics (randomized content, seasonal events, roguelike elements)

**Quality checks:**
- Progression should feel rewarding without invalidating earlier content
- Balance targets should use specific numbers, not vague descriptions
- Economy should clearly describe sources and sinks
- Endgame must justify 50%+ of play time (for retention games)

**Example violation:**
- ❌ "The difficulty curve should be balanced" (vague, not testable)
- ✅ "Difficulty curve: Normal difficulty targets 10-12 hour campaign. Players gain 0.2x attack power per level, enemies gain 0.15x health/level (widening power gap as game progresses)."

### 3. Reminders & Onboarding (Mandatory)
Describes how players are guided through the game and notified of new content or actions.

**Should contain:**
- Tutorial structure (interactive vs. passive, paced vs. on-demand)
- Learning objectives per chapter/level (what players should learn)
- Red dot/notification system logic (trigger conditions, propagation hierarchy, clearing conditions)
- Feedback systems (visual, audio, haptic feedback)
- Tutorial exit criteria (when can players skip?)

**Quality checks:**
- Tutorials should teach all core mechanics before complex scenarios
- Red dot systems must clearly define when a dot appears, how it bubbles up the UI hierarchy, and what exact player action makes it disappear
- Each tutorial segment should take <5 minutes (or explain why longer)
- Feedback must be clear for all ability levels

**Example violation:**
- ❌ "Game includes intuitive tutorials and red dots for new items." (vague)
- ✅ "Tutorial 1 (5 min): Movement controls. Red dot logic: Appears on 'Inventory' icon when new item looted. Bubbles up to 'Main Menu'. Clears only when player hovers over the specific new item."

## Excluded or Non-Standard Sections

Game PRD/GDDs should **NOT** include implementation details:
- ❌ "Built with Unity 2022 LTS"
- ❌ "Uses Photon for multiplayer"
- ❌ "Database uses MongoDB"
- ❌ "Hosted on AWS"

If these appear in FRs/NFRs, they are flagged as Implementation Leakage (Step 6).

## Game-Specific Anti-Patterns

When validating game PRD/GDDs, look for these common issues:

### 1. Subjective Game Feel Claims
- ❌ "The game is engaging and fun" → ✅ "Core loop repeats every 12 minutes, with 3 progression tiers"
- ❌ "Intuitive controls" → ✅ "All commands on WASD + mouse, full rebind support"

### 2. Vague Economy Descriptions
- ❌ "Players earn coins to buy upgrades" → ✅ "Coins earned: 10 per enemy, 50 per level. Costs: Common upgrades 200 coins, Rare 1000 coins. Target: players spend 60% of earnings, save 40%"

### 3. No Endgame Definition
- ❌ "Endgame includes raids" → ✅ "Endgame (levels 50-99): Weekly raid progression, Competitive ranking ladder (Top 100 leaderboard), Cosmetic battle pass (seasonal, 10-week duration)"

## Severity Classification for Game PRD/GDDs

### Critical (Must Fix Before Launch)
- Missing core gameplay loop description
- No progression/balance targets defined

### Warning (Fix Before Alpha/Beta)
- Onboarding tutorial or red dot logic is vague
- Economy lacks specific numbers (rough targets acceptable)
- Balance targets conflict with progression
- Endgame content < 5% of total playtime description

### Info (Nice to Have)
- Minor clarity improvements in mechanic descriptions

## Checklist for Game PRD/GDD Validation

Use this during Step 7 (Game Compliance Validation):

```
□ Core gameplay loop is described in specific terms (not "fun", "engaging")
□ Progression system is clear (levels, unlocks, chapters, etc.)
□ Balance targets are numeric (difficulty curves, economy, power scaling)
□ Reminders and onboarding (including red dot logic) are outlined
□ No implementation details in requirements (no tech stack)
□ Endgame content defined and justified
□ All list/collection features define their sort order (see List Sorting Completeness below)
```

## List Sorting Completeness

游戏 PRD/GDD 中凡是描述「列表型界面」的功能模块，必须说明排序规则。缺少排序定义会导致开发实现不一致，且通常在实现阶段才被发现，代价较高。

**需要检查排序的典型场景：**
- 任务列表、道具列表、好友列表、排行榜
- 商店物品列表、背包物品列表
- 历史记录、通知列表、消息列表
- 搜索/筛选结果列表

**排序规则必须回答：**
1. **默认排序字段**：列表默认按什么排（时间、优先级、状态、配置字段等）
2. **状态分层**（如适用）：不同状态的条目是否有优先级差异（如「可领取」置顶于「进行中」）
3. **同层内部排序**：同一状态分组内，条目按什么二级规则排列
4. **动态变化**：条目状态变化时是否触发重排（如任务完成时是否立即置顶）

**检查方法：**
扫描文档中出现以下关键词的功能模块：列表、清单、显示所有、展示、滚动列表。
对每个命中模块判断：该模块是否明确说明了排序规则？

**严重程度：**
- **Warning**：功能模块描述了列表，但未提及任何排序相关内容
- **Pass**：排序规则已明确（哪怕只是「按配置字段排序」也算明确）

**违规示例：**
- ❌ "任务界面展示所有当前任务" （只描述展示，无排序）
- ✅ "任务界面展示所有当前任务；分组内按状态排序：可领取优先，同状态内按配置的排序字段升序"

**注意**：排序规则不需要非常复杂，但必须存在。「固定顺序」「按添加时间」「策划配置」都是有效的排序定义。

## Examples: Good vs. Bad Game PRD/GDDs

### Bad Example (Vague)
```
## Gameplay
The game is a fun action-adventure title where players explore a beautiful world, 
fight enemies, and complete quests. The game is intuitive and engaging.

## Progression
Players unlock new abilities and items as they progress through the story.
```

### Good Example (Specific)
```
## Gameplay
Core loop (repeats every 12-15 min): Explore (find resources) → Combat (defeat 3-5 enemies) 
→ Crafting (combine resources into tools) → Deployment (use tools to solve puzzle). Controls: 
WASD movement, mouse aim, E interact, Space jump. All controls fully remappable.

## Progression
Three acts (Act 1: tutorial, 8 levels | Act 2: open world, 12 locations | Act 3: endgame raids, 
5 weekly challenges). Players gain 0.3x power per level. Enemies gain 0.2x per difficulty scaling 
(players become more powerful as game progresses, justifies content difficulty increase).
```

## References

Related standards:
