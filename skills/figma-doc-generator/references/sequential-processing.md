# Sequential Processing — Detailed Rules

> Read this file when you need the exact three-step pattern for Phase 3.1, the image parameter values, or the Token Budget table.

## Three-Step Sequential Pattern (Phase 3.1)

Process each node with metadata extraction, conditional image download, AND mandatory disk writes — always in strict sequence. Every step must complete and every file must be confirmed written before moving on.

**The golden rule: disk writes use Bash/PowerShell, NOT the Write tool.**

Using the `Write` tool to save XML means the full XML content appears twice in the context window — once from `get_metadata`'s response, once as the `content` parameter to `Write`. Across 8 nodes this doubles the XML footprint and risks triggering context compression mid-run. PowerShell writes the content to disk without re-serializing it into the context.

---

### Step A: Metadata Extraction + Immediate XML Write (ALWAYS)

1. Call `get_metadata` — wait for result before anything else
2. Parse structure, text content, dimensions, hierarchy from XML response
3. **Immediately write the raw XML to disk using PowerShell** — do NOT use the Write tool:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$xml = @'
{paste full XML content here}
'@
$xml | Out-File -FilePath "{output_dir}\figma-metadata\{designName}-node-{nodeId-dashes}.xml" -Encoding UTF8
Write-Output "SAVED: {designName}-node-{nodeId-dashes}.xml"
```

   - Path example: `G:\iWiki\赛事选择\figma-metadata\赛事选择-node-112-9331.xml`
   - nodeId colon → dash: `112:9331` → `112-9331`
   - Ensure the `figma-metadata\` directory exists first (create with `New-Item -ItemType Directory -Force` if needed)

4. **Wait for PowerShell confirmation** (`SAVED: ...` output) — do NOT proceed until confirmed
5. **Declare in your response:** "节点 {name} XML 已落盘，不再保留原始 XML 于工作记忆中"
   - This signals that the XML can be evicted from active context; only the compact summary JSON is needed going forward

---

### Step B: Screenshot Download + Immediate Disk Write (CONDITIONAL)

**Layer 0**: Skip entirely — no screenshots.

**Layer 1-3**: Call `get_screenshot` and wait for the result.

**First, detect what `get_screenshot` actually returns:**

| Return type | How to detect | How to save |
|-------------|---------------|-------------|
| **Image URL** (e.g. `https://figma-alpha-api.s3.us-west-2.amazonaws.com/...`) | Response contains a URL string | Use PowerShell `Invoke-WebRequest` to download directly to disk |
| **Rendered in visual context** (image shown inline, no URL) | No URL in response text | Cannot extract raw bytes; save a `.url` reference file instead |

**If URL is returned — download with PowerShell:**
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$url = "{screenshot_url_from_response}"
$outPath = "{output_dir}\figma-screenshots\{designName}-node-{nodeId-dashes}-l1.png"
New-Item -ItemType Directory -Force -Path (Split-Path $outPath) | Out-Null
Invoke-WebRequest -Uri $url -OutFile $outPath
Write-Output "SAVED: $(Split-Path $outPath -Leaf) ($($(Get-Item $outPath).Length) bytes)"
```

**If rendered inline only — save a reference stub:**
```powershell
# Cannot extract raw image bytes; record that screenshot was captured for this node
$stub = '{ "nodeId": "{nodeId}", "nodeName": "{name}", "note": "screenshot rendered inline, no downloadable URL", "layer": 1 }'
$stub | Out-File -FilePath "{output_dir}\figma-screenshots\{designName}-node-{nodeId-dashes}-l1.url.json" -Encoding UTF8
Write-Output "STUB: {designName}-node-{nodeId-dashes}-l1.url.json (no raw bytes available)"
```

Wait for PowerShell output before continuing. Note in your progress report whether a real PNG or a stub was saved.

**Scale parameters by layer:**

| Layer | `scale` param | Resolution | Tokens/image | Suffix |
|-------|--------------|-----------|-------------|--------|
| 1 | `scale=0.333` | ~853×480 | ~135 | `-l1.png` |
| 2 | `scale=0.5` | ~960×540 | ~250 | `-l2.png` |
| 3 | `scale=1.0` | ~1500×3000 | ~2000 | `-l3.png` |

---

### Step C: Update Checkpoint (MANDATORY after Step A + B)

After both writes are confirmed, update the checkpoint file. **Include the node's compact summary in the checkpoint entry** — this is the required behavior, not optional. The summary is already in context at this point; embedding it here costs nothing and protects against compression loss between nodes.

```powershell
# Read existing checkpoint (or create new), append this node's status + summary, write back
$cpPath = "{output_dir}\checkpoint.json"
if (Test-Path $cpPath) { $cp = Get-Content $cpPath | ConvertFrom-Json } else { $cp = @{ nodes = @() } }
$cp.nodes += [PSCustomObject]@{
  nodeId = "{nodeId}"; nodeName = "{name}"; xmlSaved = $true; screenshotSaved = $true
  summary = @{ dimensions = "{dimensions}"; totalNodes = {n}; keyText = @({keyText}) }
}
$cp | ConvertTo-Json -Depth 5 | Out-File $cpPath -Encoding UTF8
Write-Output "CHECKPOINT updated: {i}/{total} nodes complete"
```

**Why include summary in checkpoint:** The compact summary JSON is the only per-node data carried in context across the full Phase 3.1 loop. Writing it into checkpoint.json costs nothing extra (Step C already runs) and ensures that if context compression evicts the in-memory summaries, they can be recovered with a single `Get-Content checkpoint.json` before Phase 6.

---

## Execution Pattern (CORRECT vs WRONG)

```
✅ CORRECT — three steps with PowerShell disk writes per node:

For each key node:
  Announce: "正在处理节点 {i}/{total}: {nodeName}..."

  Step A:
    → Call get_metadata, WAIT for result
    → Extract structure, text, dimensions into compact summary JSON
    → Run PowerShell Out-File to save XML
    → WAIT for "SAVED: ..." confirmation
    → Declare: "XML 已落盘，不再保留原始 XML 于工作记忆"

  Step B (if Layer > 0):
    → Call get_screenshot with scale param, WAIT for result
    → Detect return type (URL vs inline)
    → Run PowerShell Invoke-WebRequest (URL) or Out-File stub (inline)
    → WAIT for PowerShell confirmation

  Step C:
    → Run PowerShell to update checkpoint.json
    → WAIT for "CHECKPOINT updated" confirmation

  Report: "节点完成: {name} | XML: ✓ | 图片: ✓ PNG / ✓ stub / ✗ | 进度: {i}/{total}"

→ Only then move to the next node

❌ WRONG — these patterns lead to lost files or context bloat:
  → Using the Write tool to save XML (doubles XML in context window)
  → Storing full XML strings in a variable across multiple nodes
  → Calling get_metadata for node 2 before node 1's disk write is confirmed
  → Deferring all saves to Phase 5 ("I'll batch save at the end")
  → Skipping Step C (checkpoint) — makes recovery impossible
```

---

## Why PowerShell Instead of the Write Tool

| | Write Tool | PowerShell Out-File |
|---|---|---|
| XML appears in context | **Twice** (response + content param) | **Once** (response only) |
| Context pressure | High — doubles across 8 nodes | Low — only compact summary kept |
| Compression risk | High mid-run | Minimal |
| Confirmation | Tool result | Explicit `Write-Output` |

After `Out-File` runs, explicitly declare the XML is no longer needed in working memory. This lets the context compression evict the raw XML and keep only the compact summary JSON — which is all that's needed for document generation.

---

## Token Budget Table

| Layer | Metadata/Node | Image/Node | Total/Node | 10 Nodes | % of 3M Budget |
|-------|--------------|-----------|-----------|----------|----------------|
| 0 | ~50 | 0 | ~50 | ~500 | 0.017% |
| 1 | ~50 | ~135 | ~185 | ~1850 | 0.062% |
| 2 | ~50 | ~250 | ~300 | ~3000 | 0.100% |
| 3 | ~50 | ~2000 | ~2050 | ~20500 | 0.683% |

These estimates are for the compact summary JSON kept in context. The raw XML is evicted after each `Out-File` write.

---

## Aggregation During Processing

After each node completes, append to aggregation immediately:
- Compact summary JSON (nodeId, nodeName, dimensions, keyText, screenshotPath)
- Token estimate (running total)
- Progress: "已处理 {i}/{total} 个节点，累计约 {total_tokens} tokens"

Do NOT carry forward the full XML — only the compact summary is needed for document generation.

---

## Session.json Update Templates

### Phase 1 Refresh

```powershell
$s = Get-Content "{output_dir}\session.json" | ConvertFrom-Json
$s.rootNodeId = "{confirmed_nodeId}"; $s.phase = "1"; $s.status = "in_progress"
$s | ConvertTo-Json | Out-File "{output_dir}\session.json" -Encoding UTF8
Write-Output "SESSION refreshed at Phase 1"
```

### Phase 1.1 Refresh (after imageLayer is determined)

```powershell
$s = Get-Content "{output_dir}\session.json" | ConvertFrom-Json
$s.imageLayer = {N}; $s.phase = "1.1"
$s | ConvertTo-Json | Out-File "{output_dir}\session.json" -Encoding UTF8
Write-Output "SESSION imageLayer set to {N}"
```

### Phase 2 Update

```powershell
$s = Get-Content "{output_dir}\session.json" | ConvertFrom-Json
$s.phase = "2"; $s.topLevelNodes = {N_top_level}
$s | ConvertTo-Json | Out-File "{output_dir}\session.json" -Encoding UTF8
Write-Output "SESSION phase=2"
```
