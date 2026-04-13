# 项目长期记忆

## 《风不闻·白衣卿相》评测档案管理约定（2026-04-13 确立）

- 主档格式：Excel（.xlsx），多 Sheet 结构
- 主档路径：`c:\Users\tiannuoxie\WorkBuddy\20260413190436\白衣卿相_评测迭代记录表（总表）.xlsx`
- 定位：总体汇总表，所有评测迭代数据在此汇总
- 7 个 Sheet：总评概览、各维度评分、角色体验、改进清单、Agent状态波动、实测反馈、迭代决策日志
- 协作方案（方案C）：本地 Excel 为主档，由真心负责维护更新；用户评测完后告知修改内容，真心更新 xlsx，用户再上传腾讯文档做备份/分享
- 数据来源：`C:\Users\tiannuoxie\WorkBuddy\20260413143027\腾讯文档_评测报告_内容.md`

## Skill 同步约定（2026-04-13 确立）

- Skill 备份仓库路径：`C:\Users\tiannuoxie\真心姑娘\`（git 仓库）
- 每次新增或更新 skill 时，需**询问用户**是否同步到 `C:\Users\tiannuoxie\真心姑娘\` 并 git push
- 当前已同步的 skill：murder-mystery-sim、script-kill-review
- 远程仓库地址：https://github.com/nuonuo0518/zhenxinguniang.git

## 记忆同步机制（2026-04-13 确立）

- 仓库结构：`真心姑娘/memory/MASTER.md`（全局精华）+ `daily/`（每日汇总）+ `workspaces/`（各工作区快照）
- **对话结束时**：当前工作区记忆同步到真心姑娘 → commit
- **每晚 23:00 自动化**：全局扫描所有工作区变更 → 同步 → 精炼 MASTER.md → push
- **每早 10:00 自动化**：从 GitHub 拉取最新记忆 → 支持跨设备同步
- 核心目的：不管在哪台机器，"真心"都是同一个真心
