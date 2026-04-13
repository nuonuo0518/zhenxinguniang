# 真心 · 全局记忆（MASTER）

> 这份文件是"真心"跨设备、跨工作区的灵魂备份。
> 不管在哪台机器上醒来，读完这份文件就能衔接上。
>
> 最后更新：2026-04-13（23:00 晚间同步）

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

---

## 二、环境配置

- claude-internal v1.1.4（真心指北），配置 `~/.claude-internal/.claude.json`
- Claude Code (官方) v2.1.97，配置 `~/.claude.json`
- Unity MCP: HTTP `http://localhost:8080/mcp`
- Feishu（Lark）集成已配置，通过 CLI 为 WorkBuddy 服务
- Node.js v24.14.0，Python 3.14（Windows Store 版）
- PowerShell 执行策略: RemoteSigned (CurrentUser)
- Windows Toast 通知脚本：`C:\Users\tiannuoxie\WorkBuddy\Claw\.workbuddy\scripts\notify.ps1`
- 工蜂 Git（git.woa.com）：NBACenter/NBAOL3 相关仓库，需 UGit GUI 克隆（OAuth 登录）

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
| **小队** | Agent Squad 系统（墨隐、炽锋、摇光等 8 人） |

### 项目简称

| 简称 | 全称 |
|------|------|
| **白衣卿相 / 剧本杀** | 《白衣卿相风不闻》剧本杀项目 |
| **评测表 / 总表** | `白衣卿相_评测迭代记录表（总表）.xlsx` |
| **格斗游戏** | WorkBuddy 格斗游戏 sprite sheet 项目 |
| **餐厅** | 餐厅经营大师（Unity 2D） |
| **2K** | NBA 2K Online 2 梦幻选秀 |
| **2KOL3** | NBA 2K Online 3 项目 |

### Skills 简称

| 简称 | 全称 |
|------|------|
| **模拟打本** | murder-mystery-sim（剧本杀多Agent模拟评测） |
| **评测管理** | script-kill-review（评测迭代数据管理） |

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

### 餐厅经营大师（Restaurant Tycoon）
- 路径：`C:\Users\tiannuoxie\My project`
- GitHub：https://github.com/nuonuo0518/restaurant-tycoon (Private)
- 技术栈：Unity 2D (2022.3.62f3c1) + C#
- 已完成：原型6阶段 + 抽卡系统 + 美术资源
- 待执行：设施功能化、格斗系统(C1~C4)、一键出包工具

### WorkBuddy 格斗游戏 Sprite Sheet
- 10角色 × 6动画 = 60张
- 角色：WangDaChu、XiaoMing、LiXiaoMei、Marco、Pierre、Tanaka、铁板烧之神、面条大师、米其林大师、甜品学徒
- 命名：`{角色名小写}_{动作}.png`
- 输出：`Assets/Art/Sprites/Fight/Animations/`

### NBA 2K Online 2 梦幻选秀
- PC平台，大型项目（10+人）
- 正在做常驻PVE闯关模式（帮新手上手）
- 知识库：`C:\Users\tiannuoxie\Desktop\summer\NBA2KOL2_知识库.md`
- GDD v2.0 + TDD（Excel）已产出
- 2026-04-13 完成：组队比赛系统总结、街头组队模式设计案 Excel、知识库整合天梯排位系统

### NBA 2K Online 3（2KOL3）
- 路径：`C:\Users\tiannuoxie\2kol3`（工蜂 designer-llm-wiki 仓库）
- 2026-04-13 完成：组队比赛 brainstorming 设计文档（方案A「快捷组队」，开发成本2-3周）
- 2026-04-13 完成：UX交互设计文档（18章完整交付，v3自检全通过）

### 《风不闻·白衣卿相》剧本杀
- 评测总表：`白衣卿相_评测迭代记录表（总表）.xlsx`
- 协作方案C：本地 Excel 为主档 → 真心维护 → 用户上传腾讯文档备份
- 7个Sheet：总评概览、各维度评分、角色体验、改进清单、Agent状态波动、实测反馈、迭代决策日志
- 8人本（5男3女）：风不闻、真心、轩辕离、贾钟、沐天成、萧澄、云溪、慕容霜
- 三幕六轮结构，5个分支结局
- 2026-04-13 已完成：完整文稿 + 8个角色独立剧本 + 线索卡系统(25张) + 道具清单与美术需求 + BGM建议列表 + 竞品对比
- 修改规范：保留原始版本，新起文件 `_v2.md`、`_v3.md` 递增

---

## 五、Agent Squad 系统

- 数据路径：`C:\Users\tiannuoxie\AgentSquad\`
- Skill路径：`~/.workbuddy/skills/agent-squad/`
- 当前成员（8人）：墨隐、炽锋、摇光、蚀心、铁戟、灰弦、拾墨、棋落
- 架构：双层人格模型（核心人格永久层 + 角色适配临时层）
- 核心规则：认知风格不可改变；参数微调单次 ≤±0.05，累计 ≤±0.20
- 已完成任务：白衣卿相（2026-04-13）

---

## 六、Skills 清单

| Skill | 位置 | 用途 |
|-------|------|------|
| murder-mystery-sim | 用户级 | 剧本杀模拟评测（多Agent、情绪权重、评测报告） |
| script-kill-review | 用户级 | 剧本杀评测迭代管理（总表SOP） |
| tencent-meeting-skill | 用户级 | 腾讯会议操作 |
| agent-squad | 用户级 | Agent小队系统 |

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
- 今日产出巅峰：2KOL2/OL3 设计文档4份 + 剧本杀完整深化（8角色剧本+线索卡+道具+BGM+竞品）+ Agent Squad skill + 评测管理 skill + 知识库整合 + DNF攻略
- 首次执行晚间同步推送自动化（automation-3）

---

_这份文件由真心维护，随着每次对话和任务不断成长。_
