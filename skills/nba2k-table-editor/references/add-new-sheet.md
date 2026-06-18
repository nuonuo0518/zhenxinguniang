# Adding a New Sheet to Existing Excel File

## When to Use This Workflow

Use this workflow when you need to add a **new configuration sheet** to an **existing Excel file** in the Table repository, rather than creating a completely new Excel file.

**Common scenarios:**
- Adding related configuration tables to an existing file (e.g., adding `PlayerStaminaPlayingTime` to `UserLineupSet.xlsx`)
- Extending a module with additional configuration sheets
- Grouping related tables in one Excel file for better organization

**User request patterns:**
- "为 excel/UserLineupSet.xlsx 增加一个新的 sheet"
- "Add a new configuration sheet to existing table"
- "在现有表格中添加新的配置页"

**If you need to create a completely new Excel file, use the standard "Adding a New Table" workflow instead.**

---

## Quick Start with Table Toolkit API

The easiest way to add a new sheet is using the **TableToolkit.add_new_sheet()** high-level API, which automates the entire workflow:

### Python API Usage

```python
from table_toolkit import TableToolkit

toolkit = TableToolkit()

# Define fields
fields = [
    {'name': 'Id', 'type': 'uint32', 'comment': '唯一ID', 'export_target': 'PrimaryKey'},
    {'name': 'Name', 'type': 'string', 'comment': '名称', 'export_target': 'Server'},
    {'name': 'Value', 'type': 'uint32', 'comment': '数值', 'export_target': 'Server'}
]

# Add new sheet with full pipeline
result = toolkit.add_new_sheet(
    excel_file='excel/UserLineupSet.xlsx',
    sheet_name='NewConfig',
    fields=fields,
    sample_data=[[1, 'test', 100]],  # Optional sample data
    category='Player',
    target='server',
    compile_and_convert=True,  # Automatically compile proto and convert tables
    verbose=True
)

# Check results
if result['binary_verified']:
    print("Success! All steps completed.")
else:
    print(f"Errors: {result['errors']}")
```

### Command Line Usage

```bash
# Via table_tool.py (if CLI wrapper is implemented)
python table_tool/table_tool.py add-sheet excel/UserLineupSet.xlsx NewConfig \
    --fields "Id:uint32:唯一ID:PrimaryKey" \
    --fields "Name:string:名称:Server" \
    --category Player \
    --target server
```

### What This API Does Automatically

The `add_new_sheet()` method orchestrates the complete workflow:

1. ✅ Creates sheet in Excel with 4-row header
2. ✅ Generates proto message definition
3. ✅ Updates XML configuration
4. ✅ Compiles proto files
5. ✅ Converts tables to binary
6. ✅ Verifies generated binary file

**This is the RECOMMENDED approach for adding new sheets.**

---

## Manual Step-by-Step Workflow

If you need more control or the API doesn't meet your needs, follow the manual workflow below.

---

## Complete Workflow

### Step 1: Gather Required Information

Before starting, collect the following information from the user (use AskUserQuestion if not provided):

1. **Target Excel file path** (e.g., `excel/UserLineupSet.xlsx`)
2. **New sheet name** (e.g., `PlayerStaminaPlayingTime`)
3. **Field definitions** - For each field:
   - Field name (English, PascalCase recommended)
   - Field type (uint32, int32, string, float, etc.)
   - Chinese comment/description
   - Export target (PrimaryKey, Client, Server, or empty for both)
4. **Target export** (client, server, or both)
5. **Sample data rows** (optional, for validation)
6. **Category in XML** (Player, Team, Item, etc. - check existing categories in convert_list*.xml)

**If any information is missing, use AskUserQuestion to ask the user.**

---

### Step 2: Validate Excel File Exists

Check that the target Excel file exists:

```bash
ls excel\YourFile.xlsx
```

If the file doesn't exist, ask the user if they want to:
- Create a new Excel file (switch to standard "Adding a New Table" workflow)
- Specify a different existing file

---

### Step 3: Create New Sheet with 4-Row Header

> **优先使用 `XlsxWriter.add_sheet()`** — 无 Excel 进程，同步更新 4 个 XML 文件。  
> 仅当需要 xlwings 特有功能（autofit、数据验证等）时才降级，且需在任务结束时报告未支持场景。

#### 方案 A：XlsxWriter（优先）

```python
from table_tool.table_toolkit.core.xlsx_writer import XlsxWriter

with XlsxWriter('excel/YourFile.xlsx') as writer:
    # 检查 sheet 是否已存在
    if 'NewSheetName' in writer.get_sheet_names():
        raise ValueError("Sheet 'NewSheetName' already exists — delete it first or use a different name")

    # 创建 sheet（同步更新 workbook.xml / rels / Content_Types）
    writer.add_sheet('NewSheetName')

    # 追加所需字符串到 sharedStrings
    field_names = ['FieldName1', 'FieldName2', 'FieldName3']
    field_types = ['uint32', 'string', 'uint32']
    field_comments = ['描述1', '描述2', '描述3']
    export_targets = ['PrimaryKey', 'Server', 'Client']

    all_strings = field_names + field_types + field_comments + export_targets
    idx = writer.append_shared_strings(list(set(all_strings)))

    # Row 1: 字段名
    writer.insert_row_content('NewSheetName', 1, [
        ('A', 's', idx['FieldName1']),
        ('B', 's', idx['FieldName2']),
        ('C', 's', idx['FieldName3']),
    ])
    # Row 2: 类型
    writer.insert_row_content('NewSheetName', 2, [
        ('A', 's', idx['uint32']),
        ('B', 's', idx['string']),
        ('C', 's', idx['uint32']),
    ])
    # Row 3: 注释
    writer.insert_row_content('NewSheetName', 3, [
        ('A', 's', idx['描述1']),
        ('B', 's', idx['描述2']),
        ('C', 's', idx['描述3']),
    ])
    # Row 4: 导出目标
    writer.insert_row_content('NewSheetName', 4, [
        ('A', 's', idx['PrimaryKey']),
        ('B', 's', idx['Server']),
        ('C', 's', idx['Client']),
    ])

    # Row 5+: 示例数据（可选，用数字类型写入）
    sample_data = [[1, 'value1', 100], [2, 'value2', 200]]
    for i, row in enumerate(sample_data):
        writer.insert_row_content('NewSheetName', 5 + i, [
            ('A', 'n', row[0]),
            ('B', 'inlineStr', row[1]),
            ('C', 'n', row[2]),
        ])
    # pack 在 __exit__ 自动执行

print('Sheet created successfully (no Excel process)')
```

#### 方案 B：xlwings 兜底（仅当需要 autofit / 数据验证等时）

> 使用后需在任务结束时报告"未支持场景"（具体未支持的 API）。

```python
import xlwings as xw

app = None
try:
    app = xw.App(visible=False)
    app.display_alerts = False
    app.screen_updating = False

    wb = app.books.open('excel/YourFile.xlsx')

    # Check if sheet already exists
    if 'NewSheetName' in [s.name for s in wb.sheets]:
        wb.sheets['NewSheetName'].delete()

    # Create new sheet
    new_sheet = wb.sheets.add('NewSheetName')

    # Row 1: Field names
    new_sheet.range('A1').value = ['FieldName1', 'FieldName2', 'FieldName3']
    # Row 2: Types
    new_sheet.range('A2').value = ['uint32', 'string', 'uint32']
    # Row 3: Comments
    new_sheet.range('A3').value = ['描述1', '描述2', '描述3']
    # Row 4: Export targets
    new_sheet.range('A4').value = ['PrimaryKey', 'Server', 'Client']

    # Row 5+: Sample data (optional)
    sample_data = [[1, 'value1', 100], [2, 'value2', 200]]
    if sample_data:
        new_sheet.range('A5').value = sample_data

    # autofit 等 XlsxWriter 暂不支持的操作
    new_sheet.range('A:Z').autofit()

    wb.save()
    wb.close()

    print(f'Success: Created sheet {new_sheet.name}')

finally:
    if app:
        try:
            app.quit()
        except:
            pass
```

---

### Step 4: Generate Proto Message Definition

Add the proto message definition to the appropriate proto file based on export target:

**For server-only tables:**
Edit `converter/resource/desc/server/res_server.proto`

**For client-only tables:**
Edit `converter/resource/desc/client/res_client_struct.proto`

**For both client and server:**
Edit both files, or use `res_common.proto` if the structure is identical

**Proto message format:**
```protobuf
message YourMessageName {
    uint32 FieldName1 = 1; // 描述1
    string FieldName2 = 2; // 描述2
    uint32 FieldName3 = 3; // 描述3
}
```

**Key points:**
- Message name should match the sheet name (recommended)
- Field numbers start from 1 and increment sequentially
- Add Chinese comments from Excel Row 3 after each field
- Follow existing naming conventions in the proto file

**Location to insert:**
- Append to the end of the proto file before the closing brace
- Or insert near related message definitions for better organization

> ⚠️ **Server 导出专属：非 `Id` 主键必须在 proto 中追加 `option (primary_key_field)`**
>
> 如果该 sheet 是 server 导出（写入 `convert_list_server.xml`），且 `<indexer>` 中的主键字段名**不是 `Id`**，必须在 proto message 头部加入：
> ```protobuf
> message YourMessageName {
>     option (primary_key_field) = "YourPrimaryKeyField";   // ← 放在所有字段之前
>
>     uint32 YourPrimaryKeyField = 1;
>     // ... 其余字段
> }
> ```
> 详细规则和示例见 [`references/indexer-type-check.md`](indexer-type-check.md) 的"Server 专属规则"章节。

---

### Step 5: Update XML Conversion Configuration

Update the appropriate XML configuration file(s) based on export target:

**For server export:**
Edit `converter/convert_list_server.xml`

**For client export:**
Edit `converter/convert_list.xml`

**For gamelib export:**
Edit `converter/convert_list_gamelib.xml`

**XML item format:**
```xml
<item name="Main_Server" cat="Category" class="server">
    <scheme name="DataSource" desc="数据源">../../excel/YourFile.xlsx|SheetName|5,1</scheme>
    <scheme name="ProtoName" desc="协议名">NBA3.Game.Resource.server.YourMessageName</scheme>
    <scheme name="OutputFile" desc="输出文件名">server/OutputFileName.bin</scheme>
</item>
```

**Key parameters:**
- `cat`: Category (Player, Team, Item, etc. - must match existing categories in XML)
- `class`: Export class (server, client, or gamelib)
- `DataSource`: `../../excel/FileName.xlsx|SheetName|5,1` (5 = data starts at row 5)
- `ProtoName`: Full proto message path with namespace
- `OutputFile`: Output binary file path (server/, client/, or gamelib/)

**Where to insert:**
- Find the appropriate category section (search for `cat="YourCategory"`)
- Insert near related table configurations
- Maintain alphabetical or logical grouping

---

### Step 6: Compile Proto Files

Compile the proto files to generate `.pb` files:

**For server proto:**
```bash
cd converter/protobuf/bin
./protoc.exe -I=../../resource/desc/common -I=../../resource/desc/server \
  ../../resource/desc/server/res_server.proto \
  ../../resource/desc/common/res_common.proto \
  ../../resource/desc/server/component_enum.proto \
  -o ../../resource/desc/res_server.pb
```

**For client proto:**
```bash
cd converter/protobuf/bin
protoc.exe -I=../../resource/desc/client -I=../../resource/desc/common \
  res_client_struct.proto res_client_enum.proto res_common.proto \
  -o ../../resource/desc/res.pb
```

**Check for compilation errors:**
- Syntax errors in proto files
- Missing imports or dependencies
- Field number conflicts

---

### Step 7: Run Table Conversion

Execute the conversion process to generate binary files:

**For server tables:**
```bash
cd converter
python xresconv-cli/xresconv-cli.py convert_list_server.xml --data-version 0
```

**For client tables:**
```bash
cd converter
python xresconv-cli-win/xresconv-cli.py convert_list.xml
```

**For gamelib tables:**
```bash
cd converter
python xresconv-cli-win/xresconv-cli.py convert_list_gamelib.xml
```

**Monitor the output:**
- Look for `[INFO] xresloader - Convert from "../../excel/YourFile.xlsx|SheetName" to "server/OutputFile.bin" success.`
- Check for error messages like:
  - `Field not found in proto message`
  - `Type mismatch`
  - `Excel file not found`
  - `Invalid data format`

---

### Step 8: Verify Generated Binary File

Check that the binary file was successfully generated:

```bash
ls -lh converter/resource/bin/server/OutputFileName.bin
```

**Validation checklist:**
- ✅ File exists
- ✅ File size is reasonable (not 0 bytes)
- ✅ Conversion log shows correct row count
- ✅ No error messages in conversion output

**If the file is missing or empty:**
1. Check proto compilation was successful
2. Verify XML configuration paths are correct
3. Check Excel sheet name matches exactly (case-sensitive)
4. Verify DataSource row number is correct (5,1 for NBA2kOL3 format)
5. Check proto message name matches ProtoName in XML

---

### Step 9: Document and Commit Changes

**Files modified (commit together):**
1. `excel/YourFile.xlsx` - New sheet added
2. `converter/resource/desc/server/res_server.proto` (or client proto)
3. `converter/convert_list_server.xml` (or client/gamelib XML)

**Commit message format:**
```
feat(table): Add NewSheetName configuration to YourFile.xlsx

- Added NewSheetName sheet with X fields
- Export target: server/client/both
- Generated proto message and XML config
- Validated conversion generates OutputFileName.bin
```

**Files NOT to commit (already in .gitignore):**
- `converter/resource/bin/**/*.bin`
- `converter/resource/desc/*.pb`
- `converter/resource/src/**/*`
- `~$*.xlsx` (Excel temp files)

---

## Common Issues and Troubleshooting

### Issue 1: Sheet Already Exists
**Symptom:** `ValueError: Sheet named 'XXX' already present in workbook`

**Solution:**
- Delete the existing sheet first
- Or ask user if they want to overwrite or use a different name

### Issue 2: Proto Compilation Fails
**Symptom:** `Field not found` or syntax errors

**Solution:**
- Check field names in Excel Row 1 match proto message fields exactly (case-sensitive)
- Verify proto syntax (semicolons, braces, field numbers)
- Check imports are correct

### Issue 3: Conversion Produces Empty/Missing Binary
**Symptom:** No .bin file generated or 0 bytes

**Solution:**
- Verify XML DataSource path and sheet name are correct
- Check proto was compiled successfully (.pb file exists)
- Verify ProtoName namespace matches proto package
- Check Excel data starts from Row 5

### Issue 4: Type Mismatch Errors
**Symptom:** `Cannot convert value 'XXX' to type YYY`

**Solution:**
- Check Excel Row 2 types match proto message field types
- Verify data in Row 5+ matches the declared types
- Common issues:
  - String data in numeric fields
  - Missing quotes for string values
  - Invalid enum values

### Issue 5: XML Configuration Not Found
**Symptom:** Conversion skips the new sheet

**Solution:**
- Verify the item was added to the correct XML file
- Check `class` attribute matches the conversion command (server/client/gamelib)
- Verify category exists in `<category>` section
- Check XML syntax (closing tags, quotes)

---

## Example: Adding PlayerStaminaPlayingTime to UserLineupSet.xlsx

### Input Information:
- Target file: `excel/UserLineupSet.xlsx`
- Sheet name: `PlayerStaminaPlayingTime`
- Fields:
  - `Stamina` (uint32, 球员体力上限值, PrimaryKey)
  - `RecommendedMinutes` (uint32, 建议上场分钟, Server)
  - `RecommendedQuarters` (uint32, 建议上场节数(只支持2和3), Server)
- Export target: Server only
- Category: Player

### Step-by-step execution:

1. **Create sheet in Excel** ✅
2. **Add proto message to `res_server.proto`:**
   ```protobuf
   message PlayerStaminaPlayingTime {
       uint32 Stamina = 1; // 球员体力上限值
       uint32 RecommendedMinutes = 2; // 建议上场分钟
       uint32 RecommendedQuarters = 3; // 建议上场节数(只支持2和3)
   }
   ```
3. **Update `convert_list_server.xml`:**
   ```xml
   <item name="Main_Server" cat="Player" class="server">
       <scheme name="DataSource">../../excel/UserLineupSet.xlsx|PlayerStaminaPlayingTime|5,1</scheme>
       <scheme name="ProtoName">NBA3.Game.Resource.server.PlayerStaminaPlayingTime</scheme>
       <scheme name="OutputFile">server/PlayerStaminaPlayingTime.bin</scheme>
   </item>
   ```
4. **Compile proto** ✅
5. **Run conversion** ✅
6. **Verify output:** `server/PlayerStaminaPlayingTime.bin` (272 bytes, 9 rows)

---

## Summary Checklist

Before completing this workflow, verify ALL steps:

- [ ] New sheet created in Excel file with 4-row header
- [ ] Sample data rows added (optional but recommended)
- [ ] Proto message added to appropriate proto file with Chinese comments
- [ ] **（Server 导出 + 非 `Id` 主键）** proto message 头部有 `option (primary_key_field) = "字段名";`，且与 XML `<indexer>` 字段名完全一致
- [ ] XML configuration added to appropriate convert_list*.xml file
- [ ] Proto files compiled successfully (.pb files generated)
- [ ] Table conversion executed without errors
- [ ] Binary output file exists and has reasonable size
- [ ] Conversion log shows correct row count
- [ ] All modified files staged for commit (Excel, proto, XML only)

**Only declare the task complete when ALL checklist items are verified.**
