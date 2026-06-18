# Table Validation

Validate Excel table structure and cross-table field references.

## Overview

The validation tools ensure consistency between:
- Excel table definitions and conversion configs
- Field references between tables (foreign keys)

## Commands

### Validate Excel and Configs

```bash
# Validate Excel file structure and conversion configuration
python table_tool/table_tool.py validate excel/YourFile.xlsx
```

### Validate Field References

```bash
# Validate references using DOT file
python table_tool/table_tool.py validate-references --dot-file doc/excel.dot

# Validate with JSON output
python table_tool/table_tool.py validate-references --dot-file doc/excel.dot --format json

# Validate with CSV output
python table_tool/table_tool.py validate-references --dot-file doc/excel.dot --format csv
```

### Command Options

| Option | Description |
|--------|-------------|
| `--dot-file FILE` | DOT file containing table structure |
| `--format {text|json|csv}` | Output format (default: text) |

## Validation Checks

### Excel File Validation

Validates:
1. **Header Structure**: 4-row header format for NBA2kOL3 standard
2. **Field Names**: Match proto message field names
3. **Field Types**: Valid types (uint32, string, etc.)
4. **Export Targets**: Valid export target values
5. **Data Types**: Data values match specified field types
6. **PrimaryKey**: Exactly one PrimaryKey field exists
7. **Duplicate Keys**: Primary key values are unique

### Reference Validation

Validates:
1. **Referenced Tables Exist**: All referenced tables are defined in the DOT file
2. **Referenced Fields Exist**: Referenced fields exist in target tables
3. **Reference Types**: Reference field types match target field types
4. **Circular References**: Detects circular dependency chains

## Output Examples

### Text Format

```
Validating excel/Users.xlsx...
Validating excel/PlayerCard.xlsx...

Reference validation:
✓ UserLineupSet.RotationTimeId -> RotationInitial.Id (valid)
✓ PlayerCard.PlayerId -> PlayerAttribute.Id (valid)
✗ PlayerTeam.TeamId -> TeamInfo.TeamId ( TeamInfo.TeamId not found)
  at excel/PlayerTeam.xlsx:45

Validation complete: 2 errors found
```

### JSON Format

```json
{
  "errors": [
    {
      "type": "reference_not_found",
      "source": {
        "table": "PlayerTeam",
        "field": "TeamId"
      },
      "target": {
        "table": "TeamInfo",
        "field": "TeamId",
        "exists": false
      },
      "location": {
        "file": "excel/PlayerTeam.xlsx",
        "row": 45
      }
    }
  ],
  "warning_count": 0,
  "error_count": 1
}
```

### CSV Format

```csv
type,source_table,source_field,target_table,target_field,status,location
reference_not_found,PlayerTeam,TeamId,TeamInfo,TeamId,invalid,excel/PlayerTeam.xlsx:45
reference_valid,UserLineupSet,RotationTimeId,RotationInitial,Id,valid,-
```

## Complete Workflow

```bash
# Step 1: Generate/update DOT file
python table_tool/table_tool.py visualize excel/*.xlsx -o doc/excel.dot

# Step 2: Add reference edges
python table_tool/table_tool.py reference \
    --from-table UserLineupSet \
    --from-sheet UserLineupSet \
    --from-field RotationTimeId \
    --to-table RotationInitial \
    --to-sheet Main \
    --to-field Id

# Step 3: Validate specific Excel file
python table_tool/table_tool.py validate excel/UserLineupSet.xlsx

# Step 4: Validate all references
python table_tool/table_tool.py validate-references --dot-file doc/excel.dot

# Step 5: Export results for review
python table_tool/table_tool.py validate-references --dot-file doc/excel.dot --format csv > validation_report.csv
```

## Common Issues and Solutions

### Issue: Missing Reference Target

```
✗ PlayerTeam.TeamId -> TeamInfo.TeamId (TeamInfo not found)
```

Solution:
- Add the target table to visualization
- Or verify the table name is correct

### Issue: Field Type Mismatch

```
✗ User.TeamId -> Team.Id (type mismatch: string vs uint32)
```

Solution:
- Check field definitions in Excel
- Ensure source and target field types match

### Issue: Circular References

```
⚠ Circular reference detected: A -> B -> C -> A
```

Solution:
- Review the reference chain
- Determine if circular reference is intentional
- Consider redesigning the data model

## Notes

- Reference validation requires a DOT file generated with `visualize` command
- Use CSV or JSON format for programmatic processing of validation results
- Reference edges can be added manually using the `reference` command
