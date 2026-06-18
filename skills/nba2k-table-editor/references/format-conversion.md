# Format Conversion

Convert Legacy (2-row header) Excel files to NBA2kOL3 standard (4-row header) format.

## Legacy vs NBA2kOL3 Format

### Legacy Format (Old NBA Allstar standard)
- 2-row header (Row 1: Field names, Row 2: Comments)
- Data starts from **row 3**
- No type information or export target specification
- Used by older tables from the NBA Allstar codebase

### NBA2kOL3 Format (Standard)
- 4-row header
- Data starts from **row 5**
- Full type and export control
- Standard for all new tables

| Row | Purpose |
|-----|---------|
| 1   | Field names (must match proto message field names) |
| 2   | Field types (uint32, int32, string, etc.) |
| 3   | Designer comments/descriptions |
| 4   | Export target specification |
| 5+  | Data |

## Commands

### Convert All Sheets

```bash
# Convert all sheets in a file
python table_tool/table_tool.py convert excel/YourFile.xlsx --all-sheets --update-xml

# Preview changes without modifying (dry-run)
python table_tool/table_tool.py convert excel/YourFile.xlsx --all-sheets --dry-run
```

### Convert Specific Sheets

```bash
# Convert only Sheet1 and Sheet2
python table_tool/table_tool.py convert excel/YourFile.xlsx --sheet Sheet1 --sheet Sheet2

# Convert with XML update
python table_tool/table_tool.py convert excel/YourFile.xlsx --sheet Sheet1 --sheet Sheet2 --update-xml
```

### Command Options

| Option | Description |
|--------|-------------|
| `--all-sheets` | Convert all sheets in the workbook |
| `--sheet NAME` | Convert only specified sheet(s) |
| `--update-xml` | Update DataSource start row in XML configs from `|3,1` to `|5,1` |
| `--dry-run` | Preview changes without writing to files |

## Row 4 Export Targets

- `PrimaryKey`: Primary key field, exported to both client and server
- `Client`: Export to client only
- `Server`: Export to server only
- Empty: Export to both client and server
- `Skip`: Not exported (designer helper columns)

### Export Target Auto-Detection

The conversion tool automatically determines export targets by comparing field availability across client and server proto definitions:

**Field Name Extraction:**
- Enum fields: `BadgeName@PlayerBadges` → extracts `BadgeName`
- Array fields: `UnlockCondition[0]` → extracts `UnlockCondition`
- Nested array fields: `UnlockCondition[0].Method` → extracts `UnlockCondition`
- Combined: `BadgeName[0]@PlayerBadges` → extracts `BadgeName`

**Export Target Rules:**
- Columns with names containing "备注", "注", or "公式" → `Skip`
- Field matching XML `<indexer>` value → `PrimaryKey` (if no indexer, defaults to first column)
- Field exists only in client proto → `Client`
- Field exists only in server proto → `Server`
- Field exists in both protos → Empty (export to both)
- Field exists in **neither** proto → `Skip`

### Repeated Field Support

The tool correctly handles xresloader array syntax for `repeated` proto fields:

**Simple repeated types:**
```protobuf
repeated uint32 WinStreak = 9;
```
Excel columns: `WinStreak[0]`, `WinStreak[1]`, `WinStreak[2]`, etc.

**Repeated message types:**
```protobuf
message BadgeUnlock {
  repeated BadgeUnlockCondition UnlockCondition = 4;
}

message BadgeUnlockCondition {
  string Method = 1;
  string Key = 2;
  string Value = 3;
}
```
Excel columns: `UnlockCondition[0].Method`, `UnlockCondition[0].Key`, `UnlockCondition[0].Value`, `UnlockCondition[1].Method`, etc.

All array syntax fields are correctly matched to their parent proto field for export target determination.

## What the Tool Does

When converting Legacy format to NBA2kOL3 format:

1. Detects current format (2-row vs 4-row header)
2. Inserts Row 2 (types) and Row 4 (export targets) while preserving Row 2 comments as Row 3
3. Auto-infers types from proto definitions or naming conventions:
   - `Ranking*` → uint32
   - `*Ability` → uint32
   - `*Id` → uint32
4. Determines export targets by comparing client/server proto field definitions
5. Sets PrimaryKey based on XML `<indexer>` tag
6. Marks columns with "备注"/"注"/"公式" as `Skip`
7. Updates all matching `DataSource` entries in `convert*.xml` files from `|3,1` to `|5,1`
8. Uses xlwings in background mode to preserve all Excel formulas and formatting

## Complete Workflow

### Interactive Format Conversion (Skill-based)

When using the `/nba2k-table-editor` skill, follow this workflow:

**Step 1: Preview Conversion**
```bash
python table_tool/table_tool.py convert excel/YourFile.xlsx --sheet YourSheet --dry-run
```
- Detect current format and enum field suggestions
- Capture output for parsing

**Step 2: Parse Enum Suggestions (if detected)**

If the output contains "检测到 X 个枚举字段建议添加@符号", extract the suggestions:

```python
# Import from table_toolkit.utils
from doc.table_toolkit.utils import parse_enum_suggestions, format_suggestions_for_display

# Parse dry-run output
suggestions = parse_enum_suggestions(dry_run_output)

if suggestions:
    # Format for display
    display_text = format_suggestions_for_display(suggestions)
    # Use AskUserQuestion to ask user
```

**Step 3: Ask User (via AskUserQuestion tool)**

When enum fields are detected, ask:
- **Question**: "检测到以下枚举字段可以添加 @ 符号以明确指定枚举类型，是否自动重命名？\n\n{display_text}"
- **Header**: "Enum Rename"
- **Options**:
  - Label: "是，自动重命名 (推荐)"
    Description: "将枚举字段重命名为 Field@EnumType 格式，提高代码可读性"
  - Label: "否，保持当前字段名"
    Description: "保持字段名不变，但会在 Row 2 标记为 enum 类型"

**Step 4: Execute Conversion**

Based on user choice:
```bash
# If user chose "Yes"
python table_tool/table_tool.py convert excel/YourFile.xlsx --sheet YourSheet --update-xml --auto-rename-enum

# If user chose "No"
python table_tool/table_tool.py convert excel/YourFile.xlsx --sheet YourSheet --update-xml
```

**Step 5: Post-Conversion Check — PrimaryKey Column Correctness**

After conversion, **always verify** that the `PrimaryKey` column in Row 4 is correct.

The tool defaults to setting the **first column** as `PrimaryKey` (unless the XML `<indexer>` tag specifies otherwise). However, some legacy tables have a **dummy/unused first column** (e.g., a `BackUp` or remark column) that was never part of the proto, and the **actual primary key is in the second column**.

**How to detect this situation:**
- Row 4 result looks like: `['PrimaryKey', 'Server', 'Server', ...]`
- But Row 4, column 1 field (e.g., `BackUp`) is **absent from all proto definitions** (client/server/gamelib)
- The actual ID field (e.g., `Id`) is in column 2

**Fix with xlwings:**
```python
import xlwings as xw

app = xw.App(visible=False)
app.display_alerts = False
app.screen_updating = False

try:
    wb = app.books.open('excel/YourFile.xlsx')
    sheet = wb.sheets['Main']
    sheet.range('A4').value = 'Skip'      # Dummy first column → Skip
    sheet.range('B4').value = 'PrimaryKey'  # Actual ID column → PrimaryKey
    wb.save()
    wb.close()
finally:
    app.quit()
```

**Verification:**
```python
import openpyxl
wb = openpyxl.load_workbook('excel/YourFile.xlsx', data_only=True)
sheet = wb['Main']
row4 = [sheet.cell(4, col).value for col in range(1, 8)]
print(f'Row 4: {row4}')
wb.close()
# Expected: ['Skip', 'PrimaryKey', 'Server', ...]
```

**Step 6: Verify Results**
- Check Excel file structure
- Confirm enum fields handled correctly
- Verify XML configs updated (DataSource start row)

### Manual CLI Workflow

```bash
# Step 1: Preview what will be changed
python table_tool/table_tool.py convert excel/OldTable.xlsx --all-sheets --update-xml --dry-run

# Step 2: Check for enum field suggestions in output
# If you see "检测到 X 个枚举字段建议添加@符号", decide whether to use --auto-rename-enum

# Step 3a: Execute conversion WITHOUT auto-rename
python table_tool/table_tool.py convert excel/OldTable.xlsx --all-sheets --update-xml

# Step 3b: Execute conversion WITH auto-rename
python table_tool/table_tool.py convert excel/OldTable.xlsx --all-sheets --update-xml --auto-rename-enum

# Step 4: Verify the converted table structure
# (Check the Excel file manually)

# Step 5: Test the conversion
cd converter
convert.bat  # On Windows
# or
bash convert.sh  # On Linux/macOS
```

## Notes

- Always use xlwings for Excel programmatic access to preserve formulas
- Generated binary files are in .gitignore
- Excel temp files (`~$*.xlsx`) should not be committed
