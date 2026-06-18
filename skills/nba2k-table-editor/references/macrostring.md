# Adding MacroString Texts

> ⚠️ **此文档已过时**
>
> MacroString 的添加流程已变更，**不再需要修改 Excel 或 proto 文件**。
>
> 请改用独立技能 **`nba2k-macrostring`**，该技能记录了当前唯一正确的流程：只向 `{Client\OL3根目录}\ResRoot\Editor\MacroTable.conf` 追加 JSON 条目。遇到 MacroString 需求时，直接调用 `/nba2k-macrostring`。
>
> 以下内容仅供历史参考，**不要按此执行**。

Add new macrostring text configurations for NBA2kOL3.

## 🚨 CRITICAL: READ THIS ENTIRE DOCUMENT BEFORE STARTING

**DO NOT begin work until you have:**
1. ✅ Read this complete document from start to finish
2. ✅ Created a TodoWrite checklist with ALL 6 steps below
3. ✅ Confirmed you understand each step

**Incomplete execution is NOT ACCEPTABLE. ALL 6 steps MUST be completed.**

---

## Overview

Macrostrings are localized text strings used throughout the game UI. They are stored in `ID2StringMapTable.xlsx` and referenced by enum values in the proto files.

## 📌 TodoWrite Template (Copy This)

**Create your TodoWrite checklist with these EXACT items:**

```
TodoWrite([
  {"content": "Step 1: 确定新内容和命名规范", "status": "pending", "activeForm": "确定新内容和命名规范"},
  {"content": "Step 2: 查找已有 Key 风格和最大枚举值", "status": "pending", "activeForm": "查找已有 Key 风格和最大枚举值"},
  {"content": "Step 3: 添加数据到 Excel", "status": "pending", "activeForm": "添加数据到 Excel"},
  {"content": "Step 4: 在 proto 中添加枚举定义 ⚠️ CRITICAL", "status": "pending", "activeForm": "在 proto 中添加枚举定义"},
  {"content": "Step 5: 验证 Excel 和 Proto 的一致性", "status": "pending", "activeForm": "验证 Excel 和 Proto 的一致性"},
  {"content": "Step 6: 文档记录和最终总结", "status": "pending", "activeForm": "文档记录和最终总结"}
])
```

---

## 📋 COMPLETE WORKFLOW (6 Steps - ALL MANDATORY)

### ✅ Step 1: Determine New Content

**TodoWrite Item:** `"Step 1: 确定新内容和命名规范"`

#### 1.1 Collect Requirements

Before adding macrostrings, gather:
- Text content (Chinese, English)
- Category (OL3)
- Usage description
- Whether it contains dynamic parameters (e.g., `{0}`, `{1}`)

### 1.2 Naming Convention

**Core Rule:**
**All new macrostring keys must include the `OL3` identifier to avoid conflicts with NBA Allstar legacy code keys.**

Follow existing naming styles:
- Base format: `ID_STRING_{MODULE}_{CATEGORY}_{NAME}`
- **Mandatory rule:** OL3-related text must contain `_OL3_` segment
- OL3 common text: `ID_STRING_OL3_COMMON_{NAME}`
- Format strings with parameters: `_FORMAT` suffix
- Title/Label types: `_TITLE` suffix

**Naming Examples:**
```
ID_STRING_OL3_COMMON_PLAYER_POSITION_POINTGUARD    // OL3 Common-Player-Position-PG
ID_STRING_OL3_COMMON_PLAYER_GRADE_STAR_FORMAT      // OL3 Common-Player-Grade/Star Format (with {0}{1} params)
ID_STRING_OL3_COMMON_PLAYER_LEVEL_TITLE            // OL3 Common-Player-Level Title
ID_STRING_OL3_LINEUP_ROTATION_SAVE_SUCCESS_TOAST   // Toast 飘字：轮换设置保存成功！
```

**Naming Checklist:**
- [ ] Contains `_OL3_` identifier
- [ ] Follows existing naming pattern
- [ ] Correct suffix (`_FORMAT`, `_TITLE`, `_TOAST`, etc.)
- [ ] **If toast/飘字**: Key MUST end with `_TOAST` suffix

## Step 2: Find Existing Key Style

**TodoWrite Item:** `"Step 2: 查找已有 Key 风格和最大枚举值"`

**Completion Criteria:**
- ✅ Found the maximum enum value in `res_client_enum.proto`
- ✅ Identified the naming pattern for similar keys
- ✅ Confirmed next available enum value (max + 1)

### 2.1 Search for Related Existing Keys

```bash
cd excel
python -c "
import openpyxl
wb = openpyxl.load_workbook('ID2StringMapTable.xlsx')
sheet = wb.sheets['MacroString']
# Search for keys containing specific keywords
for row in range(5, sheet.max_row + 1):
    key = sheet.cell(row, 1).value
    if key and 'KEYWORD' in str(key).upper():
        print(f'{key}: {sheet.cell(row, 2).value}')
"
```

### 2.2 Find Maximum Enum Value

```bash
cd converter/resource/desc/client
grep "ID_STRING_OL3_.*= \d+;" res_client_enum.proto | tail -5
```

This ensures proper enum value continuity.

## Step 3: Add Data to Excel

**TodoWrite Item:** `"Step 3: 添加数据到 Excel"`

**Completion Criteria:**
- ✅ Data added to `excel/ID2StringMapTable.xlsx` MacroString sheet
- ✅ Used xlwings (not openpyxl/pandas)
- ✅ Key name matches proto naming convention
- ✅ Both Chinese and English text added
- ✅ File saved successfully

### 3.1 Data Structure

MacroString sheet uses 4-row header format, data starts from row 5:

| Row | Col A | Col B | Col C |
|-----|-------|-------|-------|
| 1 | Id@ID2StringMacroKey | SystemLanguageCn | SystemLanguageEn |
| 2 | string | string | string |
| 3 | Key | Chinese-Simplified | English-System |
| 4 | PrimaryKey | Client | Client |
| 5+ | {enum name} | {Chinese content} | {English content} |

### 3.2 Add Data (using xlwings)

```python
import xlwings as xw

app = xw.App(visible=False)
app.display_alerts = False
app.screen_updating = False

try:
    wb = app.books.open('excel/ID2StringMapTable.xlsx')
    sheet = wb.sheets['MacroString']

    # Get last row
    last_row = sheet.used_range.last_cell.row

    # Add new data
    sheet.range(f'A{last_row + 1}').value = 'ID_STRING_OL3_COMMON_PLAYER_LEVEL_TITLE'
    sheet.range(f'B{last_row + 1}').value = '等级'
    sheet.range(f'C{last_row + 1}').value = 'Level'

    wb.save()
    wb.close()

    print('Data added successfully')

finally:
    app.quit()  # CRITICAL: Ensures Excel process exits
```

**Important:** Must use xlwings, not openpyxl/pandas, to preserve Excel formatting and formulas.

## Step 4: Add Enum in Proto

**TodoWrite Item:** `"Step 4: 在 proto 中添加枚举定义"`

**⚠️ CRITICAL STEP - DO NOT SKIP THIS**

**Completion Criteria:**
- ✅ Read `converter/resource/desc/client/res_client_enum.proto`
- ✅ Found the last enum entry in `ID2StringMacroKey`
- ✅ Added new enum with value = (max enum value + 1)
- ✅ Enum name EXACTLY matches Excel Key name
- ✅ Added Chinese comment after `//`
- ✅ File saved successfully

### 4.1 File Location

`converter/resource/desc/client/res_client_enum.proto`

**Note:** Server-side proto files do not contain `ID2StringMacroKey` enum, no synchronization needed for server files.

### 4.2 Enum Structure

```protobuf
enum ID2StringMacroKey //ID2String类型
{
    ID_STRING_NONE = 0;
    ...
    ID_STRING_OL3_COMMON_PLAYER_LEVEL_TITLE = 101356; // 等级
}
```

### 4.3 Assign Enum Value

- Add 1 to the existing maximum enum value
- Keep values continuous
- Format: `KEY_NAME = enum_value; // comment`

## Step 5: Verification

**TodoWrite Item:** `"Step 5: 验证 Excel 和 Proto 的一致性"`

**Completion Criteria:**
- ✅ Verified Excel data is correct
- ✅ Verified Proto enum is correct
- ✅ Confirmed Key names match EXACTLY between Excel and Proto
- ✅ Confirmed enum value is sequential (no gaps)

### 5.1 Verify Excel Data

```python
import openpyxl
wb = openpyxl.load_workbook('excel/ID2StringMapTable.xlsx')
sheet = wb.sheets['MacroString']
# Check added entry
for row in range(5, sheet.max_row + 1):
    key = sheet.cell(row, 1).value
    if key == 'KeyToVerify':
        print(f'Key: {key}')
        print(f'Chinese: {sheet.cell(row, 2).value}')
        print(f'English: {sheet.cell(row, 3).value}')
```

### 5.2 Verify Proto Enum

```bash
grep "NewKeyName" converter/resource/desc/client/res_client_enum.proto
```

### 5.3 Optional: Run Conversion to Validate

```bash
cd converter
convert.bat  # Windows
# or
bash convert.sh  # Linux/macOS
```

## Step 6: Documentation

**TodoWrite Item:** `"Step 6: 文档记录和最终总结"`

**Completion Criteria:**
- ✅ Created summary table with all information
- ✅ Documented usage example
- ✅ Provided next steps for client integration
- ✅ Confirmed ALL previous steps are completed

Record the added macrostring:

| Key | Chinese | English | Enum Value | Usage |
|-----|---------|---------|------------|-------|
| ... | ... | ... | ... | ... |

## Common Naming Suffixes

| Suffix | Meaning | Example |
|--------|---------|---------|
| `_POSITION` | Position | `PLAYER_POSITION_POINTGUARD` |
| `_GRADE` | Breakthrough level | `PLAYER_GRADE_FORMAT` |
| `_STAR` | Breakthrough star | `PLAYER_STAR_FORMAT` |
| `_LEVEL` | Level | `PLAYER_LEVEL_FORMAT` |
| `_TITLE` | Title | `PLAYER_LEVEL_TITLE` |
| `_FORMAT` | Format string (with params) | `GRADE_STAR_FORMAT` |
| `_BTN` | Button text | `COMMON_BTN_CONFIRM` |
| `_TOAST` | **Toast 飘字提示（必须使用）** | `ROTATION_SAVE_SUCCESS_TOAST` |
| `_CONFIRM` | 确认弹窗文本 | `DELETE_CONFIRM` |

## Complete Workflow Example

Adding player position labels:

```bash
# Step 1: Search existing position keys
cd excel
python -c "
import openpyxl
wb = openpyxl.load_workbook('ID2StringMapTable.xlsx')
sheet = wb.sheets['MacroString']
for row in range(5, sheet.max_row + 1):
    key = sheet.cell(row, 1).value
    if key and 'POSITION' in str(key).upper():
        print(f'{key}')
"

# Step 2: Find max OL3 enum value
cd converter/resource/desc/client
grep "ID_STRING_OL3_.*= \d+;" res_client_enum.proto | tail -1

# Step 3: Add data to Excel (using xlwings script)
# ... run the Python script ...

# Step 4: Add enum to proto
# ... edit res_client_enum.proto ...

# Step 5: Verify
cd converter
convert.bat
```

## Notes for MacroString

1. **Excel tool choice:** Always use xlwings for Excel operations, avoid openpyxl/pandas that may break formatting
2. **OL3 identifier:** All new macrostring keys must contain `OL3` identifier
3. **Toast suffix:** Toast 飘字类文本的 Key 必须以 `_TOAST` 结尾，例如 `ID_STRING_OL3_LINEUP_ROTATION_SAVE_SUCCESS_TOAST`
4. **Enum value continuity:** Keep enum values continuous and incremental
4. **Naming consistency:** Follow existing naming patterns and structure
5. **Parameter placeholders:** Strings containing `{0}`, `{1}` parameters should use `_FORMAT` suffix
6. **Key consistency:** The enum name in proto must exactly match the key in Excel column A (case-sensitive). Mismatched names will cause conversion errors.
7. **Server sync:** No need to sync to server proto files - `ID2StringMacroKey` enum only exists in client-sideproto.
8. **Excel instance cleanup:** Before new xlwings operations, clean up any residual Excel instances to avoid file lock issues:
   ```bash
   taskkill /F /IM EXCEL.EXE  # Windows, force close all Excel processes
   ```
   Or use context managers (`with xw.App(...)`) for automatic cleanup. This prevents "read-only" errors caused by residual processes holding file locks.

---

## 📝 MANDATORY EXECUTION CHECKLIST

**Before reporting task completion, verify ALL items below:**

### Pre-Execution
- [ ] Read this complete document from start to finish
- [ ] Created TodoWrite with ALL 6 steps
- [ ] Understood the requirements and naming convention

### Step 1: Determine New Content
- [ ] Collected Chinese and English text
- [ ] Determined category (OL3)
- [ ] Generated Key name following naming convention
- [ ] Key contains `_OL3_` identifier
- [ ] **If toast/飘字: Key ends with `_TOAST` suffix**
- [ ] Key has appropriate suffix (`_FORMAT`, `_TITLE`, `_TOAST`, `_CONFIRM`, etc.)

### Step 2: Find Existing Key Style
- [ ] Found maximum enum value in res_client_enum.proto
- [ ] Identified naming pattern for similar keys
- [ ] Determined next available enum value (max + 1)

### Step 3: Add Data to Excel
- [ ] Opened excel/ID2StringMapTable.xlsx MacroString sheet
- [ ] Used xlwings (not openpyxl/pandas)
- [ ] Added Key in Column A
- [ ] Added Chinese text in Column B
- [ ] Added English text in Column C
- [ ] Saved file successfully

### Step 4: Add Enum in Proto ⚠️ CRITICAL
- [ ] Read converter/resource/desc/client/res_client_enum.proto
- [ ] Located ID2StringMacroKey enum
- [ ] Found last enum entry
- [ ] Added new enum entry with correct value
- [ ] Enum name EXACTLY matches Excel Key
- [ ] Added Chinese comment
- [ ] Saved file successfully

### Step 5: Verification
- [ ] Verified Excel data is correct
- [ ] Verified Proto enum is correct
- [ ] Confirmed Key names match between Excel and Proto
- [ ] Confirmed enum value is sequential

### Step 6: Documentation
- [ ] Created summary table
- [ ] Provided usage example
- [ ] Listed next steps for client integration
- [ ] Marked all TodoWrite items as completed

**IF ANY CHECKBOX IS UNCHECKED, THE TASK IS NOT COMPLETE.**

---

## 🚨 COMMON MISTAKES TO AVOID

1. ❌ **Skipping Step 4 (Proto enum)** → Client compilation will fail
2. ❌ **Key name mismatch between Excel and Proto** → Conversion will fail
3. ❌ **Forgetting `_OL3_` identifier** → Conflicts with legacy code
4. ❌ **Toast/飘字 without `_TOAST` suffix** → Naming inconsistency, hard to identify text type
5. ❌ **Using openpyxl instead of xlwings** → Formula loss
6. ❌ **Non-sequential enum values** → Breaks enum continuity
7. ❌ **Not verifying before declaring complete** → Incomplete work
