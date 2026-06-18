# Proto Generation

Generate Protocol Buffer message definitions based on Excel table structure.

## Overview

The proto generation tool reads Excel files and creates corresponding proto message definitions for server and client use.

## Commands

### Generate Server Proto

```bash
# Generate server proto for all sheets
python table_tool/table_tool.py generate excel/YourFile.xlsx --target server

# Preview before generating
python table_tool/table_tool.py generate excel/YourFile.xlsx --target server --dry-run
```

### Generate Client Proto

```bash
# Generate client proto for all sheets
python table_tool/table_tool.py generate excel/YourFile.xlsx --target client

# Generate for specific sheet only
python table_tool/table_tool.py generate excel/YourFile.xlsx --sheet Sheet1 --target client

# Preview before generating
python table_tool/table_tool.py generate excel/YourFile.xlsx --target client --dry-run
```

### Command Options

| Option | Description |
|--------|-------------|
| `--target {server|client}` | Target proto generation destination |
| `--sheet NAME` | Generate proto for specific sheet only |
| `--dry-run` | Preview proto output without writing files |

## Type Inference

Field types are determined by priority:

1. **Excel Row 2** (explicit type, highest priority)
2. **Proto definition** (if message already exists)
3. **Field name pattern**:
   - `Ranking*` → uint32
   - `*Ability` → uint32
   - `*Id` → uint32
   - `*Count` → uint32
   - `*Time` → uint32
4. **Default**: string

### Supported Types

| Type | Description |
|------|-------------|
| `uint32` | Unsigned 32-bit integer |
| `int32` | Signed 32-bit integer |
| `uint64` | Unsigned 64-bit integer |
| `int64` | Signed 64-bit integer |
| `float` | 32-bit floating point |
| `double` | 64-bit floating point |
| `bool` | Boolean |
| `string` | String |

### Enum Types

For enum type fields:
- Use `FieldName@EnumType` syntax in Row 1
- Specify `enum` in Row 2

Example:
```
| Position@PlayerPosition | Rank@RankingType |
| enum                     | uint32            |
| 球员位置                  | 排名类型         |
```

## Generated Proto Structure

### Generated Message Example

```protobuf
message YourTable {
    uint32 Id = 1;
    uint32 Field1 = 2;
    string Field2 = 3;
    repeated uint32 FieldList = 4;
    PlayerPosition Position = 5;  // Enum field
}
```

### Server 导出：非 `Id` 主键的额外声明

> **仅 server 类型（写 `convert_list_server.xml`）且主键字段名不是 `Id` 时才需要。**

server 框架默认只识别名为 `Id` 的主键。当 `<indexer>` 中声明的是其他字段名时，必须在 proto message **头部**（所有字段行之前）加入 `option (primary_key_field)`，否则 server 无法正确定位主键：

```protobuf
message PlayerScore {
    option (primary_key_field) = "PlayerId";  // 与 XML <indexer> 中的字段名完全一致

    uint32 PlayerId = 1;   // 主键字段
    uint32 Score = 2;
    uint32 Season = 3;
}
```

对应的 XML 配置：
```xml
<scheme name="indexer">PlayerId</scheme>
```

如果主键就叫 `Id`，则不需要加这行 option，正常写 message 即可。

详细核查步骤见 [`references/indexer-type-check.md`](indexer-type-check.md)。

### Field Numbering

- Field numbers are auto-incremented starting from 1
- Repeated fields use `repeated` keyword
- Enum fields reference existing enum definitions

## Complete Workflow

```bash
# Step 1: Create Excel file with 4-row header format
# (See docs/table-format.md)

# Step 2: Preview proto generation
python table_tool/table_tool.py generate excel/YourFile.xlsx --target server --dry-run

# Step 3: Generate proto
python table_tool/table_tool.py generate excel/YourFile.xlsx --target server

# Step 4: Update XML configs if needed
# (Edit converter/convert_list*.xml)

# Step 5: Test conversion
cd converter
convert.bat  # Windows
# or
bash convert.sh  # Linux/macOS
```

## Output Files

### Client Proto
Output: `converter/resource/desc/client/res_client_struct.proto`

### Server Proto
Output: `converter/resource/desc/server/res_server.proto`

## Notes

- Excel field names MUST match proto message field names exactly
- Field numbers are auto-assigned in sequential order
- For enum types, ensure the enum definition exists before generation
