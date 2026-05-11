# Task Recovery & Failure Handling

> Read this file when the task was interrupted (API timeout, context compaction, file write error, or user said "继续"/"恢复").

## Recovery Workflow After Interruption

**Step 1: Check existing data**
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
# Check if XML metadata files exist
Get-ChildItem -Path "{output_dir}\figma-metadata\" -ErrorAction SilentlyContinue

# Check if markdown documentation exists
Test-Path "{output_dir}\figma设计文档.md"

# Check checkpoint.json for last known state
Get-Content "{output_dir}\checkpoint.json" -ErrorAction SilentlyContinue | ConvertFrom-Json

# Check session.json for session parameters
Get-Content "{output_dir}\session.json" -ErrorAction SilentlyContinue | ConvertFrom-Json
```

**Step 2: Determine recovery point**

| Situation | Recovery Action |
|-----------|-----------------|
| No directory exists | Restart from Phase 1 (complete fresh start) |
| Directory exists, no XML files | Restart from Phase 3 (re-extract all nodes) |
| XML files exist but incomplete | Resume from last processed node (check checkpoint.json) |
| XML files complete, no markdown | Skip to Phase 6 (generate docs from saved XML) |
| All files exist | Verify completeness, report to user |

**Step 3: Resume from checkpoint**

**If XML files exist but markdown missing:**
1. Read all saved XML files to extract summaries
2. If Layer >= 1: check if `figma-visual-analysis.json` exists; if missing, regenerate from saved screenshots first
3. Proceed directly to Phase 6 to generate markdown

**If XML files are incomplete:**
1. Read `checkpoint.json` for `nodesProcessed` and `lastCompletedNodeId`
2. Count XML files in `figma-metadata/` to verify checkpoint accuracy
3. Resume Phase 3 from node `nodesProcessed + 1` (skip already-done nodes)
4. After all nodes complete, continue to Phase 5 and Phase 6 normally

## Checkpoint File Format

Written after each node completes in Phase 3.1:
```json
{
  "phase": 3,
  "nodesTotal": 8,
  "nodesProcessed": 3,
  "lastCompletedNodeId": "122:16933",
  "imageLayer": 1,
  "timestamp": "2026-04-03T10:15:30Z"
}
```

## Handling Specific Interruption Scenarios

### Context Compaction (Auto-Compact / Manual /compact)

**Symptoms:** Task state appears reset; user says "继续" or re-invokes the skill after a compact event.

**Recovery (automatic via Phase 0.0):**
1. Phase 0.0 auto-detection runs first — scans for `session.json` within 3 directory levels
2. If found: reads `session.json` + `checkpoint.json` → resumes automatically from correct phase
3. If not found (compact fired before Phase 0.3): ask user for the output directory path and/or Figma URL; restart from Phase 0.3

**Manual recovery (if Phase 0.0 doesn't trigger):**
```powershell
# Find session.json
Get-ChildItem -Path "." -Recurse -Filter "session.json" -Depth 3 | Select-Object FullName
# Read it
Get-Content "{found_path}" | ConvertFrom-Json
```

Then resume from the phase recorded in `session.json`:
- `phase = "0.3"` → re-fetch root metadata (Phase 2), then Phase 3+
- `phase = "2"` → resume Phase 3 from checkpoint
- `phase = "3"` → resume Phase 3 from `nodesProcessed` in checkpoint.json

### API Timeout
**Symptoms:** `get_metadata` call times out or returns error

**Recovery:**
1. Note which node failed
2. Wait 2-3 seconds (implicit by starting new response)
3. Retry the failed node
4. If persistent error, skip that node and continue
5. Document the failure in the final output

### File Write Error
**Symptoms:** XML or markdown file creation fails

**Recovery:**
1. Verify directory exists (create with `mkdir -p`)
2. Verify write permissions
3. Try alternative write method (Write tool or Bash)
4. If all fail, report to user and exit gracefully

### Context Truncation (Legacy)

> Note: This scenario is now largely handled automatically by Phase 0.0 compact resume detection. This section describes the manual fallback if Phase 0.0 doesn't trigger.

**Symptoms:** Response cuts off mid-task

**Recovery:**
1. When user says "继续" or "continue", Phase 0.0 in SKILL.md auto-detects session.json and resumes
2. If Phase 0.0 doesn't trigger: check for session.json manually (see Context Compaction section above)
3. Otherwise: check existing files to determine last completed step, resume from next logical phase
4. Re-report progress to user

## Progressive Reporting Pattern

Report after each phase to show progress even if interrupted:

```
## 执行进度报告

[✓] Phase 1: 解析 URL 和初始化
[✓] Phase 2: 获取根节点结构
[🔄] Phase 3: 提取关键节点 (3/8 完成)
    - [✓] 节点 73:6932 (页签)
    - [✓] 节点 99:7725 (初始状态)
    - [✓] 节点 122:16933 (进攻策略)
    - [ ] 节点 116:5049 (下拉列表切换)
    - [ ] ...
[ ] Phase 4: 聚合结果
[ ] Phase 5: 保存 XML 元数据
[ ] Phase 6: 生成设计文档
```

## Safe File Writing Patterns

**When saving XML files:**
- Save one at a time, never batch
- Use Write tool for reliability
- Confirm each save before moving to next

**When saving markdown:**
- Write the complete document in one operation
- Use Write tool (not Bash heredoc) for proper file handling
- Verify the file exists after writing

## User Prompt for Recovery

When user says "继续" or "恢复":
1. Acknowledge the interruption
2. Check for existing files
3. Report which phase was in progress
4. Resume from appropriate point

**Example response pattern:**
```
检测到之前的任务中断。正在检查现有文件...

发现以下文件：
- 存在: figma-metadata/目录
- 已保存: 3/15 个 XML 节点
- 缺失: figma设计文档.md

正在恢复任务...
从 Phase 3 (节点 4/15) 继续提取节点...
```

## Final Verification Before Declaring Success

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
# Check directory exists
if (Test-Path "{output_dir}\") { Write-Output "✓ 目录存在" } else { Write-Output "✗ 目录不存在" }

# Check markdown exists and is not empty
if ((Test-Path "{output_dir}\figma设计文档.md") -and (Get-Item "{output_dir}\figma设计文档.md").Length -gt 0) {
  Write-Output "✓ 文档存在"
} else { Write-Output "✗ 文档缺失或为空" }

# Count XML files
$count = (Get-ChildItem "{output_dir}\figma-metadata\*.xml" -ErrorAction SilentlyContinue).Count
Write-Output "✓ 已保存 $count 个 XML 文件"
```

Only report success if:
- Markdown file exists and has content
- All planned XML files are saved (or user was informed of failures)

---

## Subagent Mode Prompt Template

```
Read session.json at {outputDir}/session.json.
Process these Figma nodes using the figma-doc-generator skill, starting at Phase 3:
  fileKey: {fileKey}, nodes: [{nodeId1}, {nodeId2}, ...], imageLayer: {N}
Output directory: {outputDir}/
Continue through Phase 6 (generate the markdown doc). Report completion.
```
