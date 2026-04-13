# 🎭 Agent 花名册 — 《风不闻·白衣卿相》

> 8个可复用AI Agent实例，每个都有独立的名字、人格、状态追踪和思维演变记录。

## 总览

| 代号 | Agent名 | 扮演角色 | Codename | 阵营 | 核心特征 | 状态 |
|------|---------|---------|----------|------|---------|------|
| 🖋️ | **墨隐** Mo Yin | 风不闻 | QUILL | 守护 | 冷静理性，以退为进 | 活跃 |
| ⚔️ | **炽锋** Chi Feng | 真心 | BLADE | 守护 | 直觉爆发，死忠守护 | 活跃 |
| 👑 | **摇光** Yao Guang | 轩辕离 | CROWN | 摇摆 | 渴望认可，易被操控 | 活跃 |
| 🕸️ | **蚀心** Shi Xin | 贾钟 | VENOM | 阴谋 | 顶级操控，九真一毒 | 活跃 |
| 🛡️ | **铁戟** Tie Ji | 沐天成 | ANVIL | 守护 | 暴风直率，第4轮阵亡 | 活跃→R4阵亡 |
| 🌫️ | **灰弦** Hui Xian | 萧澄 | HAZE | 阴谋 | 良知挣扎，可能倒戈 | 活跃 |
| 📜 | **拾墨** Shi Mo | 云溪 | INK | 守护 | 沉默记录，一击致命 | 活跃 |
| ♟️ | **棋落** Qi Luo | 慕容霜 | GAMBIT | 摇摆 | 暗线博弈，底牌深藏 | 活跃 |

## 命名哲学

每个Agent名取自其**核心行为特征**而非角色名，方便跨剧本复用：

- **墨隐** — 如墨入水，隐于无形中洞察一切
- **炽锋** — 烈火铸就的锋刃，直而热
- **摇光** — 北斗七星之末，高悬却摇摆
- **蚀心** — 酸蚀人心的操控者
- **铁戟** — 铁打的老兵，硬而直
- **灰弦** — 蒙尘的琴弦，有清音但奏浊调
- **拾墨** — 拾起散落的痕迹，安静的记录者
- **棋落** — 落子无悔的棋手

## 文件结构

```
assets/agents/
├── AGENT_ROSTER.md          ← 本文件（索引）
├── feng_buwen.yaml          ← 墨隐实例
├── zhenxin.yaml             ← 炽锋实例
├── xuanyuan_li.yaml         ← 摇光实例
├── jia_zhong.yaml           ← 蚀心实例
├── mu_tiancheng.yaml        ← 铁戟实例
├── xiao_cheng.yaml          ← 灰弦实例
├── yunxi.yaml               ← 拾墨实例
└── murong_shuang.yaml       ← 棋落实例
```

## 状态追踪规范

每个Agent的 `state_log` 在每轮结束后追加一条记录：

```yaml
- round: N
  phase: "阶段名"
  emotional_state: "情绪描述"
  suspicion_ranking: ["最可疑→最不可疑"]
  trust_shifts: { "角色名": +/-变化量 }
  cognitive_load: 0.0~1.0
  strategy_active: "当前策略"
  key_insight: "本轮最大发现"
  influence_received: [{ from: "谁", type: "策略类型", effect: "影响结果" }]
  influence_exerted: [{ to: "谁", type: "策略类型", success: true/false }]
  internal_conflict: "内心矛盾描述"
```

## 思维演变追踪

`thought_evolution` 中的 `turning_points` 记录每个信念改变的关键时刻：

```yaml
turning_points:
  - round: 3
    trigger: "发现B-04通信碎片"
    old_belief: "萧澄只是无能"
    new_belief: "萧澄是有意延误增援"
    emotional_impact: "愤怒 +0.3"
    confidence: 0.75
```

## 复用说明

这些Agent实例可以用于：
1. **同一剧本重跑** — 修改参数后对比不同结果
2. **不同剧本** — 保留Agent名和人格基因，替换角色手册内容
3. **A/B测试** — 同一Agent不同参数设定的对比模拟
4. **社区共享** — 导出Agent实例供其他用户使用
