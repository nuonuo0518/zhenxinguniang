# Text Migration to Local Sheet

Migrate module-specific text from global ID2StringMapTable to module's Local sheet with proper localization key naming.

## Overview

Module-specific error messages, UI texts, and other localized strings should be stored in the module's own Local sheet instead of the global ID2StringMapTable. This improves:
- **Modularity**: Each module manages its own localization resources
- **Clarity**: Easier to find and maintain module-specific texts
- **Naming**: Follows `Loc_{Module}_{Sheet}_{Field}_{Id}` or `Loc_{Module}_{Sheet}_{Id}` convention

---

## Standard Workflow: CLI-First

> **Always start with the CLI command. Only fall back to manual scripting if the CLI fails.**

### Step 1: Check proto field type

```bash
grep "FieldName" converter/resource/desc/client/res_client_struct.proto
```

| Result | Action |
|--------|--------|
| `string FieldName` | No proto change needed — proceed |
| `uint32 FieldName` | Note it: must update proto to `string` after migration |
| Not found | Field name mismatch — verify in Excel Row 1 |

### Step 2: Preview (dry-run)

```bash
# Always use absolute path to avoid Git Bash encoding issues on Windows
python table_tool/table_tool.py migrate-text G:/Git/.../excel/YourModule.xlsx --field FieldName --dry-run
```

Dry-run output shows:
- Number of records to process
- Number of unique text entries to migrate

**⚠️ If the command produces NO output and exits silently (exit code 0):**
This is a known failure mode — the CLI returned early without processing. Do NOT assume migration succeeded.
Diagnose with:
```bash
# 1. Check for residual Excel processes that may block file access
tasklist | findstr /i EXCEL

# 2. Check for temp lock files
dir excel | findstr "~$"

# 3. Try re-running — if still silent, fall back to manual workflow below
```
If silent exit persists after clearing Excel processes, proceed to **Fallback: Manual Migration Workflow**.

### Step 3: Run the migration

```bash
python table_tool/table_tool.py migrate-text G:/Git/.../excel/YourModule.xlsx --field FieldName
```

The CLI automatically handles:
- Phase 0: Proto type check (warns if not `string`)
- Phase 1: Collect referenced IDs from source sheet
- Phase 2: Extract text from ID2StringMapTable
- Phase 3: Create or append to Local sheet with Loc keys, then **validate key uniqueness** (raises `ValueError` on duplicates, file NOT saved)
- Phase 4: Update source field values to Loc keys
- Phase 5: Delete migrated rows from ID2StringMapTable
- Phase 6: Auto-update `convert_list.xml` (adds Local DataSource to `Client_Key2StringMapTable`, skips if already present)
- Cleanup: Remove temp JSON file

**Options:**
- `--sheet SheetName` — Source sheet (default: `Main`)
- `--basic` — Use `Loc_Module_Id` format instead of `Loc_Module_Field_Id` (default: enhanced)
- `--export-target client|server|both` — Export target for Local sheet (default: `client`)

### Step 4: Verify XML config was updated (should be automatic)

```bash
grep -n "YourModule.xlsx|Local" converter/convert_list.xml
```

**Two things to check:**

1. **Entry exists** — If missing (Phase 6 failed), add manually to `Client_Key2StringMapTable`
2. **Entry is on its own line** — If the output line also contains `ProtoName` or `OutputFile`, the CLI wrote without a trailing newline and corrupted the file. Fix by splitting the line:

```xml
<!-- Corrupted (wrong): -->
...YourModule.xlsx|Local|5,1</scheme><scheme name="ProtoName" ...>Key2StringMapTable</scheme>

<!-- Correct: -->
...YourModule.xlsx|Local|5,1</scheme>
      <scheme name="ProtoName" ...>Key2StringMapTable</scheme>
```

> **Note:** If the Local DataSource entry already exists for this module from a previous field migration, Phase 6 will skip the file entirely — `convert_list.xml` should not be modified at all. If it was modified anyway, check for the line-concatenation bug above.

If **missing** (Phase 6 failed), add manually to `Client_Key2StringMapTable`:

```xml
<scheme name="DataSource" desc="数据源(文件名|表名|数据起始行号,数据起始列号)">../../excel/YourModule.xlsx|Local|5,1</scheme>
```

Do **not** create a separate `<item>` — it merges into `Key2StringMapTable.bytes`.

For server export (`--export-target server` or `both`), also check `convert_list_server.xml`.

### Step 5: Update proto if needed

Only when Step 1 showed the field was `uint32`/`int32`:

Edit `converter/resource/desc/client/res_client_struct.proto`:
```protobuf
// Before:
uint32 FieldName = N;
// After:
string FieldName = N;
```

### Verification checklist

- [ ] Local sheet exists with 4-row header and correct Row 4 export targets
- [ ] **All Loc keys in Local sheet are unique** (automatically validated by CLI — `ValueError` raised if duplicates found)
- [ ] All data rows in source sheet now reference `Loc_*` keys (not numeric IDs)
- [ ] ID2StringMapTable rows deleted
- [ ] XML config contains `YourModule.xlsx|Local|5,1`
- [ ] Proto type is `string` (if it was numeric before)
- [ ] No Excel processes remain: `tasklist | findstr EXCEL` (empty)
- [ ] No temp files remain: `dir excel | findstr "~$"` (empty)

---

## CRITICAL: Excel Process Management - ALWAYS Use try-finally

⚠️ **MANDATORY for ALL Excel Operations in This Workflow**

When using xlwings for any Excel operation in text migration, the Excel process MUST be properly closed using try-finally pattern. Without this:
- Excel processes can remain in memory even after `wb.save()` and `wb.close()`
- File locks persist (temporary `~$*.xlsx` files)
- Data may not persist despite save() appearing to succeed
- Subsequent operations fail with "Permission denied" errors

**This pattern is MANDATORY for:**
- ✅ Inline Python code in terminal/bash commands
- ✅ Standalone Python scripts
- ✅ All code examples in this documentation
- ✅ Migration automation workflows

### MANDATORY Pattern

```python
import xlwings as xw

app = xw.App(visible=False)
app.display_alerts = False      # Suppress Excel dialogs
app.screen_updating = False     # Disable screen updates for speed

try:
    wb = app.books.open('excel/YourFile.xlsx')
    sheet = wb.sheets['YourSheet']

    # Perform operations
    sheet.range('A5').value = new_value

    wb.save()
    wb.close()
finally:
    app.quit()  # CRITICAL: Ensures Excel process exits
```

### Common Mistakes to Avoid

```python
# ❌ WRONG - No try-finally
app = xw.App(visible=False)
wb = app.books.open('file.xlsx')
wb.save()
wb.close()
app.quit()  # May not run if exception occurs!

# ❌ WRONG - Only catch, no finally
try:
    app = xw.App(visible=False)
    wb = app.books.open('file.xlsx')
    wb.save()
except Exception as e:
    print(f'Error: {e}')
app.quit()  # Won't run if exception occurs before this point
```

### Debugging Excel Process Issues

```bash
# Check if Excel is still running
tasklist | findstr /i "EXCEL"

# Force kill all Excel processes (use with caution)
taskkill /F /IM EXCEL.EXE

# Check for temp lock files (indicates file is open)
dir excel | findstr "~$"
```

### Verification After Operations

After any Excel operation:
1. Check Excel processes: `tasklist | findstr EXCEL` (should be empty)
2. Check temp files: `dir excel | findstr "~$"` (should be empty)
3. Open file with openpyxl to verify data persisted
4. Re-open with xlwings to confirm changes are still present

**NOTE:** All Excel code examples in this document follow this pattern. Use them as templates for your operations.

---

## Text Source Location

**Default source for text migration:**
- **File**: `excel/ID2StringMapTable.xlsx`
- **Sheet**: `Main`
- **Structure**: `{Id, SystemLanguageCn, SystemLanguageEn}`

This is the standard location for global localization texts in NBA2kOL3 project.

## Involved Files

| File | Path | Purpose |
|------|------|---------|
| Source Excel | `excel/{Module}.xlsx` | Module table referencing text IDs |
| Target Local Sheet | `excel/{Module}.xlsx` / Local | Destination for migrated texts |
| **Text Source** | **`excel/ID2StringMapTable.xlsx` / Main** | **Global text table to migrate from (standard)** |
| Proto Definition | `converter/resource/desc/client/res_client_struct.proto` | Field type definition update |
| Client Config | `converter/convert_list.xml` | Key2StringMapTable configuration |

## Architecture: Key2StringMapTable Integration

**IMPORTANT - Local Sheet Configuration:**

All Local sheets must be **merged into the `Key2StringMapTable` configuration** in `convert_list.xml`:

```xml
<item name="Client_Key2StringMapTable" cat="Key2String" class="client ">
  <indexer type="string">Id</indexer>
  <scheme name="DataSource">../../excel/ID2StringMapTable.xlsx|Main|5,1</scheme>
  <scheme name="DataSource">../../excel/Z账号创建_UserNameRandom.xlsx|Local|5,1</scheme>
  <scheme name="DataSource">../../excel/{YourModule}.xlsx|Local|5,1</scheme>  <!-- Add here -->
  <!-- More DataSources -->
  <scheme name="ProtoName">Key2StringMapTable</scheme>
  <scheme name="OutputFile">Key2StringMapTable.bytes</scheme>
</item>
```

**Do NOT create separate item configurations for Local sheets** - they all merge into `Key2StringMapTable.bytes`.

## Export Target Determination

### Two Scenarios

**1. Converting Existing Tables (proto exists):**
- ✅ Auto-detect export targets from proto definitions
- Efficient and accurate

**2. Creating New Local Sheet (no proto yet):**
- ⚠️ **Must ask user** via `AskUserQuestion` tool
- Example: "Should the localization data in {Module} Local sheet be exported to Client only, Server only, or Both?"
- Typical answer for localization: "Client only"
- Set Row 4 to `[PrimaryKey, Client, Client]` for client-only export

## Naming Convention

### Localization Key Format

**Basic Format** (when simple ID is clear enough):
```
Loc_{ModuleName}_{SheetName}_{RecordId}
```

**Examples:**
- `Loc_CsRetError_Main_0` - CsRetError module, Main sheet, ID 0
- `Loc_ConnectorError_Main_201` - ConnectorError module, Main sheet, error code 201

**Enhanced Format** (default, always use to prevent cross-sheet collisions):
```
Loc_{ModuleName}_{SheetName}_{ColumnHeader}_{RecordId}
```

**Examples:**
- `Loc_PlayerAbility_Main_Name_1` - PlayerAbility module, Main sheet, Name column, ID 1
- `Loc_PlayerAbility_Main_Description_1` - PlayerAbility module, Main sheet, Description column, ID 1
- `Loc_TacticsSettings_GameTacticsOption_TacticsTextual_5` - TacticsSettings module, GameTacticsOption sheet, TacticsTextual column, ID 5

**Why SheetName is mandatory (never omit):**
- Same file can have multiple sheets with the same column name → key collision
- Future sheets may be added → design must be forward-compatible
- All four parts are required for guaranteed uniqueness

**Naming Rules:**
- Prefix: Always `Loc_` (localization)
- ModuleName: ASCII-only stem of the Excel filename (strip Chinese prefixes like "S赛事模式_")
- SheetName: Exact sheet name from `--sheet` parameter (default: `Main`)
- ColumnHeader: Exact column header from `--field` parameter (Enhanced format only)
- RecordId: Primary key value of the row
- Separator: Underscore `_`

**When to Ask User:**
If naming format is unclear, use `AskUserQuestion` to ask:
- "Should we use the basic format (Loc_{Module}_{Sheet}_{Id}) or enhanced format (Loc_{Module}_{Sheet}_{Field}_{Id})?"
- Provide context: "The enhanced format includes the column name and is recommended for clarity."

## Fallback: Manual Migration Workflow

> **Use this section only if `migrate-text` CLI command fails or hangs.**
> Under normal circumstances, the CLI handles Phase 0–5 automatically.
> The most common cause of CLI failure is Excel process residue — check with `tasklist | findstr EXCEL` and kill any processes before retrying.

### 写操作方案选择（手动回退时）

手动回退时，写操作按以下优先级选择：

1. **`XlsxWriter`（minimax-xlsx）** — 无 Excel 进程，支持：新建 sheet、写入行、更新单元格、删除行
2. **`xlwings`** — 仅当 XlsxWriter 不支持该操作时（如 autofit、数据验证），且完成后需报告"未支持场景"

### Phase 0: Pre-Migration Verification

#### 0.1 Check Proto Field Type

**CRITICAL:** Before migrating text, verify the current proto field type to determine if proto definition needs updating.

```bash
# Search for the field definition in client proto
grep "SecondTabTextual" converter/resource/desc/client/res_client_struct.proto
```

**Check result interpretation:**

| Proto Definition | Action Required |
|------------------|-----------------|
| `string SecondTabTextual = N;` | ✅ No proto change needed - proceed with migration only |
| `uint32 SecondTabTextual = N;` | ⚠️ Must update proto type after migration (see Phase 3.2) |
| `int32 SecondTabTextual = N;` | ⚠️ Must update proto type after migration |
| Field not found | ❌ Field name mismatch - verify field name in Excel sheet |

**Why this check matters:**

1. **If already `string`:** Migration can proceed without proto changes. The field already supports Loc keys.

2. **If numeric type (`uint32`, `int32`, etc.):** You must update the proto definition after migration, or:
   - The conversion will fail with type mismatch errors
   - Binary output may not compile correctly
   - Game code may crash when reading the field

3. **If field not found:** Double-check the actual field name in Excel Row 1 - proto field names must match exactly.

**Example:**

```bash
$ grep "SecondTabTextual" converter/resource/desc/client/res_client_struct.proto
    string SecondTabTextual = 4;

# Output shows "string" - safe to proceed with migration, no proto update needed

$ grep "DescriptionId" converter/resource/desc/client/res_client_struct.proto
    uint32 DescriptionId = 3;

# Output shows "uint32" - must remember to update proto to "string" after migration
```

Add this verification to your migration checklist before proceeding to Phase 1.

---

### Phase 1: Data Analysis

#### 1.1 Identify Table Format

Check `convert_list.xml` for the DataSource configuration:

```xml
<!-- Legacy format (2-row header) -->
<scheme name="DataSource">../../excel/ErrorCodeFeedback.xlsx|CsRetError|3,1</scheme>

<!-- NBA2kOL3 format (4-row header) -->
<scheme name="DataSource">../../excel/ErrorCodeFeedback.xlsx|CsRetError|5,1</scheme>
```

**Format determination:**
- `|3,1` → Old format, data starts at row 3 (2-row header)
- `|5,1` → New format, data starts at row 5 (4-row header)

#### 1.2 Collect Referenced IDs

Use openpyxl for fast read-only analysis:

```python
from openpyxl import load_workbook

# Read source table
wb_src = load_workbook('excel/ErrorCodeFeedback.xlsx', data_only=True)
sheet_src = wb_src['CsRetError']

# Determine data start row from XML config
data_start_row = 3  # or 5 for new format

# Collect all referenced text IDs
desc_ids = []
for row in range(data_start_row, sheet_src.max_row + 1):
    id_val = sheet_src.cell(row, 1).value  # Module ID
    if not id_val:
        break
    desc_id = sheet_src.cell(row, 4).value  # DescriptionId (old numeric ID)
    if desc_id:
        desc_ids.append((int(id_val), int(desc_id)))

print(f'Found {len(desc_ids)} records to migrate')
```

#### 1.3 Extract Text from ID2StringMapTable

```python
wb_map = load_workbook('excel/ID2StringMapTable.xlsx', data_only=True)
sheet_main = wb_map['Main']

target_ids = set([d[1] for d in desc_ids])

id_to_text = {}  # {desc_id: (cn_text, en_text)}
id_to_row = {}   # {desc_id: row_number} for cleanup

for row in range(5, sheet_main.max_row + 1):
    id_val = sheet_main.cell(row, 1).value
    if not id_val:
        continue
    try:
        id_int = int(id_val)
        if id_int in target_ids:
            cn = sheet_main.cell(row, 2).value or ''
            en = sheet_main.cell(row, 3).value or ''
            id_to_text[id_int] = (cn, en)
            id_to_row[id_int] = row
    except:
        pass

print(f'Matched {len(id_to_text)} text entries')
```

#### 1.4 Save Intermediate Data

```python
import json

with open('temp_migration_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'module_data': desc_ids,
        'id_to_text': {str(k): v for k, v in id_to_text.items()},
        'id_to_row': {str(k): v for k, v in id_to_row.items()}
    }, f, ensure_ascii=False, indent=2)
```

### Phase 2: Create or Verify Local Sheet

> **优先使用 XlsxWriter（无进程残留）。** 仅当遇到 XlsxWriter 不支持的操作（如 autofit、数据验证）时，才降级使用 xlwings，并在任务结束时报告未支持场景。

#### 2.1 Check if Local Sheet Exists

```python
import tempfile
from table_tool.table_toolkit.core.xlsx_writer import XlsxWriter

# 用 XlsxWriter 检查 sheet 是否存在（无需启动 Excel）
with tempfile.TemporaryDirectory() as tmp:
    w = XlsxWriter('excel/{Module}.xlsx', work_dir=tmp)
    w.unpack()
    sheet_names = w.get_sheet_names()
    local_exists = 'Local' in sheet_names
    print('Local sheet exists:', local_exists)
```

#### 2.2 Create Local Sheet (if needed) — XlsxWriter 版（优先）

**IMPORTANT: Ask user for export target first**

如果 Local sheet 不存在且没有 proto 定义，先通过 `AskUserQuestion` 确认导出目标，再创建：

```python
from table_tool.table_toolkit.core.xlsx_writer import XlsxWriter

with XlsxWriter('excel/{Module}.xlsx') as writer:
    # 创建 Local sheet（同步更新 workbook.xml、rels、Content_Types）
    writer.add_sheet('Local')

    # 追加 sharedStrings
    header_strings = ['Id', 'SystemLanguageCn', 'SystemLanguageEn',
                      'string', '唯一序号', 'PrimaryKey', 'Client']
    idx = writer.append_shared_strings(header_strings)

    # Row 1: 字段名
    writer.insert_row_content('Local', 1, [
        ('A', 's', idx['Id']),
        ('B', 's', idx['SystemLanguageCn']),
        ('C', 's', idx['SystemLanguageEn']),
    ])
    # Row 2: 类型
    writer.insert_row_content('Local', 2, [
        ('A', 's', idx['string']),
        ('B', 's', idx['string']),
        ('C', 's', idx['string']),
    ])
    # Row 3: 注释（A列写唯一序号，B/C列省略空单元格）
    writer.insert_row_content('Local', 3, [
        ('A', 's', idx['唯一序号']),
    ])
    # Row 4: 导出目标（client-only 示例）
    writer.insert_row_content('Local', 4, [
        ('A', 's', idx['PrimaryKey']),
        ('B', 's', idx['Client']),
        ('C', 's', idx['Client']),
    ])
    # pack 在 __exit__ 自动执行

print('Local sheet created (no Excel process)')
```

#### 2.3 Write Localization Data — XlsxWriter 版（优先）

```python
from table_tool.table_toolkit.core.xlsx_writer import XlsxWriter
import json

with open('temp_migration_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
module_data = data['module_data']
id_to_text = {int(k): v for k, v in data['id_to_text'].items()}

# 收集所有字符串，批量追加 sharedStrings
all_strings = set()
for module_id, desc_id in module_data:
    all_strings.add(f'Loc_{module_name}_{module_id}')
    if desc_id in id_to_text:
        cn, en = id_to_text[desc_id]
        if cn: all_strings.add(cn)
        if en: all_strings.add(en)

with XlsxWriter('excel/{Module}.xlsx') as writer:
    idx = writer.append_shared_strings(list(all_strings))
    append_row = writer.get_last_data_row('Local') + 1

    rows_data = []
    for module_id, desc_id in module_data:
        loc_key = f'Loc_{module_name}_{module_id}'
        cn, en = id_to_text.get(desc_id, ('', ''))
        cells = [('A', 's', idx[loc_key])]
        if cn: cells.append(('B', 's', idx[cn]))
        if en: cells.append(('C', 's', idx[en]))
        rows_data.append(cells)

    writer.write_rows('Local', append_row, rows_data)

print(f'Wrote {len(rows_data)} entries to Local sheet (no Excel process)')
```

> **xlwings 兜底（仅当 XlsxWriter 不支持时）：** 若需要 autofit 列宽等 XlsxWriter 未实现的操作，才回退到下方 xlwings 写法，并在任务结束时报告未支持场景。

<details>
<summary>▶ xlwings 兜底写法（点击展开）</summary>

```python
import xlwings as xw

app = xw.App(visible=False)
app.display_alerts = False
app.screen_updating = False

try:
    wb = xw.Book('excel/{Module}.xlsx')
    local_sheet = wb.sheets.add(name='Local', after=wb.sheets[-1])

    local_sheet.range('A1:C1').value = ['Id', 'SystemLanguageCn', 'SystemLanguageEn']
    local_sheet.range('A2:C2').value = ['string', 'string', 'string']
    local_sheet.range('A3:C3').value = ['唯一序号', '通用系统-文本内容', '英语系统-文本内容']
    local_sheet.range('A4:C4').value = ['PrimaryKey', 'Client', 'Client']

    if loc_data:
        local_sheet.range(f'A5:C{5+len(loc_data)-1}').value = loc_data

    wb.save()
    wb.close()
finally:
    app.quit()
```

</details>

### Phase 3: Update Source Table References

#### 3.1 Update Field Type and Values

⚠️ **CRITICAL: 单列写入必须用 1D list + transpose=True，禁止用 2D list + 列范围**

已发生事故（2026-03-11）：使用 2D list `[[loc_key], ...]` 配合列范围 `D5:D16` 导致值横向溢出，整行数据被污染。

```python
# 迁移前保存快照（出错时可快速回滚）
# backup = sheet_src.range(f'D5:F{last_row}').value  # 目标列 + 相邻2列

app = xw.App(visible=False)
app.display_alerts = False
app.screen_updating = False

try:
    wb = xw.Book('excel/ErrorCodeFeedback.xlsx')
    sheet_src = wb.sheets['CsRetError']

    # 1. Update field type in header row 2
    sheet_src.range('D2').value = 'string'  # DescriptionId column

    # 2. Prepare new Loc keys as 1D list (NOT 2D list!)
    updates = []
    for module_id, desc_id in module_data:
        loc_key = f'Loc_CsRetError_{module_id}'
        updates.append(loc_key)  # ✅ 1D list element, NOT [loc_key]

    # 3. Batch write new Loc keys using transpose=True (纵向填充)
    data_start_row = 3  # or 5 for new format
    if updates:
        # ✅ 正确: 1D list + options(transpose=True) → 纵向填充
        sheet_src.range(f'D{data_start_row}').options(transpose=True).value = updates
        # ❌ 错误: sheet_src.range(f'D{data_start_row}:D{data_start_row+len(updates)-1}').value = updates
        #    （1D list 在列范围上仍会横向溢出！）

    # 4. 验证相邻列未被污染
    for i in range(len(updates)):
        row = data_start_row + i
        adj = sheet_src.range(row, 5).value  # E 列（D列的下一列）
        if isinstance(adj, str) and adj.startswith('Loc_'):
            raise ValueError(f'Data pollution detected at row {row}, E col = {adj}')

    print(f'Updated {len(updates)} DescriptionId values')

    wb.save()
    wb.close()
finally:
    app.quit()
```

#### 3.2 Update Proto Definition

Modify the proto file to change field type from numeric to string:

```protobuf
// Before:
message CsRetError {
    uint32 Id = 1;
    ErrorCodeFeedbackType FeedbackType = 2;
    uint32 DescriptionId = 3;  // ← Change this
    bool ShowErrorCode = 4;
}

// After:
message CsRetError {
    uint32 Id = 1;
    ErrorCodeFeedbackType FeedbackType = 2;
    string DescriptionId = 3;  // ← Now string
    bool ShowErrorCode = 4;
}
```

Use Edit tool to modify `converter/resource/desc/client/res_client_struct.proto`.

### Phase 4: Cleanup Source Data

> **优先使用 XlsxWriter 的 `delete_rows()`** — 自动更新行号、公式引用（含 `<f ref=>`），无 Excel 进程。

#### 4.1 XlsxWriter 行删除（优先）

```python
from table_tool.table_toolkit.core.xlsx_writer import XlsxWriter
import json

with open('temp_migration_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

id_to_row = {int(k): v for k, v in data['id_to_row'].items()}
row_nums_to_delete = set(id_to_row.values())

with XlsxWriter('excel/ID2StringMapTable.xlsx') as writer:
    deleted = writer.delete_rows('Main', row_nums_to_delete)

print(f'Cleanup complete: {deleted} rows deleted (no Excel process)')
```

**`delete_rows` 自动处理：**
- `<row r="N">` 行号重排
- `<c r="XN">` 单元格地址重排
- `<f>...</f>` 公式内行号偏移
- `<f t="shared" ref="B5:B100">` 共享公式范围属性重排
- `<dimension ref="...">` 更新

> **xlwings 兜底（仅当 delete_rows 无法覆盖时）：** 例如需要保留特殊 COM 行为。完成后报告未支持场景。

<details>
<summary>▶ xlwings 兜底写法（点击展开）</summary>

```python
import xlwings as xw

app = xw.App(visible=False)
app.display_alerts = False
app.screen_updating = False

try:
    wb = xw.Book('excel/ID2StringMapTable.xlsx')
    main_sheet = wb.sheets['Main']

    rows_to_delete = sorted(id_to_row.values(), reverse=True)
    for i, row_num in enumerate(rows_to_delete, 1):
        main_sheet.api.Rows(row_num).Delete()
        if i % 10 == 0:
            print(f'Deleted {i}/{len(rows_to_delete)} rows')

    wb.save()
    wb.close()
finally:
    app.quit()
```

</details>

### Phase 5: Update Configuration

#### 5.1 Add Local Sheet to Key2StringMapTable

**IMPORTANT:** Add the new Local sheet to the `Key2StringMapTable` configuration based on export target.

**For Client-only export (typical for UI texts):**

Edit `converter/convert_list.xml` to find the `Client_Key2StringMapTable` item (around line 68-78):

```xml
<item name="Client_Key2StringMapTable" cat="Key2String" class="client ">
  <indexer type="string" desc="索引键要求值全表唯一(ProtoMessage的成员名)">Id</indexer>
  <scheme name="DataSource" desc="数据源(文件名|表名|数据起始行号,数据起始列号)">../../excel/ID2StringMapTable.xlsx|Main|5,1</scheme>
  <scheme name="DataSource" desc="数据源(文件名|表名|数据起始行号,数据起始列号)">../../excel/Z账号创建_UserNameRandom.xlsx|Local|5,1</scheme>
  <!-- Add your module's Local sheet here -->
  <scheme name="DataSource" desc="数据源(文件名|表名|数据起始行号,数据起始列号)">../../excel/{YourModule}.xlsx|Local|5,1</scheme>
  <scheme name="DataSource" desc="数据源(文件名|表名|数据起始行号,数据起始列号)">../../excel/ID2StringMapTable.xlsx|Local|5,1</scheme>
  <scheme name="ProtoName" desc="协议名">Key2StringMapTable</scheme>
  <scheme name="OutputFile" desc="输出文件名">Key2StringMapTable.bytes</scheme>
</item>
```

**For Server-only or Both client+server export:**

Also edit `converter/convert_list_server.xml` to find the `Server_Key2StringMapTable` item:

```xml
<item name="Server_Key2StringMapTable" cat="Key2String" class="server">
  <indexer type="string" desc="索引键要求值全表唯一(ProtoMessage的成员名)">Id</indexer>
  <scheme name="DataSource" desc="数据源(文件名|表名|数据起始行号,数据起始列号)">../../excel/ID2StringMapTable.xlsx|Main|5,1</scheme>
  <!-- Add your module's Local sheet here if exported to server -->
  <scheme name="DataSource" desc="数据源(文件名|表名|数据起始行号,数据起始列号)">../../excel/{YourModule}.xlsx|Local|5,1</scheme>
  <scheme name="DataSource" desc="数据源(文件名|表名|数据起始行号,数据起始列号)">../../excel/ID2StringMapTable.xlsx|Local|5,1</scheme>
  <scheme name="ProtoName" desc="协议名">NBA3.Game.Resource.server.Key2StringMapTable</scheme>
  <scheme name="OutputFile" desc="输出文件名">server/Key2StringMapTable.bin</scheme>
</item>
```

**Configuration Summary:**

| Export Target | Client XML (`convert_list.xml`) | Server XML (`convert_list_server.xml`) |
|---------------|----------------------------------|----------------------------------------|
| Client only (typical) | ✅ Add to `Client_Key2StringMapTable` | ❌ Do NOT add |
| Server only | ❌ Do NOT add | ✅ Add to `Server_Key2StringMapTable` |
| Both | ✅ Add to `Client_Key2StringMapTable` | ✅ Add to `Server_Key2StringMapTable` |

Use the Edit tool to insert the new DataSource line(s).

**Do NOT:**
- Create a separate `<item>` configuration for Local sheet
- Add a new proto message definition (uses existing `Key2StringMapTable`)

#### 5.2 Verify Configuration

```python
import xml.etree.ElementTree as ET

# Check client XML
tree_client = ET.parse('converter/convert_list.xml')
root_client = tree_client.getroot()

print('=== Client Configuration ===')
for item in root_client.findall('.//item[@name="Client_Key2StringMapTable"]'):
    datasources = item.findall('.//scheme[@name="DataSource"]')
    print(f'Client_Key2StringMapTable has {len(datasources)} DataSources')
    for ds in datasources:
        if '{YourModule}.xlsx|Local' in ds.text:
            print(f'  ✓ Found: {ds.text}')
            break
    else:
        print(f'  ℹ Not found: {YourModule} Local sheet in client config')

# Check server XML (if needed for server export)
print('\n=== Server Configuration ===')
tree_server = ET.parse('converter/convert_list_server.xml')
root_server = tree_server.getroot()

for item in root_server.findall('.//item[@name="Server_Key2StringMapTable"]'):
    datasources = item.findall('.//scheme[@name="DataSource"]')
    print(f'Server_Key2StringMapTable has {len(datasources)} DataSources')
    for ds in datasources:
        if '{YourModule}.xlsx|Local' in ds.text:
            print(f'  ✓ Found: {ds.text}')
            break
    else:
        print(f'  ℹ Not found: {YourModule} Local sheet in server config (expected if client-only)')

print('\n✓ Configuration verification complete')
```

### Phase 6: Verification

#### 5.1 Verify Migration Completeness

```python
app = xw.App(visible=False)

try:
    # 1. Check Local sheet
    wb_target = xw.Book('excel/ErrorCodeFeedback.xlsx')
    sheet_local = wb_target.sheets['Local']
    sheet_src = wb_target.sheets['CsRetError']

    # Count Local sheet entries
    last_row = 5
    while sheet_local.range(last_row, 1).value:
        last_row += 1
    print(f'Local sheet entries: {last_row - 5}')

    # Check field type
    dtype = sheet_src.range('D2').value
    print(f'DescriptionId type: {dtype}')

    # Sample data check
    print('\nSample data:')
    for row in range(data_start_row, data_start_row + 3):
        id_val = sheet_src.range(row, 1).value
        desc = sheet_src.range(row, 4).value
        print(f'  Id={id_val}, DescriptionId={desc}')

    wb_target.close()

    # 2. Check cleanup
    wb_source = xw.Book('excel/ID2StringMapTable.xlsx')
    sheet_main = wb_source.sheets['Main']

    # Look for remaining IDs in range (e.g., 817000000-818000000)
    found = []
    for row in range(5, min(10000, sheet_main.used_range.last_cell.row + 1)):
        id_val = sheet_main.range(row, 1).value
        if id_val:
            try:
                if 817000000 <= int(id_val) < 818000000:
                    found.append(int(id_val))
            except:
                pass

    if found:
        print(f'\n⚠️ Warning: {len(found)} entries still remain')
    else:
        print('\n✓ All entries cleaned up')

    wb_source.close()
finally:
    app.quit()
```

#### 5.2 Cleanup Temporary Files

```python
# 方法 1: 使用 table_toolkit 工具函数（推荐）
from doc.table_toolkit.utils import rm_f, clean_temps

# 删除指定文件
rm_f('temp_migration_data.json')

# 或批量清理所有 temp_*.json 文件
count = clean_temps('temp_*.json')
print(f'清理了 {count} 个临时文件')

# 方法 2: 使用 Python pathlib（跨平台）
from pathlib import Path

# 删除单个文件（忽略不存在的情况）
Path('temp_migration_data.json').unlink(missing_ok=True)

# 删除多个文件
for file in ['temp_migration_data.json', 'temp_quality_des_data.json']:
    Path(file).unlink(missing_ok=True)
```

**注意：** 表格中的所有临时文件清理操作都应使用以上 Python 方法，避免使用平台特定的 shell 命令（如 `rm` 或 `del`），以确保跨平台兼容性。

## Naming Convention

### Localization Key Format

```
Loc_{ModuleName}_{SheetName}_{ColumnHeader}_{RecordId}   (Enhanced, default)
Loc_{ModuleName}_{SheetName}_{RecordId}                  (Basic)
```

**Examples:**
- `Loc_CsRetError_Main_0` - CsRetError module, Main sheet, ID 0
- `Loc_CsRetError_Main_1101` - CsRetError module, Main sheet, ID 1101
- `Loc_ConnectorError_Main_201` - ConnectorError module, Main sheet, error code 201

**Naming Rules:**
- Prefix: Always `Loc_` (localization)
- ModuleName: ASCII-only stem of the Excel filename (strip Chinese prefixes)
- SheetName: Exact sheet name (always included — prevents cross-sheet collisions)
- ColumnHeader: Exact column header (Enhanced format only)
- RecordId: Primary key value of the row
- Separator: Underscore `_`

## Edge Cases

### 1. Header Row Data (Old Format)

In legacy 2-row header format, rows 3-4 may contain sample data:

```
Row 1: Id | DescriptionId
Row 2: Type | Type
Row 3: 0 | 817000000  ← This is data!
Row 4: 1 | 817000001  ← This is data!
Row 5: 2 | 817000002  ← Data continues
```

**Solution:** Include rows 3-4 in migration (they are not headers).

### 2. Missing Text Entries

Some IDs may not have matching text in ID2StringMapTable:

```python
if desc_id in id_to_text:
    # Migrate
else:
    print(f'Warning: No text found for ID {desc_id}')
```

### 3. Duplicate Keys

If Local sheet already has entries:

```python
# Find last occupied row
last_row = 5
while sheet_local.range(last_row, 1).value:
    last_row += 1

# Append new data starting from last_row
sheet_local.range(f'A{last_row}:C{last_row+len(loc_data)-1}').value = loc_data
```

---

## CRITICAL: xlwings Batch Writing - Data Structure vs Target Range Matching

⚠️ **CRITICAL ERROR PATTERNS TO AVOID**

**Real-world Incident**: When updating a single column (e.g., NameId) in a table, using a **2D list** with a **single-column range** caused data to spill into adjacent columns, corrupting the entire row.

### Understanding xlwings Batch Write Behavior

**CRITICAL: xlwings 1D lists ALWAYS fill horizontally by default!**

xlwings batch writing behavior depends on data structure and whether transpose is used:

| Data Structure | Write Method | Result |
|----------------|--------------|--------|
| 1D list `[a,b,c]` | `range('A1').value = ...` | ✗ Horizontal (A1, B1, C1) |
| **1D list `[a,b,c]`** | **`range('A1').options(transpose=True).value = ...`** | **✓ Vertical (A1, A2, A3)** |
| 2D list `[[a],[b],[c]]` | `range('A1').value = ...` | ✓ Vertical (A1, A2, A3) |
| 2D list `[[a,b,c]]` | `range('A1').value = ...` | ✗ Horizontal (A1, B1, C1) |
| 2D list `[[a,b],[c,d]]` | `range('A1').value = ...` | ✓ Rectangle (A1=a, B1=b, A2=c, B2=d) |

**Key Insight**: xlwings does NOT infer direction from the target range! Even if you write `range('A1:A10').value = list`, it will still fill horizontally if list is 1D.

### ❌ The Mistake (What Went Wrong)

```python
# WRONG: 1D list fills horizontally, not vertically!
updates = [
    'Loc_Module_1',
    'Loc_Module_2',
    'Loc_Module_3'
]

# Even with column range specified, this fills HORIZONTALLY
sheet.range('C5:C7').value = updates

# Results in DATA CORRUPTION:
# C5: Loc_Module_1  ✓ Correct position
# D5: Loc_Module_2  ✗ Wrong! Spilled to next column
# E5: Loc_Module_3  ✗ Wrong! Continues horizontally
# C6: (empty)
# C7: (empty)
```

**What actually happened**: xlwings ignores the column range and fills 1D lists horizontally by default, regardless of the target range specification.

### ✅ Solution 1: Use transpose (RECOMMENDED - Fast)

```python
# CORRECT: Use transpose to force vertical fill
updates = [
    'Loc_Module_1',
    'Loc_Module_2',
    'Loc_Module_3'
]

# transpose=True forces vertical fill
sheet.range('C5').options(transpose=True).value = updates  # ✓ Vertical!

# Result:
# C5: Loc_Module_1  ✓
# C6: Loc_Module_2  ✓
# C7: Loc_Module_3  ✓
```

### ✅ Solution 2: Convert to 2D List (Alternative)

```python
# CORRECT: Convert to 2D list (each row is one element)
updates = [
    ['Loc_Module_1'],
    ['Loc_Module_2'],
    ['Loc_Module_3']
]

sheet.range('C5').value = updates  # ✓ Vertical fill

# Result:
# C5: Loc_Module_1  ✓
# C6: Loc_Module_2  ✓
# C7: Loc_Module_3  ✓
```

### ✅ Solution 3: Cell-by-Cell Write (Safest)

```python
# CORRECT: Cell-by-cell (slower but precise)
for i, id_val in enumerate(ids):
    row_num = data_start_row + i
    new_loc_key = f'Loc_Module_{id_val}'
    sheet.range(row_num, 3).value = new_loc_key  # Direct cell assignment
```

### ✅ 2D List Only for Rectangular Multi-Column Ranges

```python
# CORRECT: 2D list for multi-column data
data = [
    ['key1', 'cn_text1', 'en_text1'],
    ['key2', 'cn_text2', 'en_text2'],
    ['key3', 'cn_text3', 'en_text3']
]
sheet.range(f'A3:C5').value = data  # 2D list + 3-column range = ✓
```

### ✅ Validation After Batch Write (MANDATORY)

**Always verify adjacent columns are not corrupted after single-column updates:**

```python
app = xw.App(visible=False)
app.display_alerts = False
app.screen_updating = False

try:
    wb = xw.Book('excel/YourFile.xlsx')
    sheet = wb.sheets['YourSheet']

    # Perform batch write with TRANSPOSE
    updates = ['Loc_1', 'Loc_2', 'Loc_3']
    sheet.range('C5').options(transpose=True).value = updates  # MUST use transpose!
    wb.save()

    # CRITICAL: Verify adjacent columns are not corrupted
    # Read target col and adjacent col in one batch for efficiency
    data_start_row = 5
    num_rows = 3  # C5:C7 in this example
    target_col = 3   # column C
    adjacent_col = 4  # column D

    # Verify each row: adjacent column should NOT contain Loc_* values
    corrupted = []
    for row in range(data_start_row, data_start_row + num_rows):
        adj_val = sheet.range(row, adjacent_col).value
        if isinstance(adj_val, str) and adj_val.startswith('Loc_'):
            corrupted.append((row, adjacent_col, adj_val))

    if corrupted:
        print(f'ERROR: Data spilled into adjacent column! Corrupted cells:')
        for row, col, val in corrupted:
            print(f'  Row {row} col {col}: {val}')
        # Fix: clear the corrupted cells
        for row, col, _ in corrupted:
            sheet.range(row, col).value = None
        print('Fixed: Cleared corrupted cells. Re-run write with transpose=True.')
    else:
        print('Validation passed: No adjacent column corruption detected.')

    wb.close()
finally:
    app.quit()
```

### Encoding Standards

**Add type hints and assertions:**

```python
from typing import List, Any

def safe_write_single_column(
    sheet: xw.main.Sheet,
    col: int,
    start_row: int,
    data: List[Any]
) -> None:
    """
    Safely write data to a single column.

    Args:
        sheet: xlwings sheet
        col: Column number (1-based)
        start_row: Starting row number (1-based)
        data: 1D list of values to write

    Raises:
        ValueError: If data is 2D list when single column is expected
    """
    if not data:
        return

    # Check data structure
    if isinstance(data[0], list):
        raise ValueError(
            "Single-column write requires 1D list. "
            f"Found 2D list with {len(data[0])} columns. "
            "Use 1D list: [val1, val2, val3] instead of [[val1], [val2], [val3]]"
        )

    # Write data
    end_row = start_row + len(data) - 1
    sheet.range(f'{xw.utils.col_name(col)}{start_row}:{xw.utils.col_name(col)}{end_row}').value = data

# Usage
try:
    safe_write_single_column(sheet, 3, 5, ['Loc_1', 'Loc_2', 'Loc_3'])
except ValueError as e:
    print(f'Error: {e}')
```

### Quick Reference Table

| Task | Data Structure | Code Pattern | Status |
|------|----------------|--------------|--------|
| Write to single column | `['a', 'b', 'c']` | `range('A1').options(transpose=True).value = ...` | ✓ CORRECT |
| Write to single column | `[['a'],['b'],['c']]` | `range('A1').value = ...` | ✓ Alternative |
| Write to single row | `['a', 'b', 'c']` | `range('A1').value = ...` | ✓ Horizontal fill |
| Write to rectangle | `[['a','b'],['c','d']]` | `range('A1').value = ...` | ✓ Multi-column |
| Write to single column (safe) | Use loop | `range(row, col).value = val` | ✓ Safest |
| **WRONG:** Write to column | `['a', 'b', 'c']` | `range('A1:A3').value = ...` | **✗ FILLS HORIZONTALLY!** |

### When This Error Occurs

**Symptoms:** After a batch update, columns adjacent to the target column contain unintended data like Loc_* keys.

**Root Cause:** Using 2D list `[[val1], [val2], ...]` with single-column range `'A1:A10'`.

**Prevention:**
1. Always use 1D lists for single-column updates
2. Use assertions to catch 2D lists accidentally passed to single-column writes
3. Verify adjacent columns after critical updates
4. For high-risk operations, use cell-by-cell loop

**Recovery:**
1. Identify corrupted rows (check adjacent columns for Loc_* patterns)
2. Restore original data if available
3. Use 1D list to re-write correct values
4. Verify all adjacent columns are clean

---

## Performance Optimization

### xlwings Best Practices

```python
# ✓ Good: Batch operations
sheet.range('A5:C100').value = [[...], [...], ...]

# ✗ Bad: Row-by-row
for i, row_data in enumerate(data):
    sheet.range(5+i, 1).value = row_data[0]
    sheet.range(5+i, 2).value = row_data[1]
    sheet.range(5+i, 3).value = row_data[2]
```

**Speed comparison:**
- Batch: 0.5 seconds for 300 rows
- Row-by-row: 50+ seconds for 300 rows

**IMPORTANT:** When using batch operations for single-column updates, ensure data is 1D list, not 2D list. See "CRITICAL: xlwings Batch Writing" section above.

### Settings

```python
app = xw.App(visible=False)        # Background mode
app.display_alerts = False         # No popup dialogs
app.screen_updating = False        # No screen updates
```

## File Changes Checklist

> The verification checklist is in the **Standard Workflow** section above (Step 5).
> Use the detailed checklist below only when doing manual fallback migration.

### Pre-Migration Verification (Before Phase 1)

- [ ] **Proto field type checked**
  - [ ] Verified field definition in `converter/resource/desc/client/res_client_struct.proto`
  - [ ] If `string` → No proto change needed
  - [ ] If `uint32`/`int32` → Proto update required after migration (see below)

### Post-Migration Verification

After completing text migration, verify all changes:

- [ ] **`{Module}.xlsx` → Local sheet**: Created with 4-row header, added localization texts
  - [ ] Row 4 export targets set correctly (typically `[PrimaryKey, Client, Client]`)
  - [ ] Data starts at row 5
  - [ ] Keys follow naming convention: `Loc_{Module}_{Sheet}_{Field}_{Id}` or `Loc_{Module}_{Sheet}_{Id}`

- [ ] **`{Module}.xlsx` → Source sheet**: Field type and values updated
  - [ ] Row 2 field type changed to `string` (from `uint32`)
  - [ ] Data rows updated with new Loc keys

- [ ] **`res_client_struct.proto`**: Field type updated
  - [ ] Changed from `uint32 FieldName` to `string FieldName`

- [ ] **`ID2StringMapTable.xlsx` → Main**: Migrated rows deleted
  - [ ] Used xlwings (not openpyxl) for deletion
  - [ ] Newline formatting preserved in remaining data
  - [ ] No duplicate IDs remain

- [ ] **`convert_list.xml`**: Local sheet added to Key2StringMapTable (client)
  - [ ] DataSource added to `Client_Key2StringMapTable` item
  - [ ] Format: `../../excel/{Module}.xlsx|Local|5,1`
  - [ ] NOT created as separate item configuration

- [ ] **`convert_list_server.xml`**: (If server export) Local sheet added to Key2StringMapTable
  - [ ] Check export target: Client only / Server only / Both
  - [ ] If Server only or Both: DataSource added to `Server_Key2StringMapTable` item
  - [ ] Format: `../../excel/{Module}.xlsx|Local|5,1`
  - [ ] If Client only: No changes needed to server XML

- [ ] **Temporary files**: Cleaned up
  - [ ] `temp_migration_data.json` deleted

## Decision Points and AskUserQuestion Usage

Use `AskUserQuestion` tool when information is insufficient:

### 1. Export Target (when creating new Local sheet)

**When to ask:** Creating a new Local sheet without existing proto definition

**Question:**
```
"Should the localization data in {ModuleName} Local sheet be exported to:
 - Client only (recommended for UI texts)
 - Server only
 - Both client and server?"
```

**Typical answer:** Client only → Set Row 4 to `[PrimaryKey, Client, Client]`

### 2. Naming Convention

**When to ask:** Multiple text fields exist in the same record, unclear which format to use

**Question:**
```
"Should we use the basic naming format (Loc_{Module}_{Sheet}_{Id}) or enhanced format (Loc_{Module}_{Sheet}_{Field}_{Id})?

Context:
- Basic format: Simpler, works when only one text field per record
- Enhanced format: More descriptive, includes column name, recommended by default

Example for PlayerAbility (Main sheet):
- Basic: Loc_PlayerAbility_Main_1
- Enhanced: Loc_PlayerAbility_Main_Name_1"
```

**Recommendation:** Use enhanced format when multiple text fields exist

### 3. Text Source Location

**When to ask:** User mentions migrating texts but doesn't specify source location

**Question:**
```
"Where is the source text data located?

Default is excel/ID2StringMapTable.xlsx Main sheet. Is this correct, or is the text in a different location?"
```

**Default assumption:** `excel/ID2StringMapTable.xlsx` Main sheet (standard for NBA2kOL3)

## Example: CsRetError Migration

### Before Migration

**ErrorCodeFeedback.xlsx / CsRetError:**
```
Id | DescriptionId
2  | 817000002
3  | 817000003
```

**ID2StringMapTable.xlsx / Main:**
```
Id        | SystemLanguageCn | SystemLanguageEn
817000002 | 服务器内部错误    | Server error
817000003 | 缺少玩家信息      | Missing player info
```

### After Migration

**ErrorCodeFeedback.xlsx / Local:**
```
Id                  | SystemLanguageCn | SystemLanguageEn
Loc_CsRetError_2    | 服务器内部错误    | Server error
Loc_CsRetError_3    | 缺少玩家信息      | Missing player info
```

**ErrorCodeFeedback.xlsx / CsRetError:**
```
Id | DescriptionId
2  | Loc_CsRetError_2
3  | Loc_CsRetError_3
```

**ID2StringMapTable.xlsx / Main:**
```
(Rows 817000002 and 817000003 deleted)
```

**res_client_struct.proto:**
```protobuf
message CsRetError {
    uint32 Id = 1;
    string DescriptionId = 3;  // Changed from uint32
}
```

## Troubleshooting

### CLI Produces No Output (Silent Exit)

**Symptom**: Running `migrate-text` (with or without `--dry-run`) exits immediately with no output and no error message.

**This is different from a hang** — the process exits cleanly (exit code 0) but did nothing.

**Diagnosis steps:**

```bash
# Step 1: Check for residual Excel instances that may cause early return
python -c "import xlwings as xw; print(f'Active Excel apps: {len(xw.apps)}')"

# Step 2: Kill any residual Excel processes
tasklist | findstr /i EXCEL
taskkill /F /IM EXCEL.EXE  # Only if Excel processes found

# Step 3: Check for stale lock files
dir excel | findstr "~$"
# If lock files exist, delete them after confirming no Excel is open
```

**After clearing Excel processes**, retry the CLI command. If still silent, proceed to [Fallback: Manual Migration Workflow](#fallback-manual-migration-workflow).

**Root causes observed:**
- `table_tool.py` encountered an exception internally and exited silently (bug in CLI error handling)
- File path encoding issue with Chinese filenames in Git Bash (use absolute paths to mitigate)
- Excel COM initialization failed silently

### Excel File Locked

If xlwings hangs or file cannot be saved:

```python
# 1. Try closing the specific workbook
try:
    app = xw.apps.active
    for wb in app.books:
        if 'YourFileName.xlsx' in wb.fullname:
            wb.close()
            break
except:
    pass

# 2. Force close Excel (Windows)
import subprocess
subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'],
               stderr=subprocess.DEVNULL)
```

### Formula Loss Warning

**Never use openpyxl for write operations** - it strips all formulas.

```python
# ✓ Correct: xlwings preserves formulas
import xlwings as xw
wb = xw.Book('file.xlsx')
wb.save()

# ✗ Wrong: openpyxl loses formulas
from openpyxl import load_workbook
wb = load_workbook('file.xlsx')
wb.save('file.xlsx')  # Formulas gone!
```

### Data Validation

Always verify:
1. Row count matches expected
2. No duplicate keys in Local sheet
3. All source references updated
4. Proto compilation succeeds
5. Conversion test passes (`convert.bat`)

## Related Operations

- **Adding Local Sheet**: See [macrostring.md](macrostring.md) for Local sheet creation
- **Format Conversion**: See [format-conversion.md](format-conversion.md) for header format migration
- **Proto Generation**: See [proto-generation.md](proto-generation.md) for message definition creation
