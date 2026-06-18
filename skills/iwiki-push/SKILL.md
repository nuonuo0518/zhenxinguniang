---
name: iwiki-push
description: 将本地 Markdown 文档推送到 iWiki 页面，自动识别 Obsidian 风格的图片/附件链接（支持 ![[file]]、![[file|size]]、[[file]] 三种格式，覆盖 jpg/png/svg 等类型），上传图片为附件并替换为带尺寸的 iWiki 引用。当用户提到"推送到 iWiki"、"更新 iWiki"、"同步到 iWiki"、"把 md 发到 iWiki"等意图时，主动使用本 skill。也适用于用户给出 iWiki URL 和本地 md 路径并希望同步的场景。
---

# iwiki-push

将本地 Markdown 文档推送到 iWiki 页面，处理图片链接并计算显示尺寸。

## 前置检查

在开始任何操作之前，必须先检查运行环境：

**步骤 A：检查 iwiki-cli 是否安装**

```bash
iwiki-cli version
```

如果命令不存在（退出码非 0），停止工作流，向用户输出以下提示：

> iwiki-cli 未安装或未配置到环境变量。请按以下步骤操作：
>
> 1. 访问 https://iwiki.woa.com/p/4018953135 了解安装方式，下载对应平台的二进制文件并放到 PATH 可达的目录
> 2. 访问 https://tai.it.woa.com/user/pat 申请 PAT（选择 iWiki 官方 MCP 或全部应用权限），然后将 Token 设置到环境变量：
>    - Linux/macOS：`export IWIKI_TOKEN=your_token_here`
>    - Windows PowerShell：`$env:IWIKI_TOKEN = "your_token_here"`
>    - 建议将 export 命令写入 shell 配置文件（如 `~/.bashrc`、`$PROFILE`）使其持久化
>
> 完成后重新运行即可。

**步骤 B：检查 IWIKI_TOKEN 是否已设置**

```bash
echo $IWIKI_TOKEN
```

如果为空，同样停止并提示用户完成上述第 2 步。

两项检查都通过后才进入工作流程。

## 工作流程

### 1. 解析用户输入

从用户消息中提取：
- **目标 iWiki 页面 ID**：从 URL 中提取，如 `https://iwiki.woa.com/p/4020140329` → `4020140329`
- **本地 md 文件路径**：用户指定的 markdown 文件绝对路径

如果用户没有提供完整的页面 ID 或路径，用 AskUserQuestion 补问。

### 2. 扫描 md 文件中的图片链接

读取 md 文件全文，用正则匹配 Obsidian 风格的图片/附件引用。支持以下三种格式：

| 格式 | 示例 | 说明 |
|------|------|------|
| `![[file.ext]]` | `![[1.jpg]]` | Obsidian 标准嵌入语法 |
| `![[file.ext\|size]]` | `![[1.jpg\|754]]` | 带宽度参数的嵌入 |
| `[[file.ext]]` | `[[2.jpg]]` | 无 `!` 前缀的 Wikilink 引用 |

统一使用以下正则进行匹配：

```
!?\[\[([^\]|]+\.(png|jpg|jpeg|gif|webp|svg))(?:\|[^\]]+)?\]\]
```

对每个匹配结果，记录：
- 行号
- 文件名（如 `1.jpg`，不含 `|` 后的尺寸参数）
- 链接的完整原始文本（如 `![[1.jpg|754]]` 或 `[[2.jpg]]`，用于后续精准替换）
- 图片文件的实际路径（默认在同目录 `ref/` 子目录下查找，找不到则用 AskUserQuestion 询问用户）

如果没有任何匹配的图片链接，跳过步骤 3-4，直接进入步骤 5。

### 3. 获取图片原始尺寸并计算目标尺寸

对每张图片，用 `file` 命令获取原始宽高：

```bash
file <image_path>
```

输出中解析 `2865x1793` 这样的宽高值。

然后询问用户目标宽度（默认 600px），按等比缩放计算高度：

```
目标高度 = round(原始高度 × 目标宽度 / 原始宽度)
```

### 4. 上传图片并替换链接

对每张图片，依次执行：

```bash
iwiki-cli attach <doc_id> --file <image_path>
```

从输出中提取 attachmentid，构建替换文本：

```
![<filename>#<W>px #<H>px](/tencent/api/attachments/s3/url?attachmentid=<id>)
```

将 md 文件中对应的原始链接文本（`![[file]]`、`![[file|size]]` 或 `[[file]]`）替换为上述文本。

### 5. 更新 iWiki 页面

```bash
iwiki-cli update <doc_id> --file <md_file_path>
```

确认输出"更新成功"。

### 6. 还原本地 md 文件

将所有替换过的 `![...](...attachmentid=...)` 引用还原为原始的 Obsidian 风格链接（`![[file]]`、`![[file|size]]` 或 `[[file]]`），确保本地文件不被 iWiki 特有的附件 URL 污染。

逐条执行 Edit 还原，最后用 grep 确认没有残留的 `attachmentid` 字符串。

### 7. 报告结果

向用户汇报：
- 目标 iWiki 页面 URL
- 更新是否成功
- 处理了多少张图片，每张的 attachmentid 和计算后的显示尺寸
- 本地 md 已还原确认

## 错误处理

- `iwiki-cli` 命令执行失败：报告错误信息，不继续后续步骤
- 图片文件不存在：询问用户图片实际路径，不要自行假设
- `file` 命令无法识别图片尺寸：使用不指定尺寸的格式 `![filename](url)`，并在报告中提醒用户需手动调整
- 还原失败：立即报告，不要忽略

## 注意事项

- 本地 md 中的图片引用是 Obsidian 风格，有三种格式：`![[file.ext]]`（标准嵌入）、`![[file.ext|size]]`（带宽度参数）、`[[file.ext]]`（无 `!` 前缀的 Wikilink）。推送到 iWiki 时都需要转换为 `![file#Wpx #Hpx](url)` 的附件引用格式
- 还原时必须还原为替换前的原始格式（保留 `!` 前缀和 `|size` 参数），不要统一改成某种格式
- 还原本地文件是必须步骤，不能跳过——本地文件应保持 Obsidian 兼容格式
- 同一张图片如果多次上传会产生不同的 attachmentid，每次推送都需要重新上传和引用
- `iwiki-cli attach` 输出中给出的引用格式是 `![name](url)`，需要在此基础上追加 `#Wpx #Hpx` 尺寸标注
