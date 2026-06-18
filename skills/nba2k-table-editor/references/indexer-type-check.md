# XML `<indexer>` 配置类型核对规范

## 核心原则

在 `convert_list*.xml` 中新增或修改 `<indexer>` 配置时，**indexer 中声明的数据类型必须与 proto 中对应字段的类型完全一致**。类型不匹配会导致转表时报 `Type mismatch` 或 `Invalid key type` 错误，二进制文件无法生成。

---

## ⚠️ Server 专属规则：非 `Id` 主键必须在 proto 中双重声明

> **仅适用于 server 类型导出（`convert_list_server.xml`）**，client / gamelib 不需要。

**背景**：server 侧默认只识别名为 `Id` 的主键字段。如果 `<indexer>` 中指定的主键字段名不是 `Id`，仅靠 XML 中的 `<indexer>` 配置还不够——还必须在对应的 proto `message` 定义的**头部**加入 `option (primary_key_field)` 声明，告知 server 框架哪个字段是主键。

### 规则总结

| indexer 字段名 | XML `<indexer>` | proto `message` |
|----------------|-----------------|-----------------|
| `Id`（默认）   | 正常写 | **无需** 添加 `option` |
| 非 `Id`（自定义主键）| 正常写 | **必须** 在 message 头部加 `option (primary_key_field) = "字段名";` |

### 示例：主键字段名为 `PlayerId`

**XML（`convert_list_server.xml`）：**
```xml
<item name="PlayerScore_Server" cat="Player" class="server">
    <scheme name="DataSource">../../excel/PlayerScore.xlsx|Main|5,1</scheme>
    <scheme name="ProtoName">NBA3.Game.Resource.server.PlayerScore</scheme>
    <scheme name="OutputFile">server/PlayerScore.bin</scheme>
    <scheme name="indexer">PlayerId</scheme>   <!-- 主键字段名不是 Id -->
</item>
```

**Proto（`res_server.proto`）：**
```protobuf
message PlayerScore {
    option (primary_key_field) = "PlayerId";   // ← 必须加，且在所有字段定义之前

    uint32 PlayerId = 1;  // 主键
    uint32 Score = 2;
    uint32 Season = 3;
}
```

### 示例：主键字段名就是 `Id`（正常情况，无需额外声明）

```xml
<scheme name="indexer">Id</scheme>
```

```protobuf
message PlayerAbility {
    // 无需 option (primary_key_field)，server 默认识别 Id
    uint32 Id = 1;
    uint32 Strength = 2;
}
```

### 核查清单（server 导出时）

- [ ] 确认 `<indexer>` 中的字段名
- [ ] 如果字段名 **不是** `Id`：检查对应 proto message 头部是否有 `option (primary_key_field) = "字段名";`
- [ ] `option` 声明必须放在 **所有字段行之前**（紧接 message 的开头花括号后）
- [ ] `option` 中的字段名与 `<indexer>` 中的字段名必须**完全一致**（区分大小写）

---

---

## 核查步骤

### 第一步：确认 indexer 引用的字段名

在 XML 配置中找到 `<indexer>` 行，记下其中的字段名（通常是主键字段，如 `Id`）。

### 第二步：在 proto 文件中查找该字段的类型

```bash
# 查 client proto
grep "FieldName" converter/resource/desc/client/res_client_struct.proto

# 查 server proto
grep "FieldName" converter/resource/desc/server/res_server.proto

# 查 gamelib proto（如有）
grep "FieldName" converter/resource/desc/gamelib/*.proto
```

示例输出：
```
uint32 Id = 1;   →  确认类型为 uint32
int32  Id = 1;   →  确认类型为 int32（历史遗留表常见）
string Name = 2; →  确认类型为 string
```

### 第三步：确保 indexer 声明类型与 proto 一致

indexer 里用什么类型标识，完全取决于你们项目的 xresloader 配置惯例。
**参照同一 category 里已有表的 indexer 写法是最可靠的方式：**

```bash
# 快速参考同类表的 indexer 写法
grep -B2 -A8 "cat=\"YourCategory\"" converter/convert_list_server.xml | grep -i "indexer\|KeyRow\|DataSource"
```

---

## 常见易错场景

| 场景 | 容易犯的错误 | 正确做法 |
|------|-------------|---------|
| 历史遗留表主键 | 想当然写成 `uint32`，实际 proto 是 `int32` | 先 grep proto 确认 |
| 联合主键 | 只核查第一个 key 字段 | 每个 key 字段都要分别核查 |
| 枚举字段作主键 | 直接写枚举名，但 indexer 期望 `uint32` | 参考同类表写法 |
| 新建表直接仿照旧表 | 旧表主键是 `int32`，新表 proto 用了 `uint32` | 不能盲目复制，必须核查 |

---

## 类型不匹配的后果

- 转表时报 `Type mismatch` 或 `Invalid key type`
- 二进制 `.bin` 文件生成失败，或生成 0 字节文件
- 即使侥幸生成，运行时可能出现数据读取异常

---

## 支持的类型

| 类型 | 说明 |
|------|------|
| `uint32` | 无符号 32 位整数（最常见主键类型） |
| `int32`  | 有符号 32 位整数（历史遗留表常见） |
| `uint64` | 无符号 64 位整数 |
| `int64`  | 有符号 64 位整数 |
| `string` | 字符串（较少用于主键） |
