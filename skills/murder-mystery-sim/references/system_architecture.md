# 剧本杀模拟评测系统 — 架构参考文档

## 1. 系统概览

本系统通过多Agent协作模拟剧本杀游戏全流程，并对剧本质量进行多维度评测。

### 核心流程

```
剧本输入 → 角色解析 → Agent参数配置 → 模拟执行 → 数据收集 → 评测分析 → 报告生成
```

### 输入要求

用户需提供以下材料（至少提供前2项）：

| 材料 | 必要性 | 说明 |
|------|--------|------|
| 角色手册 | **必须** | 每个角色的背景故事、已知信息、秘密、目标 |
| DM手册/真相 | **必须** | 真相时间线、凶手身份、关键线索链 |
| 线索卡 | 推荐 | 搜证环节可获取的物证/证词 |
| 地图/场景 | 可选 | 空间布局，影响搜证逻辑 |
| 特殊机制 | 可选 | 技能卡、阵营机制、投票规则等 |

## 2. Agent人格系统

### 2.1 认知参数矩阵

每个Agent拥有以下参数（0.0~1.0）：

```yaml
cognitive_profile:
  # 基础认知
  rationality: 0.7        # 理性权重（越低越感性）
  conformity: 0.4         # 从众倾向
  contrarian: 0.3         # 对抗性/唱反调倾向
  trust_threshold: 0.5    # 信任阈值（越低越容易信人）
  
  # 情绪易感度
  guilt_susceptibility: 0.5     # 愧疚驱动敏感度
  fear_susceptibility: 0.4      # 恐惧驱动敏感度
  empathy_susceptibility: 0.6   # 共情绑架敏感度
  anger_trigger: 0.3            # 愤怒触发敏感度
  
  # 推理风格
  deduction_style: "logical"    # logical / intuitive / evidence-driven / social
  attention_to_detail: 0.7      # 细节关注度
  memory_accuracy: 0.8          # 记忆准确度（影响是否"忘记"早期线索）
  
  # 社交风格
  assertiveness: 0.6            # 主动发言倾向
  persuasion_skill: 0.5         # 说服能力
  deception_detection: 0.5      # 测谎直觉
  charisma: 0.5                 # 魅力值（影响说服别人的效果）
```

### 2.2 动态关系系统

Agent之间维护实时关系矩阵：

```yaml
relationships:
  agent_a -> agent_b:
    trust: 0.5          # 信任度（-1.0 ~ 1.0）
    suspicion: 0.0      # 怀疑度（0.0 ~ 1.0）
    affinity: 0.0       # 好感度（-1.0 ~ 1.0）
    persuaded_count: 0  # 被对方成功说服的次数
    betrayed: false     # 是否发现对方撒谎
```

### 2.3 说服力计算公式

当Agent A试图说服Agent B时：

```
influence_score = 
    argument_logic_strength × 0.35
  + speaker_charisma × 0.20
  + listener_trust_toward_speaker × 0.15
  + emotional_appeal_match × 0.15
  + (1 - listener_rationality) × 0.10
  + conformity_bonus × 0.05

其中：
- argument_logic_strength：论点逻辑强度（0~1），由证据支撑度决定
- speaker_charisma：说话者魅力值
- listener_trust_toward_speaker：听者对说话者的信任度
- emotional_appeal_match：情绪策略与听者易感类型的匹配度
- listener_rationality：听者理性权重（理性越高越不容易被说服）
- conformity_bonus：如果多数人支持该观点，从众者获得加成
```

当 influence_score > listener_trust_threshold 时，听者被说服。

### 2.4 情绪煽动机制

Agent可使用以下情绪策略：

| 策略 | 触发词/模式 | 对应易感参数 | 示例 |
|------|------------|-------------|------|
| 愧疚绑架 | "你忍心…" "我这么信任你…" | guilt_susceptibility | "我把所有线索都告诉你了，你居然怀疑我？" |
| 恐惧驱动 | "再不投他就完了" "时间不多了" | fear_susceptibility | "如果今天不找出凶手，下一个死的可能就是你" |
| 共情绑架 | "我也是受害者" "将心比心" | empathy_susceptibility | "死者是我最好的朋友，你觉得我会杀他？" |
| 激将法 | "你敢不敢…" "有本事…" | anger_trigger | "你有证据就拿出来啊，别在这含沙射影" |
| 魅力压制 | 自信、从容、逻辑表象 | charisma对抗 | 高魅力角色即使论据一般也更有说服力 |

## 3. 模拟流程

### 3.1 标准流程（可根据剧本调整）

```
第一阶段：开场（1轮）
  ├── 所有Agent阅读自己的角色手册
  ├── 生成每个Agent的初始认知状态
  └── 自我介绍轮（每人1段发言）

第二阶段：自由讨论（2-3轮）
  ├── 每轮每人1次主发言 + 可选回应
  ├── 动态更新关系矩阵
  └── 记录怀疑目标变化

第三阶段：搜证（1-2轮）
  ├── 根据搜证规则分配线索
  ├── Agent决定是否公开/隐瞒线索
  └── 更新所有Agent的信息状态

第四阶段：集中讨论（2-3轮）
  ├── 基于新证据的深度讨论
  ├── 情绪策略密集使用阶段
  └── 阵营/联盟自然形成

第五阶段：投票（1轮）
  ├── 每人陈述最终推理
  ├── 投票选出凶手
  └── 记录投票理由

第六阶段：复盘
  ├── 揭示真相
  ├── 每个Agent回顾自己的推理链
  └── 生成模拟数据报告
```

### 3.2 Agent决策流程（每次发言前）

```
1. 回顾已知信息（角色手册 + 目前获得的线索 + 其他人的发言）
2. 评估当前怀疑列表（按嫌疑度排序）
3. 考虑自身目标（隐藏秘密？保护某人？找出凶手？）
4. 选择发言策略：
   a. 信息分享（公开线索）
   b. 质疑某人（提出疑点）
   c. 辩护（为自己或盟友辩护）
   d. 情绪策略（使用上述煽动手段）
   e. 试探（抛出半真半假信息试探反应）
5. 应用人格参数过滤：
   - rationality 高 → 倾向逻辑论证
   - assertiveness 高 → 倾向主动质疑
   - charisma 高 → 发言更有说服力
   - contrarian 高 → 倾向挑战主流观点
6. 生成发言内容
7. 更新自身状态和对他人的关系评估
```

## 4. 评测维度

### 4.1 信息设计评分

| 子维度 | 评分标准 | 权重 |
|--------|---------|------|
| 线索均衡度 | 每个角色掌握的关键线索数量是否均衡 | 20% |
| 推理可达性 | 真相是否可以通过公开信息合理推导 | 25% |
| 信息冗余度 | 有多少线索是完全无用的填充 | 15% |
| 信息遮蔽度 | 关键线索的隐藏是否合理 | 20% |
| "空气人"检测 | 是否有角色缺乏独特信息贡献 | 20% |

### 4.2 推理体验评分

| 子维度 | 评分标准 | 权重 |
|--------|---------|------|
| 逻辑链完整度 | 从线索到真相是否有完整推理链 | 30% |
| 误导质量 | 误导线索是否自洽且有趣 | 20% |
| "啊哈时刻" | 是否存在信息组合产生顿悟的设计 | 25% |
| 推理难度曲线 | 是太简单、太难还是恰好？ | 25% |

### 4.3 角色体验评分

| 子维度 | 评分标准 | 权重 |
|--------|---------|------|
| 故事独立性 | 每个角色有自己的完整故事弧 | 25% |
| 互动驱动力 | 角色设计是否促使玩家主动交流 | 25% |
| 秘密有趣度 | 角色的秘密是否有趣且有戏剧张力 | 25% |
| 凶手体验 | 凶手是否有主动博弈空间 | 25% |

### 4.4 节奏评分

| 子维度 | 评分标准 | 权重 |
|--------|---------|------|
| 信息释放节奏 | 关键信息出现的时机是否合理 | 30% |
| 高潮设计 | 是否有明确的戏剧高潮 | 25% |
| 中期参与度 | 中间阶段是否有"塌腰"现象 | 25% |
| 结局满足感 | 真相揭晓是否让人满足 | 20% |

### 4.5 社工空间评分

| 子维度 | 评分标准 | 权重 |
|--------|---------|------|
| 话术操作空间 | 凶手能否靠话术影响局势 | 30% |
| 带节奏脆弱度 | 一个强势玩家能否把全场带偏 | 25% |
| 联盟形成自然度 | 是否自然产生阵营对抗 | 25% |
| 情绪驱动占比 | 最终投票中感性决策vs理性决策的比例 | 20% |

### 4.6 总体评分

总分 = 信息设计 × 0.25 + 推理体验 × 0.25 + 角色体验 × 0.20 + 节奏 × 0.15 + 社工空间 × 0.15

评级标准：
- S级（90+）：精品本，各维度均衡出色
- A级（80-89）：优秀本，有明确亮点
- B级（70-79）：合格本，基本功扎实但缺乏亮点
- C级（60-69）：需要修改，存在明显问题
- D级（<60）：严重问题，需要大幅重构

## 5. 输出格式

### 5.1 模拟记录

每轮对话以Markdown格式输出：

```markdown
## 第X轮 — [阶段名称]

### [角色名] 发言
> [发言内容]

**内心状态**：[当前怀疑目标 | 情绪状态 | 策略选择]
**影响效果**：[哪些Agent被影响 | 关系变化]

---
```

### 5.2 评测报告

Markdown报告包含：
1. 概述与总评分
2. 各维度详细评分及分析
3. 每个角色的体验分析
4. 关键时刻回顾（转折点、高潮、失误）
5. 具体改进建议
6. 附录：完整模拟记录

## 6. 参数预设模板

### 典型玩家类型

```yaml
# 逻辑推理型
logical_player:
  rationality: 0.9
  conformity: 0.2
  contrarian: 0.4
  trust_threshold: 0.7
  guilt_susceptibility: 0.2
  fear_susceptibility: 0.2
  empathy_susceptibility: 0.3
  anger_trigger: 0.2
  deduction_style: "logical"
  assertiveness: 0.6
  persuasion_skill: 0.5
  charisma: 0.4

# 社交直觉型
social_player:
  rationality: 0.4
  conformity: 0.5
  contrarian: 0.3
  trust_threshold: 0.4
  guilt_susceptibility: 0.7
  fear_susceptibility: 0.5
  empathy_susceptibility: 0.8
  anger_trigger: 0.4
  deduction_style: "social"
  assertiveness: 0.7
  persuasion_skill: 0.7
  charisma: 0.7

# 萌新/观望型
newbie_player:
  rationality: 0.5
  conformity: 0.8
  contrarian: 0.1
  trust_threshold: 0.3
  guilt_susceptibility: 0.6
  fear_susceptibility: 0.7
  empathy_susceptibility: 0.6
  anger_trigger: 0.2
  deduction_style: "intuitive"
  assertiveness: 0.2
  persuasion_skill: 0.3
  charisma: 0.3

# 老玩家/控场型
veteran_player:
  rationality: 0.7
  conformity: 0.2
  contrarian: 0.5
  trust_threshold: 0.6
  guilt_susceptibility: 0.2
  fear_susceptibility: 0.2
  empathy_susceptibility: 0.3
  anger_trigger: 0.3
  deduction_style: "evidence-driven"
  assertiveness: 0.9
  persuasion_skill: 0.8
  charisma: 0.8

# 演绎沉浸型
immersive_player:
  rationality: 0.5
  conformity: 0.4
  contrarian: 0.3
  trust_threshold: 0.5
  guilt_susceptibility: 0.8
  fear_susceptibility: 0.6
  empathy_susceptibility: 0.9
  anger_trigger: 0.5
  deduction_style: "intuitive"
  assertiveness: 0.5
  persuasion_skill: 0.6
  charisma: 0.6
```
