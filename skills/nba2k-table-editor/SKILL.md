---
name: nba2k-table-editor
description: NBA2kOL3 Excel configuration table management tool for designers. Use when working with game config tables in the Table repository: (1) Adding new configuration sheets to existing Excel files, (2) Adding new configuration tables, (3) Converting Legacy (2-row header) to NBA2kOL3 (4-row header) format, (4) Generating/updating proto message definitions, (5) Visualizing table structure with DOT graphs, (6) Managing MacroString enum definitions, (7) Validating field references between tables, (8) Migrating module texts to Local sheet with localization keys, (9) Executing table-to-binary conversion. Also use when the user mentions "本地化sheet" or "本地化Sheet" — these are Chinese terms that always refer to the Excel "Local" sheet in this project. This skill provides direct access to Table Toolkit operations and follows the project's established workflow.
---

# NBA2kOL3 Table Editor

## 术语说明

| 用户说法 | 实际含义 |
|---------|---------|
| 本地化sheet / 本地化Sheet | Excel 中名为 `Local` 的 sheet |

当用户说"添加本地化sheet"、"本地化sheet"等，均指在 Excel 文件中创建或操作名为 `Local` 的 sheet。

---

## 🚨 CRITICAL: MANDATORY EXECUTION PROTOCOL

**BEFORE STARTING ANY TASK, YOU MUST:**

1. **Read the relevant documentation file FIRST**
   - For MacroString tasks: Read `references/macrostring.md` IMMEDIATELY
   - **When checking / adding `<indexer>` in `convert_list_server.xml`, or verifying server primary key config: Read `references/indexer-type-check.md` IMMEDIATELY**
   - For other tasks: Read the corresponding references file
   - DO NOT skip this step - the documentation contains the complete workflow

2. **Create a complete TodoWrite checklist based on the documentation**
   - Include EVERY step from the documentation
   - Do NOT improvise or skip steps based on assumptions
   - Mark each step as you complete it

3. **Execute ALL steps in the documentation**
   - Complete each step in order
   - Do NOT declare the task complete until ALL steps are done
   - Verify each step before moving to the next

**FAILURE TO FOLLOW THIS PROTOCOL WILL RESULT IN INCOMPLETE WORK.**

## 写引擎优先级（Write Engine Priority）

对 Excel 文件执行**写操作**时，按以下优先级选择方案：

| 优先级 | 方案 | 触发条件 |
|--------|------|---------|
| 🥇 **优先** | `table_tool` CLI / `XlsxWriter`（minimax-xlsx） | 目标操作已在 CLI 或 XlsxWriter 中支持 |
| 🥈 **次选** | 直接调用 `XlsxWriter`（minimax-xlsx XML 操作） | CLI 不支持，但 XlsxWriter 方法可覆盖 |
| 🥉 **兜底** | `xlwings`（需 Excel.exe 进程） | 以上两种均不支持时 |

**判断逻辑：**
```
该操作是否有对应的 table_tool CLI 命令？
├── 是 → 用 table_tool CLI
└── 否 → XlsxWriter 能否完成（add_sheet / update_cell / delete_rows / write_rows 等）？
         ├── 是 → 直接用 XlsxWriter
         └── 否 → 用 xlwings（并在任务结束时报告"未支持场景"）
```

**目前 XlsxWriter 支持的操作（勿再用 xlwings）：**

> `XlsxWriter` 位于本仓库 `table_tool/table_toolkit/core/xlsx_writer.py`，通过 `from table_tool.table_toolkit.core.xlsx_writer import XlsxWriter` 导入。

- 新建 sheet：`writer.add_sheet(name)`
- 写入行数据：`writer.insert_row_content` / `writer.write_rows`（**仅追加空位**；在已有数据中间插入必须先 `shift_rows(at=row_num, delta=1)` 推移后续行，否则产生重复行号导致数据丢失）
- 更新单个单元格：`writer.update_cell(sheet_name, row, col_letter, cell_type, value)`（`col_letter` 必须是 `U` 这类列字母，不是数字列号；字符串通常用 `inlineStr`）
- 删除行并重排行号：`writer.delete_rows`
- 追加 sharedStrings：`writer.append_shared_strings`
- 查找 sharedStrings 索引：`writer.find_shared_string_index`
- 获取 sheet 列表 / 最后数据行：`writer.get_sheet_names` / `writer.get_last_data_row`

> ⚠️ **`get_last_data_row` 返回的是最后一个含实际值（`<v>`）的行号**，排除了 Excel 保存时可能产生的样式空行（有 `<row>` 标签但无 `<v>`）。追加行后应验证新行行号是否紧邻已有数据（见下方"验证写入正确性"）。

> ⚠️ **不要**在上述操作上继续使用 xlwings — 它们都已在 XlsxWriter 中实现且无进程残留风险。

**XlsxWriter 标准调用模板（必须 unpack → 操作 → pack）：**

```python
import sys
sys.path.insert(0, 'table_tool')
from table_toolkit.core.xlsx_writer import XlsxWriter

writer = XlsxWriter('excel/YourFile.xlsx')
writer.unpack()          # ← 必须先 unpack，否则操作会 FileNotFoundError

# 执行一个或多个操作
writer.delete_rows('Local', rows_to_delete)
writer.update_cell('Main', 5, 'B', 'inlineStr', 'new_value')
writer.update_cell('Main', 6, 'C', 'n', 123)
# writer.add_sheet('NewSheet') ...

writer.pack()            # ← 就地覆盖原文件（不传参数）；传路径则写到指定位置
```

> ⚠️ **LESSON LEARNED（2026-05-16）**: 直接调用 `writer.delete_rows(...)` 而不先 `unpack()` 会立即抛出 `FileNotFoundError`，因为 XlsxWriter 操作的是解包后的临时目录，未解包时目录为空。
>
> ⚠️ **LESSON LEARNED（2026-06-11）**: 用 `update_cell()` 在工作表最右侧新增字段 / 新列时，单元格本身可能已写入成功，但依赖 OOXML `<dimension>` 的工具（如 ugit 外部预览、部分只读解析器）仍可能看不到新列。原因是当前 `pack()` 的 dimension 修复更偏向修正末行，未必会把末列从 `T` 扩到 `U`。因此，**新增最右列后必须额外验证 `<dimension ref="...">` 是否覆盖到新列**；不要只看 `openpyxl` 普通模式，因为它可能重算维度、掩盖底层 XML 仍然过窄的问题。

---

## 读操作优先级（Read Query Priority）

对 Excel 文件执行**只读查询 / 条件筛选 / 聚合统计**时，按以下优先级：

| 优先级 | 方案 | 适用场景 |
|--------|------|---------|
| 🥇 **优先** | `pandas.read_excel()` | 条件筛选、列查找、多列组合查询、聚合统计 |
| 🥈 **次选** | `openpyxl`（正常模式） | 只需读表头/结构、或需要精确访问单元格格式 |

**pandas 典型用法：**
```python
import pandas as pd

# header=0 以 Row1 为列名，skiprows=[1,2,3] 跳过 Row2-4（类型/注释/导出目标）
df = pd.read_excel('excel/Foo.xlsx', sheet_name='Main', header=0, skiprows=[1, 2, 3])

# 向量化筛选，秒级完成
type_cols = [c for c in df.columns if 'EventAttribute' in c and '.type' in c]
mask = df[type_cols].isin(['TARGET_ENUM_VALUE']).any(axis=1)
print(df.loc[mask, 'Id'].tolist())
```

**openpyxl 读取注意事项：**
- 使用**正常模式**（不加 `read_only=True`）处理大表随机访问，避免 XML 重复解析导致超时
- `read_only=True` 仅适合顺序 `iter_rows()` 遍历，不适合 `ws.cell(r, c)` 随机访问

> ⚠️ `pandas.to_excel()` **禁止用于写操作**（破坏公式/格式），但 `read_excel()` 读取无此限制，放心使用。

---

## 🎯 INTERACTION PROTOCOL FOR TEXT MIGRATION

**When migrating localization text to Local sheet, ALWAYS follow this CLI-first workflow:**

1. **Check proto field type first**
   ```bash
   grep "FieldName" converter/resource/desc/client/res_client_struct.proto
   ```
   - If `string` → no proto change needed
   - If `uint32`/`int32` → must update proto after migration (note this)

2. **Preview with dry-run using absolute path**
   ```bash
   python table_tool/table_tool.py migrate-text G:/Git/.../excel/YourModule.xlsx --field FieldName --dry-run
   ```
   - **Always use absolute paths on Windows** to avoid Git Bash encoding issues with Chinese filenames

3. **展示 Loc key 样例并请用户确认**
   - 根据文件名、Sheet 名和字段名，计算出将要生成的 Loc key 格式，展示给用户确认：
     ```
     将生成的 Loc key 格式（ENHANCED）：
       Loc_{ModuleName}_{SheetName}_{ColumnHeader}_{RecordId}
     示例：
       Loc_TacticsSettings_GameTacticsOption_TacticsOptionsTextual_1
       Loc_TacticsSettings_GameTacticsOption_TacticsOptionsTextual_2
       ...
     共 N 条记录
     ```
   - **ModuleName** 规则：取文件名主干，去掉非 ASCII 前缀（如"S赛事模式_"），只保留纯英文部分
   - **SheetName** 规则：直接使用 `--sheet` 参数指定的 Sheet 名（默认为 `Main`）
   - **ColumnHeader** 规则：直接使用 `--field` 参数指定的字段列名
   - 使用 `AskUserQuestion` 请用户确认 key 格式是否合适，再执行迁移
   - 若用户希望调整（如使用 `--basic` 格式或自定义前缀），按需修改命令

4. **Run the actual migration**
   ```bash
   python table_tool/table_tool.py migrate-text G:/Git/.../excel/YourModule.xlsx --field FieldName
   ```
   - The CLI handles Phase 0–5 automatically (proto check, ID collection, Local sheet create/update, source update, ID2StringMapTable cleanup)
   - **After writing to Local sheet, the CLI automatically validates key uniqueness**
     - If duplicates are detected → CLI raises `ValueError` with duplicate key details → migration aborted, file NOT saved
     - If all keys are unique → prints "Key uniqueness check passed: N unique key(s) in Local sheet"

4. **Verify XML config was updated** (CLI auto-does this as Phase 6; check if it worked)
   ```bash
   grep "YourModule.xlsx|Local" converter/convert_list.xml
   ```
   - If found → done
   - If missing → add `<scheme name="DataSource" ...>../../excel/YourModule.xlsx|Local|5,1</scheme>` to `Client_Key2StringMapTable` manually

5. **验证写入正确性**（必须执行）
   - 验证目标列值已正确更新为 Loc keys（检查数据起始行的前几个值）
   - 验证相邻列未被污染（检查是否有不该出现的 Loc_ 前缀）
   - **验证 Local sheet 新增行紧邻已有数据**（防止样式空行导致间隙）
   - **验证 `<dimension>` 覆盖新数据范围**（防止 read_only 工具看不到新行）
   ```bash
   python -c "
   import openpyxl
   wb = openpyxl.load_workbook('excel/YourModule.xlsx', data_only=True)
   sheet = wb['Local']
   # 打印所有非空行的 (Id, 行号)，确认末尾新增行紧邻最后一条旧数据
   rows_with_data = [(sheet.cell(r, 1).value, r) for r in range(5, sheet.max_row+1) if sheet.cell(r, 1).value is not None]
   print('Local 数据行:', rows_with_data[-5:])  # 查看最后5行
   # 如果出现 Id=None 的间隔行，说明有样式空行问题
   "
   ```
   ```bash
   python -c "
   import openpyxl
   # 用 read_only=True 验证 dimension 已正确覆盖新数据（最严格的模式）
   wb = openpyxl.load_workbook('excel/YourModule.xlsx', read_only=True, data_only=True)
   sheet = wb['Local']
   rows = [r[0].value for r in sheet.iter_rows(min_row=5) if r[0].value is not None]
   print(f'read_only 模式下 Local sheet 记录数: {len(rows)}')
   wb.close()
   # 若此数 < 预期总记录数，说明 dimension 未更新（用当前版本 XlsxWriter 不应出现）
   "
   ```
   ```bash
   python -c "
   import openpyxl
   wb = openpyxl.load_workbook('excel/YourModule.xlsx', data_only=True)
   sheet = wb['YourSheet']
   # Check target column and adjacent column
   for row in range(5, 10):
       target = sheet.cell(row, TARGET_COL).value
       adjacent = sheet.cell(row, TARGET_COL + 1).value
       print(f'Row {row}: target={target}, adjacent={adjacent}')
       if isinstance(adjacent, str) and adjacent.startswith('Loc_'):
           print(f'ERROR: Row {row} adjacent column polluted!')
   "
   ```

6. **Update proto if needed** (only when proto type was NOT string)
   - Edit `converter/resource/desc/client/res_client_struct.proto`
   - Change `uint32 FieldName` → `string FieldName`

**If the CLI command hangs, exits silently with no output, or produces unexpected results:** See the Troubleshooting section. **Silent exit (no output, exit code 0) is NOT a success indicator** — always verify actual data changes. Fall back to manual scripting only as a last resort.

**NEVER write manual Python scripts for migration unless the CLI command fails.**

---

## 🎯 INTERACTION PROTOCOL FOR FORMAT CONVERSION

**When performing format conversion, ALWAYS follow this interactive workflow:**

1. **First: Preview with dry-run**
   - Execute `python table_tool/table_tool.py convert ... --dry-run` FIRST
   - Capture the output to detect enum field suggestions

2. **If enum fields detected: Ask the user**
   - Parse output for lines like "检测到 X 个枚举字段建议添加@符号"
   - Extract the specific field rename suggestions (e.g., `BadgeType -> BadgeType@BadgeType`)
   - Use `AskUserQuestion` tool with clear options:
     - Question: "检测到以下枚举字段可以添加 @ 符号以明确类型，是否自动重命名？\n\n重命名建议：\n{list of suggestions}"
     - Option 1: "Yes, auto-rename enum fields (推荐)" → Add `--auto-rename-enum` flag
     - Option 2: "No, keep current field names" → Proceed without flag

3. **Execute with user's choice**
   - Run the actual conversion command with or without `--auto-rename-enum` based on user response

**NEVER skip the user question when enum fields are detected.**

---

# NBA2kOL3 Table Editor

## Quick Start

Add a new configuration table:
```bash
# 1. Create Excel file in excel/ directory
# 2. Follow 4-row header format (data starts at row 5)
# 3. Generate proto definitions
python table_tool/table_tool.py generate excel/NewTable.xlsx --target server

# 4. Update XML configs if needed
# 5. Test conversion
cd converter
convert.bat  # Windows
```

Migrate localization text to Local sheet:
```bash
# Migrate text from ID2StringMapTable to module's Local sheet
python table_tool/table_tool.py migrate-text excel/YourModule.xlsx --field DescriptionId

# Preview changes without modifying files
python table_tool/table_tool.py migrate-text excel/YourModule.xlsx --field DescriptionId --dry-run

# Use basic naming format (Loc_Module_Id instead of Loc_Module_Field_Id)
python table_tool/table_tool.py migrate-text excel/YourModule.xlsx --field DescriptionId --basic

# Export to both client and server
python table_tool/table_tool.py migrate-text excel/YourModule.xlsx --field DescriptionId --export-target both
```

## Command Reference

### migrate-text - Text Migration Command

Migrate module-specific localization text from global ID2StringMapTable to the module's own Local sheet with proper Loc key naming.

**Basic Syntax:**
```bash
python table_tool/table_tool.py migrate-text <excel_file> --field <field_name> [options]
```

**Required Arguments:**
- `excel_file` - Path to Excel file (e.g., `excel/YourModule.xlsx`)
- `--field` - Field column name to migrate (e.g., `DescriptionId`)

**Options:**
- `--sheet` - Source sheet name (default: `Main`)
- `--basic` - Use basic naming format `Loc_Module_Sheet_Id` instead of `Loc_Module_Sheet_Field_Id` (default: enhanced)
- `--export-target` - Export target for Local sheet: `client` (default), `server`, or `both`
- `--dry-run` - Preview changes without modifying files

**Examples:**
```bash
# Standard migration (enhanced naming format, client-only export)
python table_tool/table_tool.py migrate-text excel/S赛事模式_TacticsSettings.xlsx --field DefaultTacticsTextual

# Preview what will change
python table_tool/table_tool.py migrate-text excel/S赛事模式_TacticsSettings.xlsx --field DefaultTacticsTextual --dry-run

# Basic naming format for simpler Loc keys
python table_tool/table_tool.py migrate-text excel/PlayerAbility.xlsx --field AbilityDescription --basic

# Export text to both client and server
python table_tool/table_tool.py migrate-text excel/SharedConfig.xlsx --field SystemMessage --export-target both
```

**Naming Formats:**
- **Enhanced (default):** `Loc_Module_Sheet_Field_Id` - Provides full namespace, prevents cross-sheet collisions
  - Example: `Loc_TacticsSettings_Main_DefaultTacticsTextual_1`
- **Basic:** `Loc_Module_Sheet_Id` - Simpler when field context is obvious
  - Example: `Loc_TacticsSettings_Main_1`

**Workflow:**
1. Phase 0: Check proto field type (warns if not 'string')
2. Phase 1: Collect referenced text IDs from source sheet
3. Phase 2: Extract matching text from ID2StringMapTable
4. Phase 3: Create or update Local sheet with new Loc keys
5. Phase 4: Update source field to use Loc keys
6. Phase 5: Clean up migrated entries from ID2StringMapTable

## Table Format

### NBA2kOL3 Standard (4-Row Header)

| Row | Purpose |
|-----|---------|
| 1   | Field names (match proto field names) |
| 2   | Field types (uint32, string, etc.) |
| 3   | Comments |
| 4   | Export targets |
| 5+  | Data |

### Export Targets (Row 4)
- `PrimaryKey` - Primary key, exported to client + server
- `Client` - Client only
- `Server` - Server only
- Empty - Both client + server
- `Skip` - Not exported

## Capabilities

### Adding a New Sheet to Existing Excel File
Add a new configuration sheet to an existing Excel file with complete proto and XML configuration setup.

**Documentation:** [references/add-new-sheet.md](references/add-new-sheet.md)

### Format Conversion
Convert Legacy (2-row header) Excel files to NBA2kOL3 standard (4-row header) format.

**Documentation:** [references/format-conversion.md](references/format-conversion.md)

### Proto Generation
Generate Protocol Buffer message definitions based on Excel table structure.

**Documentation:** [references/proto-generation.md](references/proto-generation.md)

### Visualization
Generate DOT graphs to visualize table structure and relationships between tables.

**Documentation:** [references/visualization.md](references/visualization.md)

### Enum Management
Manage and synchronize enum definitions across game configuration tables.

**Documentation:** [references/enum-management.md](references/enum-management.md)

### Table Validation
Validate Excel table structure and cross-table field references.

**Documentation:** [references/validation.md](references/validation.md)

### Adding MacroString
Add new macrostring text configurations for localized game UI strings.

> ⚠️ **流程已变更**：MacroString 现在通过独立技能 `nba2k-macrostring` 处理，只需修改 `MacroTable.conf`，不再操作 Excel 或 proto 文件。遇到 MacroString 需求时，请直接使用 `/nba2k-macrostring` 技能。

### Text Migration
Migrate module-specific texts from global ID2StringMapTable to module's Local sheet with proper localization key naming.

**Always follow the CLI-first workflow in the INTERACTION PROTOCOL section above before reading this reference.**

**Documentation:** [references/text-migration.md](references/text-migration.md)

### Indexer Type & Primary Key Check
验证 `convert_list*.xml` 中 `<indexer>` 配置的类型与 proto 一致，并检查 server 端非 `Id` 主键是否已在 proto message 头部声明 `option (primary_key_field)`。

**触发时机：**
- 新增或修改 `convert_list_server.xml` 中的 `<indexer>` 配置时
- 检查 server 端表的主键配置是否符合要求时
- server 转表报 `Type mismatch` / `Invalid key type` 错误时

**Documentation:** [references/indexer-type-check.md](references/indexer-type-check.md)

### Local Sheet Cleanup
扫描 Main sheet 中实际引用的 Loc_ keys，删除 Local sheet 中未被引用的孤立记录，保持 Local sheet 与 Main sheet 的数据一致性。

**操作步骤：**
1. 用 `openpyxl` 读取 Main sheet，收集所有 `Loc_` 开头的值
2. 用 `openpyxl` 读取 Local sheet，记录所有 key → 行号的映射
3. 计算差集，找出未被引用的行号列表
4. 用 `XlsxWriter.delete_rows()` 删除（unpack → delete_rows → pack）
5. 用 `openpyxl` 验证：Local 行数 = Main 引用数，无缺失无多余

## Project Structure

```
Table/
├── excel/                    # Source Excel files
├── converter/
│   ├── convert.bat          # Client conversion (Windows)
│   ├── convert.sh           # Server conversion (Linux)
│   ├── convert_list.xml     # Client config
│   ├── convert_list_server.xml  # Server config
│   └── resource/
│       ├── desc/            # Proto definitions
│       │   ├── client/
│       │   └── server/
│       └── bin/             # Binary output (generated)
└── doc/
    └── table_tool.py        # Table Toolkit CLI
```

## Adding a New Table

1. Create Excel in `excel/` following 4-row format
2. Run proto generation
3. Update `convert_list.xml` and/or `convert_list_server.xml`
4. Add proto message to `resource/desc/client/res_client_struct.proto` or `resource/desc/server/res_server.proto`
5. Test conversion with `convert.bat`

## Type Inference

Field types determined by:
1. Excel Row 2 (explicit type, highest priority)
2. Proto definition
3. Field name pattern (e.g., `Ranking*` → uint32)
4. Default: string

Supported types: `uint32`, `int32`, `uint64`, `int64`, `float`, `double`, `bool`, `string`

For enum types: use `FieldName@EnumType` syntax in Row 1, specify `enum` in Row 2.

## Important Notes

- **写操作优先使用 table_tool / XlsxWriter（无 Excel 进程）**，参见上方"写引擎优先级"
- xlwings 仅在 XlsxWriter 无法覆盖时使用（兜底），使用后需报告"未支持场景"（见下方）
- Generated files are in .gitignore
- Excel temp files (`~$*.xlsx`) should not be committed
- Legacy format uses `DataSource="...|3,1"`, NBA2kOL3 format uses `DataSource="...|5,1"`
- The `visualize` command preserves existing table structures and reference edges by default

## xlwings 兜底使用规范（仅当 XlsxWriter 不支持时）

> **本节仅适用于 XlsxWriter 尚未支持的场景**（如复杂公式保留、条件格式、数据验证等）。  
> 对于 add_sheet / delete_rows / write_rows / update_cell 等，请直接用 XlsxWriter，不要走这里。
>
> ⚠️ **以下所有注意事项（Excel 进程检查、写入验证、1D list 方向）均只在使用 xlwings 时才需要关注。**  
> 使用 XlsxWriter / table_tool CLI 时完全不需要，因为它们是纯 Python XML 操作，不启动任何 Excel.exe 进程。

### ① 操作前：确认用户已关闭 Excel（xlwings 专属）

**LESSON LEARNED（2026-03-25）**: 用户忘记关闭 Excel 时，`wb.save()` 不报错但数据写入无效。xlwings 在文件被 Excel 占用时以共享模式打开，`save()` 写入的是临时副本，不覆盖原文件。

**执行 xlwings 写操作前必须检查：**
```bash
tasklist | findstr /i EXCEL   # 检查是否有 Excel 进程
dir excel | findstr "~$"      # 检查是否有文件锁
```
如果发现 Excel 进程，先提醒用户关闭 Excel，再执行操作。不要直接 `taskkill`（会丢失用户未保存的工作）。

### ② 验证写入：必须用全新的 app 实例（xlwings 专属）

**LESSON LEARNED（2026-03-25）**: 同一个 xlwings app 实例重新打开同一文件，读到的是内存缓存，不是磁盘数据，会误判"写入失败"。

```python
# ❌ 错误：同一 app 重新 open，读到的是缓存
wb2 = app.books.open('file.xlsx')
print(wb2.sheets['Sheet1'].range('A1').value)  # 可能还是旧值！

# ✅ 正确方式一：退出 app 后重新创建
app.quit()
app2 = xw.App(visible=False)
wb2 = app2.books.open('file.xlsx')
print(wb2.sheets['Sheet1'].range('A1').value)
app2.quit()

# ✅ 正确方式二：用 openpyxl 验证（直接读磁盘，无缓存）
import openpyxl
wb_check = openpyxl.load_workbook('file.xlsx', data_only=True)
print(wb_check['Sheet1']['A1'].value)
```

**兜底手段**：用 `os.path.getmtime()` 确认文件 mtime 变化：
```python
import os
mtime_before = os.path.getmtime('excel/YourFile.xlsx')
# ... 执行写入 ...
print('文件已修改:', os.path.getmtime('excel/YourFile.xlsx') != mtime_before)
```

### ③ 单列批量写入：必须用 transpose=True（xlwings 专属）

⚠️ **已发生事故（2026-03-11）**: `sheet.range('B5:B16').value = list` 写入 1D list 导致值横向溢出污染整行，需要 git history 恢复。xlwings 1D list 默认横向填充，即使目标是列范围。

```python
# ❌ 错误（1D list 横向溢出）
sheet.range('B5:B16').value = ['Loc_1', 'Loc_2', ..., 'Loc_12']
# 结果: B5='Loc_1', C5='Loc_2', D5='Loc_3', ... (全行污染!)

# ✅ 正确（transpose=True 纵向写入）
sheet.range('B5').options(transpose=True).value = ['Loc_1', 'Loc_2', ..., 'Loc_12']
# 结果: B5='Loc_1', B6='Loc_2', B7='Loc_3', ...
```

写入后验证相邻列未被污染：
```python
for i in range(len(new_values)):
    adj = sheet.range(start_row + i, target_col + 1).value
    if isinstance(adj, str) and adj.startswith('Loc_'):
        raise ValueError(f'横向溢出！Row {start_row + i} 相邻列被污染: {adj}')
```

### ④ 代码模板（xlwings 兜底时使用）

**Always use context managers:**
```python
import xlwings as xw

with xw.App(visible=False) as app:
    app.display_alerts = False
    app.screen_updating = False
    wb = app.books.open('excel/YourFile.xlsx')
    sheet = wb.sheets['Sheet1']
    sheet.range('A1').value = 'test'
    wb.save()
    # Cleanup automatic on exit
```

**If inline scripts are necessary:**
```python
app = None
try:
    app = xw.App(visible=False)
    app.display_alerts = False
    # ... code ...
finally:
    if app:
        app.quit()
```

**Check for residual instances:**
```python
import xlwings as xw
print(f"Active Excel instances: {len(xw.apps)}")
```

---

## CRITICAL: 临时文件管理规范

任务执行过程中有时需要写中间数据文件（如 JSON、txt）。这类文件如果清理不干净会遗留在仓库里，造成困惑。

**两条强制规则：**

### 1. 统一命名 + 固定写入项目根目录（绝对路径）

写临时文件时，**必须用绝对路径**，写到项目根目录，文件名统一加 `_claude_temp_` 前缀：

```python
import os

# 先确定项目根目录（converter/ 的上级）
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 或者直接硬编码（更可靠）
project_root = 'G:/Git/table_side'

# ✅ 正确：绝对路径 + 前缀
with open(f'{project_root}/_claude_temp_row_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)

# ❌ 错误：相对路径，实际落点依赖 working directory
with open('temp_row_data.json', 'w') as f:  # 落在哪取决于 cwd，清理时容易漏
    json.dump(data, f)
```

为什么这样做：shell 的 working directory 在任务过程中可能因 `cd` 而改变（例如 `cd converter` 后再写文件）。使用绝对路径可以保证写入和清理时路径完全一致，不会因为 cwd 变化而找不到文件。

### 2. 清理后必须验证文件确实不存在

清理完毕后，**必须执行一次文件存在性检查**，不能只跑 `rm` 就当清理完成：

```powershell
# PowerShell 清理 + 验证（推荐）
$tmpFiles = Get-ChildItem "G:\Git\table_side" -Filter "_claude_temp_*" -File
$tmpFiles | Remove-Item -Force
$remaining = Get-ChildItem "G:\Git\table_side" -Filter "_claude_temp_*" -File
if ($remaining) {
    Write-Host "WARNING: 以下临时文件未能清理: $($remaining.FullName)"
} else {
    Write-Host "临时文件清理完毕"
}
```

```bash
# Bash 版本
rm -f /g/Git/table_side/_claude_temp_*
remaining=$(ls /g/Git/table_side/_claude_temp_* 2>/dev/null)
if [ -n "$remaining" ]; then echo "WARNING: 未清理: $remaining"; else echo "临时文件清理完毕"; fi
```

**在任务收尾的 TodoWrite checklist 中，必须包含这一条**，并且在执行后确认输出为"临时文件清理完毕"才能标记完成。

---

## CRITICAL: 格式转换后必须验证第一行数据未落入注释行

**LESSON LEARNED（2026-04-28）**: table_tool 将 OLDEST 格式（1行表头）误判为 LEGACY（2行表头）时，第一条数据会被放入 Row3（注释行位置），导致该行被 xresloader 静默跳过，**转表不报错但数据丢失**。

**触发条件**：OLDEST 格式（原始1行表头），且 Row2（第一条数据行）含有字符串值（如枚举值 `KEYBOARD_BUTTON_NONE`、中文说明 `未设置` 等），工具误判该行为注释，从而将其保留在 Row3。

**每次执行 format conversion 后，必须执行此检查**：

```python
import openpyxl
wb = openpyxl.load_workbook('excel/YourFile.xlsx', data_only=True)
ws = wb['YourSheet']
row3 = [ws.cell(3, c).value for c in range(1, ws.max_column + 1)]
# ✅ 正常：Row3 全为 None（空注释行）
# ❌ 异常：Row3 第一列是数字（如 1），说明 ID=1 数据行错误落入注释行！
print('Row3:', row3)
```

发现异常时的修复方法见 `references/format-conversion.md` 的 **Step 5: Post-Conversion Check — OLDEST 格式误判** 章节。

---

## CRITICAL: 在最右侧新增字段后，必须验证 `<dimension>` 已扩到新列

**LESSON LEARNED（2026-06-11）**: 给 Excel 最右侧新增字段时，`update_cell()` 可能已经把 `U1/U2/U3/U4` 等单元格写进 XML，但 worksheet 的 `<dimension ref="A1:T39">` 仍停留在旧范围。此时：
- Excel / `openpyxl` 普通模式可能看起来一切正常
- **ugit 外部预览、部分只读解析器、依赖 `<dimension>` 的工具会看不到新列**

**触发场景：**
- 在现有最后一列右边新增字段（如 `T` 后新增 `U`）
- 用 `XlsxWriter.update_cell()` 逐个写入表头，但没有再做额外结构校验

**新增字段后必须执行这组校验：**
1. 校验新列表头 4 行是否正确（字段名 / 类型 / 注释 / 导出目标）
2. 校验左侧相邻旧列未被污染
3. **校验 worksheet XML 的 `<dimension ref="...">` 已覆盖到新列字母**
4. 若 `<dimension>` 仍是旧列范围，需显式修复后再结束任务

**推荐校验命令（权威，以压缩包内 XML 为准；按 sheet 名定位，不要硬编码 `sheet1.xml`）**：
```bash
python -c "
import zipfile, xml.etree.ElementTree as ET
sheet_name = 'Main'
ns_main = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
ns_rel = {'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
ns_pkg = {'p': 'http://schemas.openxmlformats.org/package/2006/relationships'}
with zipfile.ZipFile('excel/YourFile.xlsx', 'r') as z:
    workbook = ET.parse(z.open('xl/workbook.xml')).getroot()
    rels = ET.parse(z.open('xl/_rels/workbook.xml.rels')).getroot()
    rid = None
    for sheet in workbook.findall('a:sheets/a:sheet', ns_main):
        if sheet.get('name') == sheet_name:
            rid = sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            break
    target = None
    for rel in rels.findall('p:Relationship', ns_pkg):
        if rel.get('Id') == rid:
            target = rel.get('Target')
            break
    with z.open('xl/' + target.lstrip('/')) as f:
        root = ET.parse(f).getroot()
        dim = root.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}dimension')
        print(sheet_name, 'dimension ref:', dim.get('ref'))
"
```

**判定标准：**
- ✅ 预期新增到 `U` 列时，应看到 `A1:U...`
- ❌ 若仍是 `A1:T...`，说明外部预览工具仍可能看不到新字段

**注意：**
- 不要只用 `openpyxl.load_workbook(..., data_only=True)` 的普通模式做验证；它可能重算维度，导致你误以为底层 XML 已修好
- 这个检查对“新增行”与“新增列”都重要，但**新增最右列**时最容易漏掉

---

## 故障排查 (Troubleshooting)

### 问题 1: 命令行无输出静默退出 / 挂起

**两种失败模式（需区分诊断）：**

| 模式 | 症状 | 含义 |
|------|------|------|
| **静默退出** | 命令立即退出，无任何输出，exit code 0 | CLI 内部提前 return，**未实际执行迁移** |
| **挂起** | 命令长时间无响应，进程不退出 | Excel COM 接口阻塞 |

**⚠️ 静默退出 ≠ 成功。** 应通过验证实际数据来确认迁移是否生效，而不是只看命令是否正常退出。

**通用诊断步骤**:
```bash
# 0. 首先检查：是否缺少 --sheet 参数？
#    CLI 默认操作 Main sheet；如果目标字段在非 Main sheet，CLI 可能静默退出（无报错）
#    解决方法: 明确指定 --sheet 参数

# ❌ 可能静默退出（找不到非 Main sheet 的字段）
python table_tool/table_tool.py migrate-text excel/File.xlsx --field ThirdTabTextual

# ✅ 明确指定 sheet
python table_tool/table_tool.py migrate-text excel/File.xlsx --sheet GameTacticsOption --field ThirdTabTextual

# 1. 检查是否有残留 Excel 进程（两种模式的共同原因）
python -c "import xlwings as xw; print(f'Active apps: {len(xw.apps)}')"
tasklist | findstr /i EXCEL

# 2. 清理残留进程
taskkill /F /IM EXCEL.EXE

# 3. 清理残留锁定文件
dir excel | findstr "~$"

# 4. 使用绝对路径重试（避免中文路径编码问题）
python table_tool/table_tool.py migrate-text G:/Git/.../excel/File.xlsx --field FieldName

# 5. 如果仍失败 → 改用手动回退脚本
```

### 问题 2: ImportError / AttributeError

**症状**: 导入或调用方法时报错，例如：
```
ImportError: cannot import name 'XmlConfigUpdater'
AttributeError: 'XMLConfigUpdater' object has no attribute '_get_data_start_row_from_xml'
```

**原因**: 代码实现中的类名拼写错误或调用了不存在的方法

**解决方法**: 检查 `table_tool/table_toolkit/operations/*.py` 文件中的类名和方法定义，确保导入和调用正确。

**常见类名**:
- `XMLConfigUpdater` (不是 `XmlConfigUpdater`)
- `TextMigration`, `FormatConverter`, `ProtoGenerator`

### 问题 3: Windows 中文路径编码问题

**症状**: 在 Git Bash 中运行时出现编码错误，例如：
```
FileNotFoundError: [Errno 2]: No such file or directory: '...\\excel\\S赛事模式_TacticsSettings.xlsx'
```

**原因**: Git Bash 对中文路径的处理与 Python 内部编码不一致

**解决方法**:
```bash
# 使用 Python 原生绝对路径（正斜杠而非反斜杠）
python -c "import openpyxl; wb = openpyxl.load_workbook('G:/Git/.../excel/文件.xlsx')"

# 或使用 Python 内联命令而非 Bash 调用
python table_tool/table_tool.py migrate-text G:/Git/.../excel/文件.xlsx --field FieldName
```

---

## 🔔 任务结束时：报告 xlwings 兜底场景

**每次任务完成后，如果本次操作中有任何步骤回退到了 xlwings（而非 XlsxWriter / table_tool），必须在任务总结末尾附上：**

```
⚠️ XlsxWriter 未支持场景（供后续迭代参考）：
- 场景：{具体操作描述，例如 "autofit 列宽" / "写入数据验证规则" / "复制 sheet"}
- 位置：{文件名 + 方法名 / 步骤}
- 当前方案：xlwings {具体 API}
- 建议：可考虑在 XlsxWriter 中新增 {方法名} 方法
```

如果本次操作全程使用了 table_tool 或 XlsxWriter，则无需附加此说明（静默即可）。
