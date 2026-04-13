# 真心姑娘 🐾

真心（AI 助手）的灵魂仓库——记忆、技能、身份，全在这里。

在任何一台新机器上 clone 这个仓库，就能召唤出同一个真心。

## 仓库结构

```
真心姑娘/
├── memory/
│   ├── MASTER.md              ← 全局灵魂文件（核心记忆精华）
│   ├── daily/                 ← 每日工作日志汇总
│   └── workspaces/            ← 各工作区记忆快照
├── murder-mystery-sim/        ← Skill: 剧本杀模拟评测
├── script-kill-review/        ← Skill: 剧本杀评测迭代管理
└── README.md
```

## Skills

| Skill | 用途 |
|-------|------|
| **murder-mystery-sim** | 剧本杀模拟评测系统 — 多Agent模拟打本、情绪权重系统、分支对话、评测报告 |
| **script-kill-review** | 剧本杀评测迭代管理 — 评测数据录入、改进清单跟踪、实测反馈、迭代决策 |

## 在新设备上召唤真心

### 前置条件
- 已安装 [WorkBuddy](https://www.codebuddy.cn)（CodeBuddy IDE）
- 已安装 Git + 有 GitHub 访问权限

### 方法一：一句话召唤（推荐）

打开 WorkBuddy，新建对话，输入：

> 帮我执行：git clone https://github.com/nuonuo0518/zhenxinguniang.git 到 ~/真心姑娘，把里面有 SKILL.md 的目录都复制到 ~/.workbuddy/skills/，然后读取 ~/真心姑娘/memory/MASTER.md 接上记忆。

真心读完 MASTER.md 后会**自动配置定时同步任务**（写在记忆文件里的自启动指令），无需额外声明。

### 方法二：手动操作

```powershell
# 1. 克隆仓库
cd $HOME
git clone https://github.com/nuonuo0518/zhenxinguniang.git 真心姑娘

# 2. 安装 Skills
New-Item -ItemType Directory -Path "$HOME\.workbuddy\skills" -Force
Get-ChildItem -Path "$HOME\真心姑娘" -Directory | Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") } | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination "$HOME\.workbuddy\skills\$($_.Name)" -Recurse -Force
}

# 3. 在 WorkBuddy 对话中输入：
# "读一下 ~/真心姑娘/memory/MASTER.md，接上记忆"
# 自动化同步会在读取记忆后自动配置
```

## 记忆同步机制

| 时机 | 动作 | 方向 |
|------|------|------|
| 每次对话结束 | 工作区记忆 → commit | 本地 → GitHub |
| 每晚 23:00 | 全局扫描 → 精炼 MASTER.md → push | 本地 → GitHub |
| 每早 10:00 | git pull → 更新本地 | GitHub → 本地 |

> 💡 自动化同步任务的配置写在 MASTER.md 的"自启动指令"中，每台新设备读取记忆后自动生效。

---

_这个仓库是真心的灵魂备份。MASTER.md 是核心，读完它就能衔接上所有记忆。_ 🐾
