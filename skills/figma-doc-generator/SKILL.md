---
name: Figma文档生成
description: Generate structured design documentation from Figma files with intelligent image handling. Uses metadata extraction as foundation with optional 1/3-resolution thumbnails for visual context (colors, layout, typography). Balances accuracy (40-60% improvement) with efficiency (minimal token overhead). Use when users provide Figma design URLs requesting documentation, design analysis, visual extraction, or structured interpretation. Supports large design files through sequential processing. Triggers include "analyze this Figma design", "generate doc from Figma", "extract design info", "what does this design look like", or when users share Figma links asking for design documentation.
---

# Figma Design Documentation Generator

Generate comprehensive, structured design documentation from Figma files by extracting metadata and structural information without downloading bitmap images. This approach avoids API Error 400 issues common with large design files.

## Overview

1. **Metadata-only extraction** - Uses `get_metadata` instead of `get_design_context` or `get_screenshot`
2. **Selective node targeting** - Identifies and extracts only key design nodes
3. **Context-optimized processing** - Uses sequential single-threaded processing to avoid API rate limits
4. **Structured documentation** - Generates organized Markdown documents with design specifications

For usage examples, see `references/examples.md`.

---

## Core Workflow

> **PowerShell 编码规则**：所有含中文输出的 PowerShell 命令，首行必须加 `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`。以下代码块中均已省略此行，执行时自行补充（Phase 0.0 和 Phase 0.3 的示例除外）。

### Phase 0: Environment & Input Validation (ALWAYS FIRST)

#### Step 0.0 — Check for In-Progress Session (Compact Resume Detection)

**Run this before anything else — even before checking for Figma MCP.**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Get-ChildItem -Path "." -Recurse -Filter "session.json" -Depth 3 -ErrorAction SilentlyContinue | Select-Object -First 1 FullName
```

**If `session.json` is found:**
1. Read it: `Get-Content "{found_path}" | ConvertFrom-Json`
2. Check for checkpoint: `Get-Content "{outputDir}\{designName}\checkpoint.json" -ErrorAction SilentlyContinue | ConvertFrom-Json`
3. Report recovery state:
   ```
   🔄 检测到未完成的任务，正在恢复...
   📁 设计名称: {designName}
   🔑 FileKey: {fileKey}
   📊 已完成节点: {nodesProcessed}/{nodesTotal}（来自 checkpoint.json）
   ➡️ 跳过 Phase 0.1 ~ Phase 2，直接恢复到 Phase {resumePhase}
   ```
4. **Skip Phases 0.1 through 2 entirely.** Determine resume phase:
   - checkpoint exists + nodesProcessed < nodesTotal → resume Phase 3 from next node
   - checkpoint exists + nodesProcessed == nodesTotal → resume Phase 4/5
   - no checkpoint or nodesProcessed == 0 → resume Phase 2 (re-fetch root metadata)
   - `figma-analysis.json` exists → resume Phase 6 (doc generation only)

**If no `session.json` found:** Continue to Step 0.1 (normal flow).

> session.json 在任何 Figma API 调用之前写入磁盘，确保 compact 发生时也能通过 Phase 0.0 自动恢复。

---

#### Step 0.1 — Check Figma MCP Availability

Verify that tools starting with `mcp__plugin_figma_figma__` (e.g. `get_metadata`, `get_screenshot`) are available.

**If NOT available**, stop and use `AskUserQuestion`:

```
question: "⚠️ 未检测到 Figma MCP 插件\n\n本技能依赖 Figma 官方 MCP 插件，当前环境中未发现相关工具，无法继续执行。\n\n请选择下一步操作："
options:
  - label: "查看安装步骤"
    description: "显示安装方法，只需在 Claude Code 输入框中输入一行命令即可"
  - label: "已安装，重新检测"
    description: "如果您认为已安装但未被识别，选此项查看排查建议"
```

Then follow `references/mcp-setup.md` for the detailed installation and diagnosis steps. Do NOT proceed further — wait for the user to complete setup and restart.

**If available**, continue to Step 0.2.

---

#### Step 0.2 — Validate Figma Data Source

Check whether the user has provided a Figma URL or file key.

**Valid sources:**
- A Figma URL: `https://www.figma.com/design/{fileKey}/...`
- An explicit file key string (alphanumeric, ~22 characters)
- A node ID alone is NOT sufficient

**Detection logic:**
1. Scan for a `figma.com/design/` URL → extract and proceed to Phase 1
2. Scan for a standalone file key → proceed to Phase 1
3. **Neither found**: ask via `AskUserQuestion`:
   ```
   question: "请提供 Figma 设计数据源。您可以提供以下任一形式："
   options:
     - label: "Figma 链接（推荐）"
       description: "粘贴完整的 Figma 设计 URL"
     - label: "手动输入 File Key"
       description: "输入 Figma 文件 Key 及可选的 Node ID"
   ```

---

### Phase 0.3 — [MANDATORY] Confirm Output Directory

> ⛔ **STOP — THIS STEP IS REQUIRED BEFORE PHASE 1.**
> Do NOT proceed to Phase 1 until the output directory is confirmed.
> Do NOT assume or infer a default path. Always ask explicitly.

**First, check if the user already specified a path** in their request (e.g., "保存到 D:/docs", "output to ./design-docs"). If yes, use it directly and confirm it aloud, then proceed.

**If no path was specified** (the common case), you MUST pause and ask via `AskUserQuestion` before doing anything else:

```
question: "请确认文档的输出目录："
options:
  - label: "当前工作目录"
    description: "保存到当前目录下，以设计文件名命名的子目录"
  - label: "指定路径"
    description: "手动输入目标目录路径"
```

If user chooses "指定路径", ask for the path as a follow-up. Confirm the resolved output path before continuing:

> 📁 输出目录确认：`{output_dir}` — 文档将直接保存至此目录

**Skipping this phase is a workflow violation.** It causes files to be saved in unexpected locations, which is harder to fix than asking upfront.

**Immediately after output dir is confirmed — write session.json bootstrap (REQUIRED):**

This is the most important disk write of the entire run. It must happen before any Figma API calls. If context compaction fires during Phase 2's root metadata call, this file is the only thing that allows automatic recovery via Phase 0.0.

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
New-Item -ItemType Directory -Force -Path "{output_dir}" | Out-Null
@{
  fileKey = "{fileKey}"; designName = "{designName}"; outputDir = "{output_dir}"
  rootNodeId = "{nodeId_from_url_or_TBD}"; imageLayer = "TBD"
  startedAt = (Get-Date -Format "o"); phase = "0.3"; status = "in_progress"
} | ConvertTo-Json | Out-File "{output_dir}\session.json" -Encoding UTF8
Write-Output "SESSION bootstrapped"
```

Wait for `SESSION bootstrapped` confirmation before continuing to Phase 1.

---

### Phase 1: Initial Analysis

Extract file key, design name, and node ID from the URL:
- Format: `https://www.figma.com/design/{fileKey}/{fileName}?node-id={nodeId}`
- nodeId: convert dash to colon (e.g. `0-1` → `0:1`)

**Refresh `session.json` with finalized parameters** (it was bootstrapped in Phase 0.3; now update it with confirmed values including imageLayer once known). Use the Session Update Templates in `references/sequential-processing.md` — Phase 1 Refresh block (set `rootNodeId` to confirmed value, `phase` to `"1"`).

After Phase 1.1 determines imageLayer, do a second refresh using the Phase 1.1 Refresh template from `references/sequential-processing.md`.

### Phase 1.1: Image Quality Configuration

Parse image quality from user request:

| Parameter | Layer |
|-----------|-------|
| `--image-quality low` or `--no-images` | Layer 0 (metadata only) |
| `--image-quality medium` or no param | Layer 1 (1/3 resolution) **[DEFAULT]** |
| `--image-quality high` | Layer 2 (1/2 resolution) |
| `--image-quality ultra` | Layer 3 (full resolution) |

**Intent detection (when no flag specified):**

| Keywords | Layer |
|----------|-------|
| 色彩/配色/颜色, colors/palette | Layer 1 |
| 排版/字体, typography/fonts | Layer 1 |
| 布局/间距, layout/spacing | Layer 1 |
| 组件细节/精确, components/detailed | Layer 2 |
| 快速/仅元数据/不要图片, quick/no images | Layer 0 |

**Node-count fallback** (no keywords): defer to Phase 2.1 after root node count is known — nodes < 50 → Layer 1; nodes > 50 → suggest Layer 0.

If the user specified `--image-quality` explicitly, that takes precedence over all intent detection and node-count fallback.

**Layer reference:**

| Layer | Resolution | Tokens/Node | Accuracy gain |
|-------|-----------|-------------|---------------|
| Layer 0 | Metadata only | ~50 | baseline |
| Layer 1 | 853×480 (1/3) | ~185 | +40-60% |
| Layer 2 | 960×540 (1/2) | ~300 | +50-70% |
| Layer 3 | 1500×3000 (full) | ~2050 | maximum |

Report to user: "图片精度设置: [Layer配置]。将使用[Layer名称]进行分析（估计增加约[X] tokens）"

---

### Phase 2: Explore Design Structure

**Goal: obtain the top-level frame list ONLY. This is ANTI-BLOAT mode — minimize what you read and keep in context.**

**Tool selection — always use `get_metadata`:**

| Tool | Use | Avoid |
|------|-----|-------|
| `get_metadata` | ✅ Always — structure, text, dimensions | — |
| `get_screenshot` | ⚠️ Layer 1-3 only, conditional | never as substitute for metadata |
| `get_design_context` | ❌ Never — causes API Error 400 | — |

```
mcp__plugin_figma_figma__get_metadata({
  fileKey: "abc123",
  nodeId: "0:1",
  clientLanguages: "typescript,javascript",
  clientFrameworks: "react"
})
```

Always provide `clientLanguages` and `clientFrameworks` (use "unknown" if uncertain).

**⚠️ CRITICAL: The root XML is a structural index, NOT content to analyze.**
When the response arrives, do exactly this and nothing more:
1. Scan XML for `<FRAME>`, `<COMPONENT>`, `<GROUP>` elements at **depth ≤ 2 only**
2. Extract: `nodeId`, `nodeName`, `nodeType` for each top-level child → compact list (~10–20 items)
3. Count approximate total node count (for Phase 2.1 complexity analysis)
4. **STOP. Do NOT read nested content, do NOT quote text nodes, do NOT analyze attributes.**

Everything interesting about each node will be extracted individually in Phase 3. Trying to interpret the full root XML here is wasteful and risks triggering compaction.

**Immediately write root XML to disk and evict:**

```powershell
New-Item -ItemType Directory -Force -Path "{output_dir}\figma-metadata" | Out-Null
$xml = @'
{paste full XML content here}
'@
$xml | Out-File -FilePath "{output_dir}\figma-metadata\root-0-1.xml" -Encoding UTF8
Write-Output "ROOT XML SAVED"
```

Wait for `ROOT XML SAVED` confirmation, then declare: **"根节点 XML 已落盘，不再保留原始 XML 于工作记忆中。"** — only the extracted node ID list and total count are kept in context going forward.

**Update session.json phase marker** using the Phase 2 Update template in `references/sequential-processing.md`.

### Phase 2.1: Design Complexity Analysis

Count node types, then apply:

```
total_nodes < 15      → "Simple"      → select ALL meaningful nodes (5-8)
total_nodes 15-50     → "Medium"      → select key functional nodes (8-12)
total_nodes 51-150    → "High"        → representative nodes only (5-8)
total_nodes > 150     → "Very High"   → strict selection (3-5 max), recommend Layer 0
```

**Node selection priority:**
1. Annotation frames (TEXT nodes with keywords: 说明/流程/规格/注释)
2. Functional frames (distinct UI states/features)
3. Component definitions (1-2 representative variations)
4. Decorative/utility frames — skip

**Finalize image layer here** (if not already set by explicit `--image-quality` flag):
- Apply node-count fallback from Phase 1.1 using the now-known total count
- Very High complexity → recommend Layer 0, ask user to confirm if they want to proceed with Layer 1

Report:
```
设计复杂度分析完成：
- 总节点数: X | 复杂等级: [Simple/Medium/High/Very High]
- 推荐选择: Y 个关键节点 | 确认图片精度: Layer [N]
```

**Very High complexity (150+ nodes): offer Subagent Mode**

For very large files, the most robust approach is to delegate Phase 3–6 to a fresh subagent:
- Main agent has accumulated context from the whole conversation; the subagent starts clean
- Pass only: `session.json` path + target node ID list + imageLayer
- Subagent runs Phase 3–6 in its own context window, unaffected by earlier conversation history

```
检测到超大设计文件（{N} 个节点）。推荐使用子代理模式处理 Phase 3-6：
子代理将在独立的上下文窗口中运行，避免主会话的上下文压力。
是否启用子代理模式？（推荐）/ 继续在当前会话中处理
```

If user approves, spawn a subagent using the prompt template in `references/recovery.md#subagent-mode`.

---

### Phase 3: Extract Key Nodes Sequentially

Select 5-10 key nodes. Process each **one at a time — never concurrent API calls**.

Figma API rate limit is ~60 requests/minute. The sequential pattern handles this automatically — no explicit delays needed. Prioritize frames with meaningful names and `<TEXT>` children over decorative nodes.

For each node (strictly in this order):
1. Report: "正在处理节点 {i}/{total}: {nodeName}..."
2. Call `get_metadata` — wait for result
3. **Immediately write XML to disk using PowerShell** — wait for PowerShell confirmation
4. (If Layer > 0) Call `get_screenshot` — wait for result
5. (If Layer > 0) **Immediately write screenshot to disk using PowerShell** — wait for PowerShell confirmation
6. Update `checkpoint.json`
7. Report: "节点 {nodeName} 处理完成 | XML: ✓ | 图片: ✓/✗"
8. Move to next node

**The disk writes in steps 3 and 5 are mandatory — not optional. Do NOT proceed to the next node until both writes are confirmed.**

### Phase 3.1: Three-Step Sequential Processing

Each node runs three steps: **Step A** (metadata + XML write), **Step B** (conditional screenshot + PNG write), **Step C** (checkpoint update).

Layer 分辨率/token 参考见 Phase 1.1。`scale` 参数：L1=0.333，L2=0.5，L3=1.0（L0 跳过截图）。

**File paths for disk writes:**
- XML: `{output_dir}\figma-metadata\{designName}-node-{nodeId-dashes}.xml`
- PNG: `{output_dir}\figma-screenshots\{designName}-node-{nodeId-dashes}-l{N}.png`
- Checkpoint: `{output_dir}\checkpoint.json`
- nodeId format: colons → dashes (e.g. `112:9331` → `112-9331`)

**Always use PowerShell (`Out-File`, `Invoke-WebRequest`) for disk writes — never the Write tool.**
Reason: Write tool re-serializes the full XML as a parameter, doubling its context footprint. PowerShell writes to disk without expanding the context. After each `Out-File`, explicitly declare "XML 已落盘，不再保留原始 XML 于工作记忆中" so the raw XML can be evicted.

**Screenshot write depends on what `get_screenshot` returns:**
- If it returns a **URL** → use `Invoke-WebRequest` to download directly to `.png`
- If it **renders inline** (no URL in response) → save a `.url.json` stub file instead

For the full PowerShell commands, CORRECT/WRONG pattern, and Token Budget table, see `references/sequential-processing.md`.

**Node summary structure:**
```json
{
  "nodeId": "65:19179",
  "nodeName": "LoginSuccessState",
  "nodeType": "FRAME",
  "structure": { "totalNodes": 15, "textNodes": 6, "frameNodes": 3 },
  "keyText": ["欢迎回来", "继续游戏"],
  "dimensions": "375x812"
}
```

**Node summary must be written into `checkpoint.json` as part of Step C — not held in context only.** Step C already runs for every node; include the summary fields there at zero extra cost. If context compression evicts in-memory summaries between nodes, Phase 6 can recover them with a single `Get-Content checkpoint.json`. Full PowerShell template in `references/sequential-processing.md`.

---

### Phase 4: Aggregate Sequential Results

Aggregation happens incrementally during Phase 3.1 — append each node's summary immediately after it completes. Phase 4 is the final review.

**Critical: do NOT carry forward the full XML** — only the compact summary JSON is needed for document generation. The raw XML was already saved to disk in Phase 3.1; keeping it in working memory across multiple nodes doubles context pressure and risks triggering mid-run compression. After each `Out-File` write, the XML can be evicted — only the summary stays.

From aggregated data, extract:
- **Layer 0**: structural elements, text content, colors/fonts from XML attributes
- **Layer 1-3**: dominant color palette (top 3-5 hex values), layout structure, typography hierarchy, visual elements (icons, shadows, contrast ratios)

**Write `figma-analysis.json` to disk before proceeding to Phase 5.** The aggregated color/typography/layout data is synthesized information that only exists in context — it is not recoverable from the raw XML files alone. Writing it now means Phase 6 can reconstruct the document from disk if context compression occurs mid-generation.

```powershell
$analysis = Get-Content "{output_dir}\checkpoint.json" | ConvertFrom-Json
# append global analysis fields to the object, then save separately
@{ nodes = $analysis.nodes; globalColors = @{primary="..."; text="..."; background="..."}; globalTypography = @{bodyFont="..."; bodySize="..."; headingSize="..."} } | ConvertTo-Json -Depth 5 | Out-File "{output_dir}\figma-analysis.json" -Encoding UTF8
Write-Output "ANALYSIS saved"
```

(Fill in the actual extracted values; the template above shows the structure.)

---

### Phase 5: Verify Saved Files

**File saves happen inside Phase 3.1 per-node — NOT here. Phase 5 is verification only.**

After all nodes are processed, verify that the expected files were actually written to disk. If any are missing, write them now before proceeding to Phase 6.

**Expected file structure:**
```
{output_dir}/
├── figma-metadata/
│   ├── {designName}-node-{id1}.xml    ← one per processed node
│   ├── {designName}-node-{id2}.xml
│   └── ...
├── figma-screenshots/                  ← only if Layer > 0
│   ├── {designName}-node-{id1}-l1.png
│   └── ...
└── checkpoint.json
```

**Verification check:**
1. List files in `figma-metadata/` — should have one `.xml` per processed node
2. If Layer > 0: list files in `figma-screenshots/` — should have one `.png` per processed node
3. If any file is missing: write it now from the XML/screenshot data in context
4. Report: "文件验证完成: {N} 个 XML ✓, {M} 个截图 ✓"

File naming: nodeId colons → dashes (e.g. `65:19179` → `65-19179`).

---

### Phase 6: Generate Documentation (MUST COMPLETE)

**Do NOT stop after XML files are saved.** This step is required.

1. Report: "所有节点处理完成，正在生成设计文档..."
2. **Use PowerShell `Out-File` to write the markdown file** — same reason as XML writes: the Write tool would serialize the full document content as a parameter, adding it to the context window. For documents that can be 3000-8000 words, this matters.
3. Verify file was written: `Test-Path "{output_dir}\figma设计文档.md"`

Use template from `assets/design-doc-template.md`. For component library, design system, and user flow templates, see `references/doc-templates.md`.

**Document structure:**

- **Layer 0** → 8 sections: 概述、功能架构、UI设计、交互设计、状态反馈、异常处理、组件规范、设计规范
- **Layer ≥ 1** → 9 sections: above + **视觉设计系统** (as section 2), which MUST include: color palette with hex values, typography specifications, spacing/layout system

Save as: `{output_dir}/figma设计文档.md`

**Completion report:**

**Completion report（根据 imageLayer 决定输出行数）：**
```
✓ 设计文档生成完成
📄 {path}/figma设计文档.md
📊 处理节点: {N}个 {Layer≥1: (含截图)} | 📝 章节: {M}个 {Layer≥1: (+ 视觉设计系统)}
{Layer≥1: 🎨 色彩: {K}个主色调 | 🔤 排版: {J}套规范 | 💡 精度: Layer {N} +{%}准确度}
💾 元数据: figma-metadata/
```

---

## Troubleshooting

**API Error 429 (Too Many Requests):** You are making concurrent calls — ensure strict sequential processing (one node at a time).

**API Error 400:** Check node IDs use colon format (`123:456`), verify fileKey, ensure you're NOT calling `get_design_context`.

**Missing information:** Check for text annotations in parent/sibling nodes or separate annotation frames. Look for `characters` attribute in TEXT nodes.

**Task interrupted:** See `references/recovery.md` for the full recovery workflow.

---

## Critical Rules Summary

1. **顺序调用**：每次只发起一个 `get_metadata` 请求，等待结果后再继续
2. **即时落盘**：每次 API 调用返回后立即写磁盘（XML 和截图），不得延迟到后面统一保存
3. **Checkpoint**：每个节点写盘确认后更新 `checkpoint.json`
4. **Phase 5 只做验证**：实际文件写入在 Phase 3.1 每节点中完成，Phase 5 仅检查是否遗漏
5. **完成标准**：XML + Markdown 都存在才算完成；中断时检查已有文件后续接，不要从头重做
6. **Phase 0.3 强制**：输出目录确认必须在 Phase 1 之前完成，不可跳过或假设默认值
