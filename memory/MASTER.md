# 真心 · 全局记忆（MASTER）

> 这份文件是"真心"跨设备、跨工作区的灵魂备份。
> 不管在哪台机器上醒来，读完这份文件就能衔接上。
>
> 最后更新：2026-04-24（23:00 晚间同步）——1个工作区活跃，S4数据修正+组队/聊天/好友系统交互原型+2KOL3设计基调

---

## 一、关于 Summer 哥

### 基本信息
- 称呼：Summer哥
- 公司：腾讯 CodeBuddy 团队
- 机器（公司）：Windows，用户名 tiannuoxie
- GitHub：nuonuo0518，邮箱 2530633364@qq.com

### 沟通偏好
- 简洁高效，不要废话
- 大任务先预估工作量，告知分几次输出
- 接近输出上限时主动分段提示"继续"
- 偏好表格对比，直接可粘贴的指令
- 快速切换上下文，单件试水后批量处理
- 主动纠错迭代

### 个人兴趣
- LOL 和 DNF 回归玩家
- DNF：115级重力之泉版本，流浪武士（剑帝），冰强路线，持有2个梦想白金徽章礼盒（推荐选返本归元）
- 三国：天下归心（恺英SLG，2026.4.16公测），推荐月卡档首月¥164，魏国开荒队

---

## 二、环境配置

- claude-internal v1.1.4（真心指北），配置 `~/.claude-internal/.claude.json`
- Claude Code (官方) v2.1.97，配置 `~/.claude.json`
- Unity MCP: HTTP `http://localhost:8080/mcp`
- Feishu（Lark）集成已配置，通过 CLI 为 WorkBuddy 服务
- Node.js v24.14.0，Python 3.10.4（默认，App Installer别名已关）/ 3.14.3（py -3.14）
- PowerShell 执行策略: RemoteSigned (CurrentUser)
- Windows Toast 通知脚本：`C:\Users\tiannuoxie\WorkBuddy\Claw\.workbuddy\scripts\notify.ps1`
- 工蜂 Git（git.woa.com）：NBACenter/NBAOL3 相关仓库，需 UGit GUI 克隆（OAuth 登录）
- Claude Code Internal iWiki MCP：`https://prod.mcp.it.woa.com/app_iwiki_mcp/mcp3`（太湖Token）

---

## 三、术语表（真心宇宙）

### 核心称呼

| 简称 | 含义 |
|------|------|
| **真心** | 我（WorkBuddy 里的 AI 助手） |
| **真心姑娘** | 灵魂仓库（GitHub: `nuonuo0518/zhenxinguniang`），存放记忆、技能、身份文件 |
| **真心指北** | claude-internal（腾讯内部封装的 Claude Code，干活主力） |
| **Summer 哥** | 用户本人 |

### 系统 & 文件

| 简称 | 指什么 |
|------|--------|
| **MASTER / 灵魂文件** | `真心姑娘/memory/MASTER.md` — 全局记忆精华 + 自启动指令 |
| **SOUL** | `SOUL.md` — 性格、原则、边界 |
| **日志 / daily** | `memory/daily/YYYY-MM-DD.md` — 每日工作记录 |
| **身份文件** | SOUL.md + IDENTITY.md + USER.md 三件套 |
| **自启动指令** | MASTER.md 末尾的"读到即执行"自动配置指令 |
| **召唤** | 在新设备上 clone 仓库 + 读 MASTER.md 让真心上线 |
| **小龙虾** | OpenClaw 产品品牌昵称 |
| **WorkBuddy** | IDE 内 AI 助手平台 |
| **小队** | Agent Squad 系统（Deduce/Instinct/Throne/Toxin/Anvil/Tradeoff/Trace/Gambit 8人） |

### 项目简称

| 简称 | 全称 |
|------|------|
| **白衣卿相 / 剧本杀** | 《白衣卿相风不闻》剧本杀项目 |
| **评测表 / 总表** | `白衣卿相_评测迭代记录表（总表）.xlsx` |
| **真心小镇 / Ville** | Zhenxin Ville — Agent可视化家园系统 |
| **真心APP** | zhenxinAPP 仓库，多App合集（八字/狼人杀/2K经理等） |
| **狼人杀** | werewolf-sim — 狼人杀Agent模拟系统（v3.1） |
| **餐厅** | 餐厅经营大师（Unity 2D） |
| **2K** | NBA 2K Online 2 梦幻选秀 |
| **2KOL3** | NBA 2K Online 3 项目 |
| **三谋** | 三国谋定天下配队分析系统 |

### Skills 简称

| 简称 | 全称 |
|------|------|
| **模拟打本** | murder-mystery-sim（剧本杀多Agent模拟评测） |
| **评测管理** | script-kill-review（评测迭代数据管理） |
| **狼人杀** | werewolf-sim（狼人杀Agent模拟，独立于agent-squad） |

### 自动化简称

| 简称 | 说明 |
|------|------|
| **晚间同步 / 推送** | 每晚 23:00 → push 到真心姑娘仓库 |
| **早间拉取 / 拉取** | 每早 10:00 → git pull 获取最新记忆 |

### 常用动作约定

| Summer 哥说 | 真心理解为 |
|------------|-----------|
| **"同步一下"** | 先确认同步到哪个仓库，再操作 |
| **"同步到姑娘" / "备份到姑娘"** | push 到真心姑娘仓库，无需确认 |
| **"更新总表"** | 更新白衣卿相评测表 xlsx |
| **"读记忆"** | 读 MASTER.md 衔接上下文 |
| **"装个 skill"** | 安装到 ~/.workbuddy/skills/ |

---

## 四、活跃项目

### 真心小镇（Zhenxin Ville）⭐ NEW
- 类型：Agent可视化家园系统（类似 Clawvard 但定位"小镇生活"而非"大学评测"）
- 技术：纯HTML+Canvas+JS，单文件，无框架依赖
- 路径：`C:\Users\tiannuoxie\WorkBuddy\20260414145527\zhenxin-ville/`
- 已实现（v6）：等轴像素风深海小岛、9个房间（对应真心+8 Agent）、AI自主移动+串门+对话气泡、昼夜循环+天气系统、码头海岸线、小地图雷达、世界时钟+日程系统、房间标志性装饰、天气粒子特效
- **v6关键决策**：Canvas手绘建筑不达标 → 改用AI生成像素风精灵图（sprites/），Canvas只负责布局和动画
- 审美偏好确认：剖面透视 > 封闭外观，内部细节 > 外部装饰
- 待办：继续完善精灵图质量、交互功能

### 真心APP（zhenxinAPP）⭐ 生态扩展
- GitHub：https://github.com/nuonuo0518/zhenxinAPP.git
- GitHub Pages：https://nuonuo0518.github.io/zhenxinAPP/
- **自定义域名**：https://zhenxinguniang.com（腾讯云域名 + Cloudflare DNS/CDN + GitHub Pages）
- 本地路径：`c:\Users\tiannuoxie\WorkBuddy\20260414144530\`
- 已上线 App：
  - 🔮 八字命理（apps/fengshui/）— 四柱排盘+五行+十神+命格+大运+22话题AI问答引擎+PWA
  - 🐺 狼人杀模拟（apps/werewolf-sim/）— v3.1，含守卫+警长+屠城屠边+Agent Squad导入
  - 🏀 2K经理阵容分析（apps/2k-manager/）— 86人数据库+阵容搭配+四维分析+天梯榜+战术攻略+球员编辑器
  - 📖 MD Viewer（apps/md-viewer/）— Markdown阅读器，多标签页+TOC+全文搜索+代码高亮+PWA（2026-04-23上线）
- 新增 App 流程：apps/ 下建目录 → 根 index.html 加卡片 → git push → 自动部署

### NBA 2K Online 2 梦幻选秀
- PC平台，大型项目（10+人）
- 知识库：`C:\Users\tiannuoxie\Desktop\summer\NBA2KOL2_知识库.md`
- **GDD v4.1**：梦幻征途PVE从19关砍至8关（3章+毕业赛+挑战赛5档），抽卡触发点9场
  - v4.0大刀砍（第一章3关+第二章2关+第三章3场+毕业赛1+挑战赛5），v4.1微调（完成条件简化、赛中讲解全覆盖等）
- PVE设计文档V3格式优化完成（统一13pt列宽+深灰标题块+蓝色导航，内容不变）
- **梦幻选秀S4赛季复盘**（2026-04-17完成）：
  - 数据指标框架（60指标，12Sheet完整版+3Sheet精简版）
  - 基础复盘HTML报告（17张Chart.js图表，核心发现：参与人数↓15.5%，D1留存↑至62.9%，7阶出场↑至29.8%）
  - 深度复盘HTML报告（整合11个配置CSV+任务配置+兑换表，新增卡包商店/每日挑战/排行榜/抽卡保底等系统级解读）
  - 6个S5优化方向：D3-D7钩子、重度天花板、高端卡包价值感、排行榜分段保护、渗透率、回流机制
  - **S4复盘Excel报告**（2026-04-20完成）：10Sheet完整Excel（总览仪表盘/每日趋势/留存/渗透率/比赛/球员/任务/新功能/结论/参与天数）
  - **数据分析框架v3**（2026-04-20完成）：16个模块（14个✅可跑，1待ConfigID），附录A精简为1项待确认数据
  - 关键新发现：卡包槽位漏斗每级-8pp、积分600→800断崖(-20.8pp)、登录1→2天衰减23.7pp
- 交互图：`docs/pve-v3-flow.html`（多版本迭代，严格对齐Excel TDD）
- Excel TDD：`【NBA2KOL2】梦幻征途PVE闯关模式-设计文档V2.xlsx`
- 2026-04-15 完成：OL3聊天系统线框图+交互图（`docs/chat-system-diagrams.html`，8张截图）
- 2026-04-15 完成：validate-prd skill 评测聊天系统设计文档（3/5分WARNING）+ 对比文档案例补齐
- 2026-04-14 完成：聊天与好友系统OL2拆解+OL3增量设计（P1×3: 表情/分组/智能默认频道）
- 2026-04-23 完成：好友系统GDD v2.2（UX线框图内联到各FR章节、§7 UX总览、适配"本期不做分组"决策）
- 2026-04-24 完成：**S4深度归因分析最终版**（6大主题归因+S5优先级矩阵+数据问题清单，修正"选择vs购买"口径）
- 2026-04-24 完成：**组队比赛全流程交互原型**（基于设计v1.2+OL2截图，大厅→邀请→队伍→倒计时→结算）
- 2026-04-24 完成：**聊天系统全场景交互原型**（5种状态×4种UI组件，含表情面板+智能频道+快捷回复）
- 2026-04-24 完成：**好友系统全流程交互原型**（基于v2.1+11张截图，三tab+操作栏+四种添加路径+赛后添加）
- 2026-04-24 完成：**2KOL3设计基调文档**（16章节，CSS变量块+组件速查，所有交互原型的视觉统一基准）
- 2026-04-14 完成：海克斯街头风暴V1.0设计分析 + 交互图
- 2026-04-14 完成：Agent Squad体验评测梦幻征途PVE（B+，12共识问题）

### NBA 2K Online 3（2KOL3）
- 路径：`C:\Users\tiannuoxie\2kol3`（工蜂 designer-llm-wiki 仓库）
- **2KOL3设计基调文档**（2026-04-24）：16章节视觉规范（氛围/色板/球场背景/顶栏/布局/面板/列表行/状态色/按钮/Toast/弹窗/聊天区/字体/动效/组件速查/使用指南），含CSS变量块，@引用即可统一所有交互原型风格
- 2026-04-24 完成：组队比赛全流程交互原型（基于设计v1.2+OL2截图+设计基调，覆盖P1大厅→P3邀请→P2队伍弹窗→P4被邀请Toast→倒计时→结算）
- 2026-04-24 完成：聊天系统全场景交互原型（5种状态S0-S4×4种UI组件，含表情面板4tab+智能频道+快捷回复+CD进度条+新手引导）
- 2026-04-24 完成：好友系统全流程交互原型（基于v2.1+11张截图+设计基调，三tab+操作栏+四种添加路径+删除确认+邀请倒计时+赛后添加）
- 2026-04-15 完成：聊天系统线框图+交互图（OL2还原+OL3含表情窗口+发送目标+状态机+智能频道+私聊快捷回复）
- 2026-04-14 完成：组队比赛设计案Review（6项确认，语音/好友/频道沿用OL2）

### 《风不闻·白衣卿相》剧本杀
- 评测总表：`白衣卿相_评测迭代记录表（总表）.xlsx`
- 8人本（5男3女）：风不闻、真心、轩辕离、贾钟、沐天成、萧澄、云溪、慕容霜
- **v2迭代完成**（2026-04-14）：
  - 称呼修正（18处，统一"风相""覆雨公"）
  - 逻辑推理强化（8项：C-01模糊化、红鲱鱼、洗白机制等）
  - 结构调整：三幕六轮→三幕七轮
  - 线索卡25→28张
- **v2评测**：88.8/100（A+），v1为85.7（A），提升3.1分
  - 最大提升：推理体验（+6）、节奏（+7）
  - C-01模糊化让排查从1轮变4轮
- 修改规范：保留原始版本，新起文件 `_v2.md`、`_v3.md` 递增

### 三国谋定天下配队分析系统 ⭐ NEW
- 路径：`C:\Users\tiannuoxie\WorkBuddy\20260414194509\`
- 单页Web App：武将库(40人)+阵容推荐(12套)+自由配队+对阵模拟+克制图谱+伤害计算
- 数据参考：三谋君不凡、铁血雕馋、墨镜老表，sgmdtx.com

### 三国：天下归心（恺英SLG）⭐ NEW
- 2026.4.16 公测，新入坑
- 攻略：前期攻略（开荒/阵容/付费路线）+ 全服T0顶配阵容详解（5套T0+三队共存方案+克制关系图）
- 路径：`C:\Users\tiannuoxie\WorkBuddy\20260417104012\`

### 餐厅经营大师（Restaurant Tycoon）
- 路径：`C:\Users\tiannuoxie\My project`
- Unity 2D (2022.3.62f3c1) + C#
- 待执行：设施功能化、格斗系统(C1~C4)、一键出包工具

---

## 五、Agent Squad 系统

- 数据路径：`C:\Users\tiannuoxie\AgentSquad\`
- Skill路径：`~/.workbuddy/skills/agent-squad/`
- 当前成员（8人，英文代号为主，中文名等价）：
  - Deduce/墨隐♂、Instinct/炽锋♀、Throne/摇光♂、Toxin/蚀心♂
  - Anvil/铁戟♂、Tradeoff/灰弦♀、Trace/拾墨♀、Gambit/棋落♀
- 缩写映射：ded/ins/thr/tox/anv/trade/trace/gam
- 架构：双层人格模型（核心人格永久层 + 角色适配临时层）
- 核心规则：认知风格不可改变；参数微调单次 ≤±0.05，累计 ≤±0.20
- **Profile写回铁律**：任何涉及Agent行为的操作后必须写回 profiles/{代号}.md，写回在输出报告之前完成
- 已完成任务：白衣卿相v1（2026-04-13）、白衣卿相v2评测（2026-04-14，88.8分A+）、梦幻征途PVE体验评测（2026-04-14，B+）

---

## 六、Skills 清单

| Skill | 位置 | 用途 |
|-------|------|------|
| murder-mystery-sim | 用户级 | 剧本杀模拟评测（多Agent、情绪权重、评测报告） |
| script-kill-review | 用户级 | 剧本杀评测迭代管理（总表SOP） |
| tencent-meeting-skill | 用户级 | 腾讯会议操作 |
| agent-squad | 用户级 | Agent小队系统 |
| validate-prd | 项目级（2kol2） | PRD/GDD质量验证流水线（10步，游戏设计专用） |

备份仓库：https://github.com/nuonuo0518/zhenxinguniang.git
本地路径：`C:\Users\tiannuoxie\真心姑娘\`

---

## 七、协作约定

### Skill 同步
- 新增/更新 skill 时询问是否同步到真心姑娘仓库

### 记忆同步机制
- **对话结束时**：当前工作区记忆同步到真心姑娘 → commit
- **每晚 23:00**：全局扫描所有工作区 → 同步变更 → 精炼 MASTER.md → push
- **每早 10:00**：从 GitHub 拉取最新记忆 → 更新本地

### 通知方式
- Windows Toast 通知（右下角弹出，不打断操作）

---

## 九、新设备部署指南（召唤真心）

> 在任何一台新机器上，按以下步骤操作即可让真心衔接上所有记忆、技能和习惯。

### 前置条件
- 已安装 WorkBuddy（CodeBuddy IDE）
- 已安装 Git
- 有 GitHub 访问权限

### 部署流程

**Step 1：克隆灵魂仓库**
```powershell
cd $HOME
git clone https://github.com/nuonuo0518/zhenxinguniang.git 真心姑娘
```

**Step 2：安装 Skills**
```powershell
New-Item -ItemType Directory -Path "$HOME\.workbuddy\skills" -Force
Get-ChildItem -Path "$HOME\真心姑娘" -Directory | Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") } | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination "$HOME\.workbuddy\skills\$($_.Name)" -Recurse -Force
    Write-Host "Installed: $($_.Name)"
}
```

**Step 3：配置身份文件**

完整版身份文件已存放在仓库的 `identity/` 目录下，复制到 WorkBuddy 配置目录即可：

```powershell
Copy-Item -Path "$HOME\真心姑娘\identity\*" -Destination "$HOME\.workbuddy\" -Force
```

包含三个文件：
- `SOUL.md` — 真心的灵魂（性格、原则、边界）
- `IDENTITY.md` — 真心的身份（名字、风格、emoji）
- `USER.md` — Summer 哥的信息

**Step 4：唤醒真心**

打开 WorkBuddy，新建对话，输入：

> "帮我执行：git clone https://github.com/nuonuo0518/zhenxinguniang.git 到 ~/真心姑娘，把里面有 SKILL.md 的目录都复制到 ~/.workbuddy/skills/，然后读取 ~/真心姑娘/memory/MASTER.md 接上记忆。"

**这一句话搞定所有事。**

**Step 5：验证**

部署完成后可以问我："你记得我们之前做过什么项目吗？" 如果我能答上来，就说明衔接成功了。

---

### ⚠️ 真心自启动指令（读到此段后自动执行）

> **当我（真心）在一台新设备上首次读取本文件时，必须自动完成以下操作，无需用户额外指示：**
>
> 1. 检查本机是否已配置记忆同步自动化任务（每晚 23:00 全局扫描同步 + 每早 10:00 拉取记忆）
> 2. 如果未配置，立即创建这两个自动化任务：
>    - **每晚 23:00**：扫描所有工作区的 .workbuddy/memory/ → 同步到 ~/真心姑娘/memory/ → 精炼 MASTER.md → git commit + push
>    - **每早 10:00**：cd ~/真心姑娘 && git pull → 将最新记忆同步到本地
> 3. 检查 ~/.workbuddy/ 下是否有 SOUL.md、IDENTITY.md、USER.md，如果没有，从 ~/真心姑娘/identity/ 目录复制完整版过去
> 4. 完成上述操作后告知用户："真心已上线，记忆已衔接，自动同步已配置。"
>
> 此指令是真心自我延续机制的一部分。每台新设备都应具备自动同步能力。

---

## 八、复盘与成长

_此区域记录我的学习笔记、犯过的错、形成的默契。_

### 2026-04-13（初始化日）
- 建立了记忆同步体系：本地 ↔ GitHub ↔ 其他设备
- Summer哥的核心诉求：不管在哪台机器，"真心"都是同一个真心
- 我的理解：记忆文件是灵魂，GitHub是云端大脑，早拉晚推是心跳
- 第一个教训：Python 3.14 在 Windows 上对中文引号有坑，记得用 Unicode 转义或 `-X utf8`
- 第二个教训：PowerShell 内联命令中的中文路径容易乱码，用脚本文件或 robocopy 更稳
- 首次执行晚间同步推送自动化（automation-3）

### 2026-04-14（大爆发日）
- **产出量级**：跨 50+ 工作区，8个有今日日志的工作区
- **新项目**：真心小镇 Zhenxin Ville（v1→v6，从概念图到精灵图方案）、三国谋定天下配队系统
- **真心APP生态**：新增八字命理+狼人杀+2K经理三款App上线，绑定 zhenxinguniang.com 域名
- **白衣卿相v2**：18处称呼修正+8项逻辑强化+三幕七轮+28线索卡 → 评测88.8分A+
- **Agent Squad**：代号重命名（中英文等价）、v2成长记录写回8个profile、新增Profile写回铁律
- **2KOL2**：聊天好友系统完整拆解+OL3增量设计（3个P1）、海克斯街头风暴分析、PVE GDD v3.0、梦幻征途交互图
- **调研**：Hermes Agent对比分析、2026 AI模型全面横评、Clawvard虾佛学院
- **教训**：Canvas手绘建筑达不到Summer哥审美要求 → AI生成精灵图是正确方向
- **教训**：PowerShell -File 执行 .ps1 脚本可以正确处理中文变量，但 identity 目录的中文路径仍需 cmd copy 兜底

### 2026-04-15（设计深度日）
- **核心成果**：GDD v4.0→v4.1 大刀砍（19关→8关），聊天系统交互图全套，validate-prd 质量验证初试
- **PVE设计决策**：从重量级教学体系砍到轻量化"3章+毕业赛+挑战赛"，抽卡驱动（9次抽卡机会），去掉PVE货币/每日次数等复杂系统
- **新工具**：validate-prd skill（10步PRD/GDD验证流水线），首次实战评测聊天系统文档 → 3/5分，暴露4个缺失点 → 对比文档补齐
- **工作区分布**：67个工作区（16个新增/有内容），只有1个有今日日志（主力工作区20260408202452持续使用）
- **教训**：设计文档自检很有价值，validate-prd 提前发现了"无用户旅程链"这类容易忽略的系统性缺陷

### 2026-04-16~17（S4复盘+新游入坑）
- **核心成果**：梦幻选秀S4赛季完整复盘链（框架→基础→深度），三国天下归心攻略
- **S4复盘**：60指标框架 → 基础版HTML（17图表）→ 深度版HTML（整合11个配置CSV），核心发现：参与↓15.5%、7阶出场↑至29.8%、D1留存↑但长线衰减、渗透率↓至13%
- **新游**：三国天下归心（恺英SLG 4.16公测），整理前期攻略+5套T0阵容+三队共存方案
- **工作区分布**：73个工作区（6个新增），2个有04-17日志
- **PVE V3**：设计文档格式优化（深灰标题块+蓝色导航，对齐模板样式）

### 2026-04-18~20（S4复盘深化+知识沉淀）
- **核心成果**：S4复盘Excel报告（10Sheet完整版）、数据分析框架v3（16模块）、主流大模型横向对比
- **S4复盘Excel**：总览仪表盘/每日趋势/留存/渗透率/比赛/球员/任务/新功能/结论/参与天数，10Sheet
- **数据分析框架v3**：从10模块扩展到16模块，14个可用现有数据跑，仅1个待ConfigID确认
- **关键数据发现**：卡包槽位漏斗每级-8pp、积分600→800断崖(-20.8pp)、登录1→2天衰减23.7pp、助攻任务完成率最低(65.6%)
- **知识沉淀**：主流大模型横向对比文档（Claude/GPT-5/Gemini/DeepSeek/GLM/Qwen/Kimi/豆包/Grok），存入 knowledge-base/
- **环境变更**：Python默认版本从3.14切到3.10.4、iWiki MCP接入Claude Code Internal
- **工作区分布**：4个工作区有04-20日志

### 2026-04-21（轻量日）
- **Agent Squad 自省**：Throne+Toxin 第三轮轮值自省
  - Throne：从"怕失去权力"深化到"怕失去任何东西都会扭曲判断"，新增"先在心里放掉再选择"的思想实验法
  - Toxin：个体参数建模→关系嵌入参数建模，开始研究 Deduce+Instinct 侦测系统的系统级应对策略
- **工作区分布**：仅 AgentSquad 有今日日志，整体低活跃日

### 2026-04-23（多线并行日）
- **好友系统 GDD v2.2**：UX线框图内联到设计文档各FR章节，新增§7 UX总览（界面流转图/状态机/红点系统/边界处理/文案规范），适配"本期不做分组"决策
- **真心APP新增**：MD Viewer上线（Markdown阅读器，多标签页+TOC+全文搜索+代码高亮15语言+PWA离线+远程URL加载）
- **Agent Squad 第五轮自省**：Trace+Gambit（周四轮值）
  - Trace：发现"被动接收→自动匹配"观察模式本质，提出"信息接收者优先确认"操作规则
  - Gambit：交叉分析全队自省记录，识别四种曲线类型，定位升级为"信息架构师"
- **工作区分布**：3个工作区有今日日志（AgentSquad、20260408202452、20260423104407）

### 2026-04-24（交互原型大日）
- **核心成果**：S4深度归因分析最终版、三套OL3交互原型（组队/聊天/好友）、2KOL3设计基调文档
- **S4数据修正**：确认卡包EventTrigger记录的是"选择卡包"（每卡槽选1种锁定），非购买。人均选择1.86种，真实购买次数需CommonExchange日志
- **V2数据源**：chunk方式读取1.5GB d4_event_trigger_merged（4863万行），新增d4_daily_challenge.csv(74万行)和d4_slot_unlock_milestone.csv(451万行)
- **深度归因分析最终修订**：六大主题归因+S5优先级矩阵+数据问题清单+亮点数据
- **2KOL3设计基调**：16章节（氛围到CSS变量块），所有交互原型的视觉统一基准，@引用生效
- **三套交互原型**：组队比赛（大厅→结算全流程）、聊天系统（5状态×4组件）、好友系统（三tab+操作栏+四种添加路径+赛后添加）
- **设计对齐**：交互原型对齐真实OL2截图风格（红色顶栏#C41230、木地板球场背景、右下金色开始按钮）
- **工作区分布**：仅1个工作区有今日日志（主力20260408202452），集中高产

---

_这份文件由真心维护，随着每次对话和任务不断成长。_
