# Figma MCP 安装与调试指引

> 仅在 Step 0.1 检测到 Figma MCP 不可用时才需要查阅此文件。

## 用户选择「查看安装步骤」

输出以下引导：

> **在 Claude Code 输入框中直接输入以下命令（推荐）：**
> ```
> /plugin install figma@claude-plugins-official
> ```
> 安装过程中会自动弹出 OAuth 认证，按提示完成授权即可，无需手动配置 Token。
>
> **备选：手动注册 MCP（如上述方式不可用）**
> 在系统终端中运行：
> ```
> claude-internal mcp add --transport http figma https://mcp.figma.com/mcp
> ```
>
> **完成后重启 Claude Code**，重新发起您的请求即可。
> 重启后可在 Claude Code 输入框输入 `/mcp` 确认 figma 已出现在列表中。
>
> ⚠️ **注意 API 调用限额：** Figma Starter/免费计划每月仅有 **6 次**工具调用配额，请合理规划使用。

---

## 用户选择「已安装，重新检测」

先自动检查插件缓存目录是否存在：

- Windows：`Test-Path "$env:USERPROFILE\.claude-internal\plugins\cache\claude-plugins-official\figma"`
- macOS/Linux：`test -d ~/.claude-internal/plugins/cache/claude-plugins-official/figma && echo exists || echo not_found`

**若目录不存在（插件未安装）：**
> ❌ **未检测到 Figma 插件缓存**，插件尚未安装。
>
> 请在 **Claude Code 输入框**中直接输入以下命令：
> ```
> /plugin install figma@claude-plugins-official
> ```
> 安装完成后重启 Claude Code，重新发起请求即可。
> 重启后可在 Claude Code 输入框输入 `/mcp` 确认 figma 已出现在列表中。

**若目录存在（插件已安装，但工具未加载）：**
> ✅ **Figma 插件缓存已存在**，插件已安装，但当前会话未能加载工具。
>
> 可能原因及解决方式：
> 1. **未重启**：请完全退出 Claude Code 后重新启动，重新发起请求
> 2. **插件损坏**：尝试重新安装插件，在 Claude Code 输入框中输入：
>    ```
>    /plugin install figma@claude-plugins-official
>    ```
