# Enum Management

Manage and synchronize enum definitions across game configuration tables.

## Overview

The enum management tool detects enum fields in Excel tables and helps synchronize them with proto enum definitions.

## Commands

### Detect Missing Enums

```bash
# Check which enums are referenced but not defined
python table_tool/table_tool.py enum --detect-only
```

### Preview Enum Additions

```bash
# Show what enums would be added without making changes
python table_tool/table_tool.py enum --dry-run
```

### Sync Enums

```bash
# Add missing enums to proto files
python table_tool/table_tool.py enum
```

### Command Options

| Option | Description |
|--------|-------------|
| `--detect-only` | Only detect missing enums, don't modify files |
| `--dry-run` | Preview what enums would be added |

## Enum Field Definition in Excel

To define an enum field in Excel:

1. **Row 1 (Field Names)**: Use `FieldName@EnumName` syntax
2. **Row 2 (Types)**: Specify `enum`
3. **Row 4 (Export Targets)**: Set export target as needed

Example:

| Row | A | B |
|-----|---|---|
| 1 | Position@PlayerPosition | Rank@RankingType |
| 2 | enum | enum |
| 3 | 球员位置 | 排名类型 |
| 4 | Client | Client |

## Enum Definition Structure

### Generated Enum Format

```protobuf
enum PlayerPosition {
    PLAYER_POSITION_NONE = 0;
    PLAYER_POSITION_POINTGUARD = 1;
    PLAYER_POSITION_SHOOTINGGUARD = 2;
    PLAYER_POSITION_SMALLFORWARD = 3;
    PLAYER_POSITION_POWERFORWARD = 4;
    PLAYER_POSITION_CENTER = 5;
}
```

### Enum Naming Convention

- Enum name: PascalCase (e.g., `PlayerPosition`)
- Enum values: UPPER_SNAKE_CASE with enum name prefix (e.g., `PLAYER_POSITION_POINTGUARD`)
- Default value: `{ENUM_NAME}_NONE = 0`

## Sync Process

### What the Tool Does

1. Scans all Excel files for enum fields (marked with `@EnumName` syntax)
2. Compares detected enums with existing proto enum definitions
3. For missing enums:
   - Creates enum definition in appropriate proto file
   - Generates enum values based on data found in Excel
4. For existing enums with new values:
   - Appends new enum values while preserving existing ones

### Enum Detection

Enum fields are detected when:
1. Field name contains `@EnumName` syntax in Row 1
2. Field type is `enum` in Row 2
3. Data values in the column are found

### Value Extraction

Enum values are extracted from:
- Unique values in the enum column across all rows
- Existing enum definitions (to avoid duplicates)

## Output Files

### Client Enums
Output: `converter/resource/desc/client/res_client_enum.proto`

### Server Enums
Output: `converter/resource/desc/server/res_server.proto`

### Common Enums (Shared)
Output: `converter/resource/desc/common/res_common.proto`

## Complete Workflow

```bash
# Step 1: Detect missing enums
python table_tool/table_tool.py enum --detect-only

# Step 2: Preview what will be added
python table_tool/table_tool.py enum --dry-run

# Step 3: Sync enums (adds missing enums)
python table_tool/table_tool.py enum

# Step 4: Review generated enum definitions
# (Check the proto files manually)

# Step 5: Test conversion
cd converter
convert.bat  # Windows
# or
bash convert.sh  # Linux/macOS
```

## Example Scenario

### Excel Table

```
| Id (uint32) | Position@PlayerPosition (enum) | Name (string) |
|-------------|--------------------------------|---------------|
| 1           | PG                             | Player1       |
| 2           | SG                             | Player2       |
| 3           | SF                             | Player3       |
```

### Generated Enum

```protobuf
enum PlayerPosition {
    PLAYER_POSITION_NONE = 0;
    PLAYER_POSITION_PG = 1;
    PLAYER_POSITION_SG = 2;
    PLAYER_POSITION_SF = 3;
}
```

## Notes

- Enum values are automatically assigned sequential numbers
- The tool preserves existing enum values and only appends new ones
- Use `--detect-only` to check which enums need to be added before syncing
- Always review generated enum definitions after syncing
