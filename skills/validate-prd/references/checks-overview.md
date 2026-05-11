# Validation Checks Overview

> Reference file — load when the user asks "what does this skill check?" or needs an overview of check criteria before running. Each check's full execution rules are in the corresponding `steps-v/` file.

## What Each Step Checks

### Step 2: Format Detection
- 4 required core sections: Product Scope, User Journeys, Functional Requirements, Non-Functional Requirements
- Game-specific sections: Game Mechanics, Progression & Balance, Reminders & Onboarding
- Section heading numbering: every heading must have a hierarchical numeric prefix (`1.标题`, `1.1.标题`, `1.1.1.标题`)

### Step 3: Information Density
Scans for filler words and wordy phrases that reduce signal-to-noise ratio:
- ❌ "The system will allow users to..." → ✅ "Users can..."
- ❌ "Due to the fact that..." → ✅ "Because..."
- ❌ "In the event of..." → ✅ "If..."

### Step 4: Clarity & Ambiguity
Scans for expressions that are vague, contradictory, or underspecified.

**Vague qualifiers** — words that defer precision without defining what "precise" means:
- ❌ "即时刷新" → ✅ "界面在重置完成后 5 秒内刷新"
- ❌ "适当增加" → ✅ "增加 20%"
- ❌ "自动处理" → ✅ "系统自动重试 3 次后标记为失败"
- Common offenders: 实时、自动、适当、合理、必要时、视情况、尽快、默认、相关、相应

**Contradictory modifiers** — two qualifiers on the same subject that pull in opposite directions:
- ❌ "满足前不显示但生效" → ✅ "满足前界面不可见但进度在后台累积"
- ❌ "可选且必填" → ✅ (pick one, or define which contexts make it optional vs required)

**Underspecified behavior** — an action described without enough detail to implement:
- ❌ "奖励预览区支持滚动" → ✅ "奖励预览区最多同时显示 3 个奖励项，超过时垂直滚动查看"
- ❌ "进度实时推送至界面" → ✅ "任务进度更新不依赖于任务界面打开拉取"

**Implicit assumptions** — text that is only clear if the reader already knows unstated context:
- ❌ "轮式任务进度独立" → ✅ "各轮进度独立计算，不跨轮共享"
- ❌ "重置后重新开始" → ✅ "重置时已推进的阶段/轮次和所有进度全部清零"

**Severity:**
- Critical: contradictory modifiers, or underspecified behavior in FRs affecting user-facing behavior
- Warning: vague qualifiers in NFRs, or implicit assumptions partially resolved by context

### Step 5: Brief Coverage
Cross-checks the PRD/GDD against an upstream Product Brief or Vision Doc (if provided). Maps 6 elements: vision statement, target users, problem statement, key features, goals/objectives, differentiators.

### Step 6: Traceability
Validates requirement chains:
- User Journeys → Functional Requirements
- Product Scope → FRs
- Flags orphan FRs (no traceable source) and journey steps with no supporting FR

### Step 7: Implementation Leakage
Ensures requirements specify WHAT (capability), not HOW (implementation):
- ❌ Bad: "REST API with JWT authentication"
- ✅ Good: "API consumers can authenticate with cryptographic tokens"
- Scans for: React/Vue, PostgreSQL/MongoDB, Docker/Kubernetes, AWS/GCP, Unity/Unreal, Photon, etc.

### Step 8: Game Domain Compliance
Validates all 3 mandatory game-specific sections are present and specific (not vague):
- Game Mechanics & Gameplay
- Progression & Balance
- Reminders & Onboarding

Also checks: list sorting completeness, periodic content cross-boundary behavior, reward/item hover interaction, internal consistency between sections.

### Step 9: Holistic Quality
Rates document 1–5 across three dimensions:
- Document Flow & Coherence
- Dual Audience Effectiveness (humans and LLMs)
- Writing Quality Compliance

Identifies top 3 highest-impact improvements.

### Step 10: Report Complete
- Completeness check: no template variables, all required sections have substantive content, Design Purpose (设计目的) present in Product Scope
- Consolidates all findings → Overall Status (Pass / Warning / Critical)
- Saves report to same directory as the PRD/GDD

---

## Game PRD/GDD Standards Summary

A production-ready game PRD/GDD must address:

**Gameplay & Mechanics**
- Core gameplay loop (clear, repeatable, specific timing)
- Game mechanics (how players interact, what they control)
- Progression system (XP, levels, unlocks, story beats)
- Balance targets (difficulty curves, economy tuning — use specific numbers)

**Player Experience**
- Target audience & personas
- Reminders & onboarding (including red dot logic)
- User journeys (from install through end-game)

For full game-specific anti-patterns and checklist, see `data/game-requirements.md`.

---

## Tips for Document Authors

- Start with a complete first draft; this skill validates, it does not draft
- Write requirements as user capabilities, not implementation details
- Every FR should trace back to a user journey or business goal
- For balance and economy, use specific targets ("economy targets X% deflation per season")
- Always define sort order for any list-type UI feature
- Always define cross-boundary behavior for any periodic/time-limited content
