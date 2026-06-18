---
name: nba2k-skin-moment-config
description: |
  NBA2KOL2 游戏"时刻"皮肤配表工具。用于向 PlayerSkin.xlsx 及其关联 sheet 追加新的皮肤条目，覆盖完整的依赖链（UniformPanel、PicPanel、VideoPanel、CelebratePanel、IntroPanel、Main、UserInfoPanel），并配置关联的 Equipment.xlsx、Condition.xlsx、ClothesSet.xlsx、ID2StringMapTable.xlsx、Item.xlsx、CommonExchange.xlsx。

  在以下场景下请主动使用本技能：
  - 用户提到要"配表"、"新增皮肤"、"加皮肤条目"、"填 PlayerSkin"
  - 用户说要配置"时刻"内容、新球员皮肤、或某某球员的XXX版本
  - 用户提到 PlayerSkin.xlsx 的任何 sheet（Main、IntroPanel、PicPanel、VideoPanel、UniformPanel、CelebratePanel）
  - 用户提供了 Main ID、球员英文名文件夹、中文名版本标签等皮肤配置相关信息
  - 用户提到"陈列室"、"致敬传奇"、"历史球员"、"现役球员"等系列名称
  - 用户说"配XX球员"、"加个时刻"、"新增一个皮肤"、"开始配表"
  - 用户提到 Equipment、Condition、ClothesSet、Item、CommonExchange 等关联表的配置
  - 用户说"碎片"、"合成"、"分解"、"道具配置"、"本地化文本"等配表相关术语
---

# NBA2KOL2 时刻皮肤配表技能

本技能采用 **checklist 逐步推进**模式。每个阶段有明确完成条件，必须全部 ✅ 后才能进入下一阶段。

**核心规范：每收集完一个字段或完成一个步骤后，必须立即在回复中展示当前阶段的完整 checklist，用 `[x]` 标记已完成项，`[ ]` 标记未完成项，并附上已确认的值。** 不得跳过 checklist 展示。

---

## 预置脚本说明

本 skill 目录下的 `scripts/` 提供可直接调用的工具，**不需要每次临时写代码**：

### PlayerSkin 相关（阶段 1~5）

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `scripts/read_sheet_info.py` | 读取 PlayerSkin 指定 sheet 的最大 ID 及末尾行 | `python <skill_dir>/scripts/read_sheet_info.py --sheet PicPanel` |
| `scripts/write_skin_rows.py` | 按依赖顺序向 PlayerSkin 各 sheet 写入新行 | `python <skill_dir>/scripts/write_skin_rows.py --data skin_data.json` |
| `scripts/verify_skin_rows.py` | 写入后读回验证，逐字段对比 | `python <skill_dir>/scripts/verify_skin_rows.py --data skin_data.json` |

### 全局状态读取

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `scripts/read_all_state.py` | **一次性读取所有表格**（PlayerSkin/Equipment/Condition/ClothesSet/Item/CommonExchange/ID2StringMapTable）的最大 ID、号段末尾等关键状态，输出 JSON | `python <skill_dir>/scripts/read_all_state.py --output state.json` |

> **⚠️ 必须在阶段 1 第1问之前调用 `read_all_state.py`**，一次获取所有推断 ID 所需的基础数据，后续阶段直接引用，减少重复读表。这是强制步骤，不可跳过。

#### 列结构扫描（新增关联表规则时使用）

当需要为新表补充配表规则时，先运行 `--dump-columns` 扫描真实数据的所有非空列，避免遗漏"每行都一样的固定列"：

```bash
python <skill_dir>/scripts/read_all_state.py --dump-columns
python <skill_dir>/scripts/read_all_state.py --dump-columns --output columns.json
```

输出每张表每个 sheet 的：列号、列名、非空率(%)、唯一值数量、前5个样本值。重点关注：
- **非空率 100% + 唯一值 1~3** → 大概率是必填固定值列，不可遗漏
- **非空率 > 90% + 唯一值较多** → 大概率是每行不同的业务字段

### 关联表写入（阶段 6~11）

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `scripts/write_equipment.py` | Equipment 表（Equip_PlayerSkin + Equip_Clothes）+ 可选 Condition 表一次写入 | `python <skill_dir>/scripts/write_equipment.py --data equip_data.json` |
| `scripts/write_clothesset.py` | ClothesSet 表追加一行 | `python <skill_dir>/scripts/write_clothesset.py --data clothesset_data.json` |
| `scripts/write_id2string.py` | ID2StringMapTable LangShort 追加本地化文本行 | `python <skill_dir>/scripts/write_id2string.py --data id2string_data.json` |
| `scripts/write_item.py` | Item 表写入碎片/完整/服装行（支持 80XXX 中间插入 + 88XXX 末尾追加） | `python <skill_dir>/scripts/write_item.py --data item_data.json` |
| `scripts/write_exchange.py` | CommonExchange 合成/分解行写入 + Item 碎片 UseLinkID 回填 | `python <skill_dir>/scripts/write_exchange.py --data exchange_data.json` |

所有写入脚本均支持 `--dry-run` 预演模式，均内置格式继承、ID 占用校验、写入后验证。

`<skill_dir>` 为本技能目录：`C:\Users\siminggao\.workbuddy\skills\nba2k-skin-moment-config`

---

## 阶段 1：前置信息收集

> **进入条件**：用户发起配表请求
> **完成条件**：下方所有字段均已确认 ✅

**重要原则：逐个发问，一次只用 `AskUserQuestion` 问一个问题，收到回答后再问下一个。** 不要把多个问题合并成一次询问。

**AskUserQuestion 交互规范：**
- 推荐/默认选项文本末尾加 **"- 默认值"** 标识（如 `队服（ClothesType = 0）- 默认值`）
- 自由输入选项用 **"直接在聊天框输入"** 而非"自行输入"

**checklist 展示规范：每收到一个回答后，立即展示如下格式的阶段1进度 checklist，然后再提问下一个问题。**

```
### 阶段 1 进度
- [x] 球员系列: {值}（SeriesID={值}）
- [x] 皮肤类型: {小时刻/大时刻}（仅陈列室/致敬传奇）
- [ ] Main ID
- [ ] 文件夹名
- [ ] 球员中文名及版本标签
- [ ] 时刻中文名
- [ ] IntroPanel ID
- [ ] VideoMarkID
- [ ] 可选功能模块
```

这些信息贯穿所有 sheet，是路径命名基础。按以下顺序逐一收集：

**第1问：球员系列（AskUserQuestion 单选，按 SeriesID 升序排列）**
- 陈列室时刻（SeriesID = 0）
- 致敬传奇时刻（SeriesID = 1）
- 历史球员时刻（SeriesID = 2）
- 现役球员时刻（SeriesID = 3）

> **皮肤类型三分类**：小时刻、大时刻、普通皮肤。
> - 若系列为陈列室时刻或致敬传奇时刻，紧接着追加一问：**皮肤类型**（单选：小时刻 / 大时刻）。小时刻当前与普通皮肤规则一致，大时刻为原特殊皮肤规则。
> - 其他系列跳过此问，默认普通皮肤。
>
> **陈列室/致敬传奇连续配置流程**：选择陈列室或致敬传奇系列后，先完成**小时刻**的阶段1~3全部字段收集，再完成**大时刻**的阶段1~3全部字段收集，两个时刻数据一起在阶段4汇总确认，阶段5一次性写入。

**第2问：Main ID**
- 皮肤唯一主键，所有美术资产以此命名（如 `70068`）
- 若用户在请求中已提供，可跳过此问，直接在 checklist 中标记为 `[x]`

**第3问：文件夹名**
- 美术资产存放目录名（如 `Julius_Erving`）

**第4问：球员中文名及版本标签**
- 用于备注字段（如 `朱利叶斯.欧文(75版)`）

**第5问：时刻中文名**
- 用于 Main 备注字段（如 `J博士`、`炉火纯青`、`致命封锁`）
- 注意：使用"时刻中文名"而非"系列名"或"时刻名"，避免歧义

**第6问：IntroPanel ID 和 VideoMarkID**
- 运行 `read_sheet_info.py --sheet IntroPanel` 和 `--sheet VideoPanel` 自动读取当前最大 ID，推断值为最大 ID+1
- 将推断值告知用户，允许用户自定义；若用户确认使用推断值，直接标记 `[x]`

**第7问：可选功能模块（此问用多选）**
- 是否有**入场视频**（影响 PicPanel 的 VideoPic/VideoRes/PostionX/PostionY）
- 是否需要**球衣页签**（需要 UniformPanel）
- 是否需要**徽章视频**（需要 VideoPanel）
- 是否需要**庆祝动作**（需要 CelebratePanel，见"⚠️ 尚未完整定义的关联表"处理流程）

> 注意：如果用户在初始请求中已经提供了部分信息，跳过对应的问题，直接在 checklist 中标记为 `[x]`，不要重复询问已知信息。

**阶段 1 全部完成后，展示完整的最终 checklist，并显示：**
```
### 阶段 1 ✅ 全部完成
- [x] 球员系列: {值}（SeriesID={值}）
- [x] 皮肤类型: {小时刻/大时刻}
- [x] Main ID: {值}
- [x] 文件夹名: {值}
- [x] 球员中文名及版本标签: {值}
- [x] 时刻中文名: {值}
- [x] IntroPanel ID: {值}
- [x] VideoMarkID: {值}（读取 VideoPanel 最大 ID +1，独立推断）
- [x] 可选功能模块: {列出所有已选模块}
```

---

## 阶段 2：依赖链确认

> **进入条件**：阶段 1 全部 ✅
> **完成条件**：依赖链结构已展示给用户，填写顺序已确认

根据阶段 1 的选择，生成本次的依赖链图示并展示给用户：

```
Main (ID={MainID})
├── IntroPanelID ──→ IntroPanel (ID={IntroPanelID})
│                       ├── Option1 ──→ PicPanel 页签1（始终需要）
│                       ├── Option2 ──→ PicPanel 页签2（始终需要）
│                       ├── OptionN ──→ UniformPanel（如有球衣页签）
│                       ├── OptionN ──→ VideoPanel（如有徽章视频）
│                       └── OptionN ──→ CelebratePanel（如有庆祝动作）
└── VideoMarkID   ──→ VideoPanel（ID={VideoMarkID}）
```

**展示依赖链图示后，立即展示阶段2 checklist 初始状态：**
```
### 阶段 2 进度
- [x] 依赖链图示已展示
- [ ] UniformPanel 处理方式确认（如需）
- [ ] VideoPanel 处理方式确认（如需）
- [ ] CelebratePanel 处理方式确认（如需）
- [ ] 填写顺序确认
```

对于 UniformPanel / VideoPanel / CelebratePanel：
- **UniformPanel 和 VideoPanel 默认新增一行**，无需用 AskUserQuestion 询问。仅当用户主动说要复用已有记录时才走已有 ID 流程。
- **CelebratePanel** 需要询问是否有庆祝动作：选"无"则跳过；选"有"则查询该列 ID 最大值+1 推断新 ID。

**每问完一个，立即更新 checklist。**

**本次填写顺序（从底层到顶层），展示时用实际启用的 sheet：**

1. [ ] UniformPanel（如需，确认使用已有记录 or 新增）
2. [ ] PicPanel（始终需要，成对新增2行）
3. [ ] VideoPanel（如需，确认使用已有记录 or 新增）
4. [ ] CelebratePanel（如需，见"⚠️ 尚未完整定义的关联表"处理流程）
5. [ ] IntroPanel
6. [ ] Main

**阶段 2 全部完成后，展示：**
```
### 阶段 2 ✅ 全部完成
- [x] 依赖链图示已展示
- [x] UniformPanel: {新增一行 / 使用已有ID=XX}
- [x] VideoPanel: {新增一行 / 使用已有ID=XX}
- [x] 填写顺序已确认：UniformPanel → PicPanel → VideoPanel → IntroPanel → Main
```

---

## 阶段 3：各 Sheet 字段逐一确认

> **进入条件**：阶段 2 全部 ✅
> **完成条件**：所有需要填写的 sheet 的每一字段均已确认

字段类型标记：
- **[输入]** 必须用 `AskUserQuestion` 逐个向用户询问，**无论字段说明中是否给出了默认值或常见值，都不能自行决定，必须问用户确认**
- **[推断]** 根据规则推导，直接计算填入，无需发问（可在汇总时展示供用户核查）
- **[推断-ID]** 需先运行 `read_sheet_info.py` 读取当前最大 ID，告知用户后用 `AskUserQuestion` 确认
- **[引用]** 引用其他 sheet 主键，自动填入已确认的关联 ID，无需发问
- **[固定留空]** 固定为空，无需发问

**阶段3 checklist 展示规范：**
- 进入每个 sheet 小节时，先展示该 sheet 的完整 checklist（全部 `[ ]`）
- 每收集完一个 `[输入]` 字段，或确认完一批 `[推断]` 字段后，立即更新展示 checklist
- 该 sheet 所有字段确认完毕后，展示全部 `[x]` 的完成状态

### 3.1 UniformPanel（球衣面板）

> 仅在需要球衣页签且选择新增时填写

运行命令读取当前状态：
```bash
python <skill_dir>/scripts/read_sheet_info.py --sheet UniformPanel
```

**进入本节时展示初始 checklist：**
```
### 3.1 UniformPanel 进度
- [ ] ID [输入]
- [ ] ClothesType [输入]
- [ ] BkgRes [推断]
- [ ] DetailResHome [推断]
- [ ] DetailResAway [推断]
- [ ] IconLogo [推断]
- [ ] IconTitleBg [推断]
- [ ] HomeName [推断]
- [ ] AwayName [推断]
```

字段说明：
- ID `[输入]` 明确输入，不强制连续
- ClothesType `[输入]` 队服=`0`，休闲=其他值
- BkgRes `[推断]` `Skin\{文件夹名}\Jersey_Bkg.dds`
- DetailResHome `[推断]` `Skin\{文件夹名}\Jersey_Home_{MainID}`
- DetailResAway `[推断]` `Skin\{文件夹名}\Jersey_Away_{MainID}`
- IconLogo `[推断]` 固定 `Icon\Jerseylogo_01_256.dds`
- IconTitleBg `[推断]` 固定 `Skin\All_Skin\Tipstop_01.dds`
- HomeName `[推断]` 固定 `400000001`
- AwayName `[推断]` 固定 `400000002`

**收集完 ID 后，立即展示更新的 checklist（ID 变为 [x]，推断字段一并填入并标 [x]）：**
```
### 3.1 UniformPanel 进度
- [x] ID: {值}
- [ ] ClothesType [输入]
- [x] BkgRes: Skin\{文件夹名}\Jersey_Bkg.dds（推断）
- [x] DetailResHome: Skin\{文件夹名}\Jersey_Home_{MainID}（推断）
- [x] DetailResAway: Skin\{文件夹名}\Jersey_Away_{MainID}（推断）
- [x] IconLogo: Icon\Jerseylogo_01_256.dds（推断）
- [x] IconTitleBg: Skin\All_Skin\Tipstop_01.dds（推断）
- [x] HomeName: 400000001（推断）
- [x] AwayName: 400000002（推断）
```

**收集完所有字段后展示：**
```
### 3.1 UniformPanel ✅ 完成
- [x] ID: {值}
- [x] ClothesType: {值}
- [x] BkgRes: {路径}（推断）
... （所有字段全部 [x]）
```

---

### 3.2 PicPanel（图片面板）

> 始终需要，每次固定成对新增两行

运行命令读取当前最大 ID：
```bash
python <skill_dir>/scripts/read_sheet_info.py --sheet PicPanel
```

**进入本节时展示初始 checklist：**
```
### 3.2 PicPanel 进度
**行1（页签1 时刻介绍）**
- [ ] ID [推断-ID]
- [ ] 备注 [推断]
- [ ] BkgRes [推断]
- [ ] VideoPic [输入]
- [ ] VideoRes [输入]
- [ ] PostionX [输入]
- [ ] PostionY [输入]

**行2（页签2 卡面效果）**
- [ ] ID [推断-ID]
- [ ] 备注 [推断]
- [ ] BkgRes [推断]
- [ ] VideoPic/VideoRes/PostionX/PostionY [固定留空]
```

字段说明：

**行1（页签1 时刻介绍）：**
- ID `[推断-ID]` 读取后告知"当前最大 ID 为 X，推断新行为 X+1"，允许用户自定义
- 备注 `[推断]` `{球员中文名及版本} 页签1 时刻介绍`
- BkgRes `[推断]` `Skin\{文件夹名}\L_Bkg_{MainID}_Intro.dds`
- VideoPic `[推断+确认]`
  - 现役球员时刻：先用多选 `AskUserQuestion` 询问"是否需要配置以下可选项：入场视频封面（VideoPic）/ 入场视频（VideoRes）/ 视频坐标（PostionX/Y）"，勾选的才填入，未勾选留空
  - 其他系列且有入场视频：推断值为 `Skin\{文件夹名}\Entrance_{MainID}.dds`，与 VideoRes 合并为一题确认（见下）；否则留空
- VideoRes `[推断+确认]`
  - 现役球员时刻：同上多选结果决定是否填入
  - 其他系列且有入场视频：推断值为 `Skin\{文件夹名}\V_Entrance_{MainID}.usm`，与 VideoPic 合并为一题，用 `AskUserQuestion` 展示两个推断值，选项为"确认使用 - 默认值"和"直接在聊天框输入"；否则留空
- PostionX / PostionY `[输入]` VideoRes 不为空时（含现役勾选后），合并为一题"PostionX / PostionY"，用 `AskUserQuestion` 提供选项：
  - 陈列室时刻 / 致敬传奇时刻 → `140, 490` - 默认值
  - 历史球员时刻 → `994, 509` - 默认值
  - 直接在聊天框输入
  - VideoRes 为空时，PostionX/PostionY 均填 `0`

**行2（页签2 卡面效果）：**
- ID `[推断-ID]` 推断值为行1 ID+1，告知用户，允许自定义
- 备注 `[推断]` `{球员中文名及版本} 页签2 卡面效果`
- BkgRes `[推断]` `Skin\{文件夹名}\L_Bkg_{MainID}_Scene.dds`
- VideoPic / VideoRes / PostionX / PostionY `[固定留空]`

**每收集完一个 [输入] 字段后立即更新 checklist。所有字段确认完毕后展示：**
```
### 3.2 PicPanel ✅ 完成
**行1（页签1）**
- [x] ID: {值}
- [x] 备注: {值}（推断）
- [x] BkgRes: {路径}（推断）
- [x] VideoPic: {值}
- [x] VideoRes: {值}
- [x] PostionX: {值}
- [x] PostionY: {值}

**行2（页签2）**
- [x] ID: {值}
- [x] 备注: {值}（推断）
- [x] BkgRes: {路径}（推断）
- [x] VideoPic/VideoRes/PostionX/PostionY: 留空（固定）
```

---

### 3.3 VideoPanel（徽章视频面板）

> 仅在需要徽章视频且选择新增时填写；ID 与 Main.VideoMarkID 相同

运行命令读取当前状态：
```bash
python <skill_dir>/scripts/read_sheet_info.py --sheet VideoPanel
```

**进入本节时展示初始 checklist：**
```
### 3.3 VideoPanel 进度
- [ ] ID [输入]
- [ ] BadgeName [输入]
- [ ] BkgRes [推断]
- [ ] VideoRes [输入]
- [ ] 备注 [推断]
```

字段说明：
- ID `[输入]` 与 Main.VideoMarkID 相同
- BadgeName `[输入]` 用 AskUserQuestion 从已知枚举中选择（见下方列表）
- BkgRes `[推断]` `Skin\{文件夹名}\L_Bkg_{MainID}_Badge.dds`
- VideoRes `[推断+确认]` 规律：`Skin\{文件夹名}\V_{版本缩写}{球员英文名}_Bdg_{徽章类型去掉Bdg_TC}_TC.usm`
  - **版本缩写推断规则**：从"球员中文名及版本标签"的括号中提取数字部分，如 `(75版)` → `75`，`(13版)` → `13`。最终路径示例：`V_75Julius_Erving_Bdg_Slithery_TC.usm`。推断后用 `AskUserQuestion` 确认，允许用户自定义。
- 备注 `[推断]` `{时刻中文名} 页签N 徽章展示`，其中 N 为该页签在 IntroPanel 中的序号（页签1=PicPanel介绍、页签2=PicPanel卡面，有球衣页签则+1，VideoPanel 徽章页签紧随其后）；例：无球衣→页签3，有球衣→页签4

**BadgeName 选项（AskUserQuestion）：**
已知枚举：`Bdg_TCPowerDunk` / `Bdg_TCLimitlessTakeoff` / `Bdg_TCMismatchExpert` / `Bdg_TCFastTwitch` / `Bdg_TCRiseUp` / `Bdg_TCQuickRelease` / `Bdg_TCReboundChaser` / `Bdg_TCLightningBoost` / `Bdg_TCPosterizer` / `Bdg_TCLimitlessRange` / `Bdg_TCCornerSpecialist` / `Bdg_TCFastTwitchPro` / `Bdg_TCAgent3` / `Bdg_TCPickDodger` / `Bdg_TCBackdownMaster` / `Bdg_TCLimitlessDunk` / `Bdg_TCSlithery` / `Bdg_TCGlove`
**末尾追加选项："直接在聊天框输入"**（允许用户输入枚举列表以外的新徽章名）

**每收集完一个 [输入] 字段后立即更新 checklist。所有字段确认完毕后展示：**
```
### 3.3 VideoPanel ✅ 完成
- [x] ID: {值}
- [x] BadgeName: {值}
- [x] BkgRes: {路径}（推断）
- [x] VideoRes: {值}
- [x] 备注: {值}（推断）
```

---

### 3.4 IntroPanel（出场面板）

**进入本节时展示初始 checklist：**
```
### 3.4 IntroPanel 进度
- [ ] ID [输入]
- [ ] 备注 [推断]
- [ ] IntroBKG [推断]
- [ ] TitleRes [推断]
- [ ] TitleDes [推断-确认]
- [ ] TipsDes [推断]
- [ ] Option1Type/ID/Des [推断+引用]
- [ ] Option2Type/ID/Des [推断+引用]
- [ ] Option3Type/ID/Des（如有）
- [ ] Option4Type/ID/Des（如有）
...
```

字段说明：
- ID `[输入]` 与 Main.IntroPanelID 相同
- 备注 `[推断]` `{球员中文名及版本}`
- IntroBKG `[推断]` `Skin\{文件夹名}\Intro_R_Bkg.dds`
- TitleRes `[推断]` `Skin\{文件夹名}\Title_{MainID}.dds`
- TitleDes `[推断]` 读取 IntroPanel 末尾行的 TitleDes 值，递增 2 得到本次值（规律：每行 +2，如上一行为 300603142 则本次为 300603144）；告知用户推断值，允许自定义
- TipsDes `[推断]` 固定为 TitleDes + 1，无需发问
- Option1Type `[推断]` 固定 `PLAYER_SKIN_INTRO_PANEL_PIC`
- Option1ID `[引用]` PicPanel 页签1 ID
- Option1Des `[推断]` 固定 `300604001`
- Option2Type `[推断]` 固定 `PLAYER_SKIN_INTRO_PANEL_PIC`
- Option2ID `[引用]` PicPanel 页签2 ID
- Option2Des `[推断]` 固定 `300605001`
- Option3~6 Type/ID/Des：如有额外页签，**逐个**用 `AskUserQuestion` 询问，每个 Option 单独问（类型选择 + 对应 ID），不要合并
  - Des 推断规则：UNIFORM→`300608001`，VIDEO→`300606001`，CELEBRATE→`300609001`

**Option Type 枚举：**
- `PLAYER_SKIN_INTRO_PANEL_UNIFORM` → 引用 UniformPanel
- `PLAYER_SKIN_INTRO_PANEL_VIDEO` → 引用 VideoPanel
- `PLAYER_SKIN_INTRO_PANEL_CELEBRATE` → 引用 CelebratePanel（见"⚠️ 尚未完整定义的关联表"处理流程）

**每收集完一个 [输入] 字段后立即更新 checklist。所有字段确认完毕后展示：**
```
### 3.4 IntroPanel ✅ 完成
- [x] ID: {值}
- [x] 备注: {值}（推断）
- [x] IntroBKG: {路径}（推断）
- [x] TitleRes: {路径}（推断）
- [x] TitleDes: {值}
- [x] TipsDes: {值}
- [x] Option1: PIC / {ID} / 300604001（推断+引用）
- [x] Option2: PIC / {ID} / 300605001（推断+引用）
- [x] Option3: {类型} / {ID} / {Des}
...
```

---

### 3.5 Main sheet（皮肤主表）

**进入本节时展示初始 checklist：**
```
### 3.5 Main 进度
- [ ] ID [已知]
- [ ] 备注 [推断]
- [ ] PlayerTemplate [输入]
- [ ] PlayerName [推断]
- [ ] 备注.1 [推断]
- [ ] SeriesID [引用]
- [ ] SkinIcon [推断]
- [ ] SkinRectImage [推断]
- [ ] UserInfoPanelID [推断]
- [ ] Avatar [推断]
- [ ] PlayerImage [推断]
- [ ] Signature [推断]
- [ ] SignatureVideo [推断]
- [ ] CardTypeIcon [推断]
- [ ] IngameFootNote [推断]
- [ ] ScoreAnimationSetID [推断]
- [ ] IntroPanelID [引用]
- [ ] VideoMarkID [引用]
- [ ] SerialRuleID [推断]
- [ ] MergeAnimationVideo [推断]
- [ ] MergeAnimationAdjustColorBrightness [推断]
- [ ] MergeAnimationAdjustColorSaturation [推断]
- [ ] MergeAnimationAdjustColorHue [推断]
- [ ] MergeAnimationPlayerPicture [推断]
- [ ] MergeAnimationTextPicture [推断]
- [ ] ColorBar [推断]
- [ ] SessionLoadingColorType [推断]
- [ ] SessionLoadingColor [推断]
- [ ] ClothItemID [推断]
- [ ] MiscAnimationSetID [输入]
```

字段说明：
- ID `[已知]` 前置输入
- 备注 `[推断]` `{时刻中文名} {球员中文名及版本}`
- PlayerTemplate `[输入]` 球员模板 ID。**收集后需校验**：如果该 PlayerTemplate 在 Main 中已有其他皮肤记录（排除本次正在配置的），需要向用户问询确认是否正确，避免输入错误导致关联配置全错。
- PlayerName `[推断]` 同一 PlayerTemplate 的所有皮肤共用同一个 PlayerName ID。若该 PlayerTemplate 已有皮肤记录，复用已有 PlayerName；若为首次，读取 Main 末尾行的 PlayerName 值 +1 推断。大时刻复用小时刻的 PlayerName，不再额外 +1。
- 备注.1 `[推断]` `{球员中文名及版本}`
- SeriesID `[引用]` 阶段1已确认：陈列室时刻=`0`，致敬传奇时刻=`1`，历史球员时刻=`2`，现役球员时刻=`3`
- SkinIcon `[推断]` `Skin\{文件夹名}\head_{MainID}.dds`
- SkinRectImage `[推断]` `Skin\{文件夹名}\changingroom_{MainID}.dds`
- UserInfoPanelID `[推断]`
  - 小时刻 / 普通皮肤：默认填 `0`，无需询问
  - 大时刻：读取 UserInfoPanel 当前最大 ID +1 推断新值，向用户确认。确认后需同步在 PlayerSkin UserInfoPanel sheet 新增一行（字段：ID/SignaturePositionX=664/SignaturePositionY=298/备注="{球员姓}签名在个人信息的位置参数"），推断后向用户询问确认。
    **写入方式**：将 UserInfoPanel 行数据加入 skin_data.json 的 `"UserInfoPanel"` 键下，write_skin_rows.py 已支持该 sheet 自动写入和验证，无需手写代码。示例：
    ```json
    "UserInfoPanel": [{"1": 31, "2": 664, "3": 298, "4": "欧文签名在个人信息的位置参数"}]
    ```
- Avatar `[推断]` 同 SkinIcon
- PlayerImage `[推断]` `Skin\{文件夹名}\skin{MainID}.dds`（注意：无下划线）
- Signature `[推断]`
  - 小时刻 / 普通皮肤：留空，无需询问
  - 大时刻：自动推断路径 `Skin\{文件夹名}\Signature_{MainID}.dds`，无需询问
- SignatureVideo `[推断]`
  - 小时刻 / 普通皮肤：留空
  - 大时刻：自动推断路径 `Skin\{文件夹名}\V_Signature_{MainID}.usm`
- CardTypeIcon `[推断]`
  - 小时刻 / 普通皮肤：留空
  - 大时刻：自动推断 `{球员英文名}Skin`（英文名无空格无下划线，如 KawhiLeonardSkin），从文件夹名去掉下划线推断
- IngameFootNote `[推断]` 根据系列和皮肤类型自动填入，无需询问：
  - 陈列室大时刻 → `GAMELIBRARY_ROSTER_PLAYERDATA_ABILITY_ICON_TC_DESIGNED`
  - 致敬传奇大时刻 → `GAMELIBRARY_ROSTER_PLAYERDATA_ABILITY_ICON_TC_DESIGNED_LEGEND`
  - 其他所有情况（小时刻、普通皮肤）→ `0`
- ScoreAnimationSetID `[推断]` 固定 `0`
- IntroPanelID `[引用]` IntroPanel 主键
- VideoMarkID `[引用]` VideoPanel 主键
- SerialRuleID `[推断]` 根据系列和皮肤类型自动推断，无需询问：
  - 致敬传奇时刻（所有）→ `0`（无贴纸）
  - 陈列室大时刻 → 读取 Main sheet SerialRuleID 列当前非零最大值 +1
  - 其他（小时刻、普通皮肤）→ `0`
- MergeAnimationVideo `[推断]` 固定 `Skin\All_Skin\V_General_Merge_02.usm`
- MergeAnimationAdjustColorBrightness `[推断]` 固定 `0`
- MergeAnimationAdjustColorSaturation `[推断]` 根据皮肤类型自动填入，无需发问：
  - 特殊皮肤（陈列室/致敬传奇中被用户标记为大时刻）→ `0`
  - 普通皮肤（其他系列，或陈列室/致敬传奇中未标记）→ `-100`
- MergeAnimationAdjustColorHue `[推断]` 根据皮肤类型自动填入，无需发问：
  - 特殊皮肤 → `0`
  - 普通皮肤 → 留空

> **皮肤类型判断**：当系列为陈列室时刻或致敬传奇时刻时，阶段1已收集皮肤类型（小时刻/大时刻），直接引用。其他系列默认为普通皮肤。
>
> **大时刻自动复用规则**（陈列室/致敬传奇连续配置时）：大时刻以下字段与小时刻一致，自动复用无需询问：
> - 文件夹名、球员中文名及版本标签、PlayerTemplate、可选功能模块
>
> **大时刻自动递推规则**：
> - Main ID = 小时刻 Main ID + 1
> - IntroPanel ID = 小时刻 IntroPanel ID + 1
> - VideoMarkID = 小时刻 VideoMarkID + 1
> - UniformPanel ID = 小时刻 UniformPanel ID + 1
> - PicPanel ID = 小时刻 PicPanel 最后一个 ID + 1（连续）
> - PlayerName = 复用小时刻的 PlayerName（同模板共用）
> - TitleDes = 小时刻 TitleDes + 2
> - ClothItemID = 小时刻 ClothItemID + 1
>
> **大时刻需要单独询问的差异字段**：
> - 时刻中文名、BadgeName（徽章类型）
- MergeAnimationPlayerPicture `[推断]` 同 PlayerImage
- MergeAnimationTextPicture `[推断]` `Skin\{文件夹名}\textskin_{MainID}.dds`
- ColorBar `[推断]` 根据系列和皮肤类型自动填入，无需发问：
  - 陈列室时刻 + 大时刻（特殊）→ `2`
  - 陈列室时刻 + 普通 → `1`
  - 致敬传奇时刻 + 大时刻（特殊）→ `20`
  - 致敬传奇时刻 + 普通 → `1`
  - 历史球员时刻 / 现役球员时刻 → `1`
- SessionLoadingColorType `[推断]` 根据系列自动推断，无需询问：
  - 陈列室/致敬传奇 → `SESSION_LOADING_COLOR_TYPE_SKIN_COLOR`（固定）
  - 历史/现役 → 需询问（SKIN_COLOR 或 TEAM_COLOR）
- SessionLoadingColor `[推断]` 根据系列和皮肤类型自动推断，无需询问：
  - 陈列室/致敬传奇 小时刻 → `14277081`
  - 陈列室 大时刻 → `16770194`
  - 致敬传奇 大时刻 → `15378318`
  - 历史/现役 → 需询问（TEAM_COLOR 时通常 `0`，SKIN_COLOR 时为 ARGB 整数值）
- ClothItemID `[推断]` 读取 Main sheet ClothItemID 列当前最大值 +1，自动推断无需询问
- MiscAnimationSetID `[输入]` 用 AskUserQuestion 询问"本次是否有庆祝动作？"，选项A为"留空（不使用）- 无庆祝动作 - 默认值"，选项B为"有庆祝动作"。选B则读取该列当前非零最大值 +1 自动推断

**每收集完一个 [输入] 字段后立即更新 checklist。推断字段可在首次问答后批量标注为 [x]。**

**所有字段确认完毕后展示：**
```
### 3.5 Main ✅ 完成
- [x] ID: {值}
- [x] 备注: {值}（推断）
... （全部 [x]）
```

**阶段 3 全部完成后展示：**
```
### 阶段 3 ✅ 全部完成
- [x] 3.1 UniformPanel（9字段）
- [x] 3.2 PicPanel（行1×7字段 + 行2×3字段）
- [x] 3.3 VideoPanel（5字段）
- [x] 3.4 IntroPanel（N字段）
- [x] 3.5 Main（30字段）
```

---

## 阶段 4：汇总确认

> **进入条件**：阶段 3 全部 ✅
> **完成条件**：用户确认汇总表无误

将所有 sheet 的完整数据以表格形式展示给用户：

```
=== 本次写入数据汇总 ===

[UniformPanel] （如有）
  ID: ...
  ClothesType: ...
  ...

[PicPanel - 行1（页签1）]
  ID: ...
  备注: ...
  ...

[PicPanel - 行2（页签2）]
  ID: ...
  ...

[VideoPanel] （如有）
  ...

[IntroPanel]
  ...

[Main]
  ID: ...
  ...
```

询问用户：**以上数据是否确认无误？确认后将写入 PlayerSkin.xlsx。**

阶段 4 完成标志：用户明确回复"确认"或"开始写入"。

---

## 阶段 5：写入 Excel

> **进入条件**：阶段 4 用户确认 ✅
> **完成条件**：所有 sheet 写入成功，验证通过

**进入阶段5时展示初始 checklist：**
```
### 阶段 5 进度
- [ ] 5.1 文件锁定检查
- [ ] 5.2 生成 skin_data.json
- [ ] 5.3 dry-run 预演
- [ ] 5.4 实际写入
- [ ] 5.5 验证写入结果
- [ ] 5.6 清理临时文件
```

**每完成一个步骤后立即更新 checklist，例如：**
```
### 阶段 5 进度
- [x] 5.1 文件锁定检查：未锁定 ✅
- [x] 5.2 生成 skin_data.json ✅
- [ ] 5.3 dry-run 预演
- [ ] 5.4 实际写入
- [ ] 5.5 验证写入结果
- [ ] 5.6 清理临时文件
```

### 步骤 5.1：检查文件锁定

```bash
ls "F:/OL2wc/NBA2KOL2Doc_proj/~\$PlayerSkin.xlsx" 2>/dev/null && echo "文件被锁定，请先关闭Excel" || echo "文件未锁定，可以写入"
```

若有锁定文件，停止并提示用户关闭 Excel。**完成后更新 checklist，5.1 标为 [x]。**

### 步骤 5.2：生成 skin_data.json

将阶段 3 确认的所有字段组装为 JSON 文件，写入当前工作目录下的 `skin_data.json`。该文件为临时文件，步骤 5.6 完成后需删除。

列号为字符串键，空值字段不填：

```json
{
  "PicPanel": [
    {"1": 142, "2": "...", "3": "...", "6": 994, "7": 509},
    {"1": 143, "2": "...", "3": "..."}
  ],
  "VideoPanel": [
    {"1": 68, "2": "Bdg_TCSlithery", "3": "...", "4": "..."}
  ],
  "IntroPanel": [
    {"1": 68, "2": "...", ...}
  ],
  "Main": [
    {"1": 70068, "2": "...", ...}
  ]
}
```

注意：
- 列号从 `1` 开始（对应 Excel 列 A=1, B=2...）
- 空值字段不填入 JSON（脚本会跳过）
- 数字值写数字，不要写成字符串

**生成后更新 checklist，5.2 标为 [x]。**

### 步骤 5.3：预演确认（dry-run）

```bash
python <skill_dir>/scripts/write_skin_rows.py --data skin_data.json --dry-run
```

确认输出无误后，执行实际写入。**完成后更新 checklist，5.3 标为 [x]。**

### 步骤 5.4：执行写入

```bash
python <skill_dir>/scripts/write_skin_rows.py --data skin_data.json
```

脚本会：
1. 检测锁定文件（`~$PlayerSkin.xlsx`），有则中止
2. 按依赖顺序逐 sheet 写入（UniformPanel → PicPanel → VideoPanel → IntroPanel → Main）
3. 写入前验证 ID 是否已存在（防重复）
4. 逐列写入，空值字段跳过
5. 写入后读回验证 ID
6. 保存并关闭（finally 块保证执行）

**写入成功后更新 checklist，5.4 标为 [x]。**

### 步骤 5.5：验证写入结果并输出改动清单

写入成功后，**必须**运行验证脚本，对本次所有改动逐行逐列读回核对：

```bash
python <skill_dir>/scripts/verify_skin_rows.py --data skin_data.json
```

脚本会：
1. 按 ID 在每个 sheet 中查找对应行
2. 逐列对比期望值与 Excel 实际值
3. 输出每个字段的 ✓/✗ 状态
4. 在末尾打印完整改动清单汇总及整体 PASS/FAIL 结论

**验证报告示例：**
```
=== PlayerSkin 写入验证 ===

============================================================
Sheet: PicPanel
============================================================

  ✓ ID=142 行验证通过:
    ✓ 列1(A): 142
    ✓ 列2(B): '朱利叶斯.欧文(75版) 页签1 时刻介绍'
    ✓ 列3(C): 'Skin\\Julius_Erving\\L_Bkg_70068_Intro.dds'
    ...

改动清单汇总（共 XX 个字段）

[PicPanel]
  ID=142:
    ✓ 列1(A): 142
    ✓ 列2(B): '朱利叶斯.欧文(75版) 页签1 时刻介绍'
    ...
[Main]
  ID=70068:
    ✓ 列1(A): 70068
    ...

✓ 验证通过：全部 XX 个字段已正确写入 Excel
```

若出现 ✗ 字段，说明写入有误，需要排查后重新写入。

将验证报告的改动清单完整展示给用户，作为本次配表的最终确认。

**验证完成后更新 checklist，5.5 标为 [x]，附注验证结果（如"69/72字段通过"）。**

### 步骤 5.6：清理临时文件

验证通过后，删除本次 skill 执行过程中产生的所有临时文件：

```bash
rm -f skin_data.json tmp_*.json tmp_*.py
```

**清理完成后展示阶段5最终 checklist：**
```
### 阶段 5 ✅ 全部完成
- [x] 5.1 文件锁定检查：未锁定
- [x] 5.2 skin_data.json 已生成
- [x] 5.3 dry-run 预演：通过
- [x] 5.4 实际写入：成功（UniformPanel/PicPanel/VideoPanel/IntroPanel/Main）
- [x] 5.5 验证：{N}/{总} 字段通过
- [x] 5.6 临时文件已清理
```

---

## 路径命名速查

| 资产用途 | 路径规律 |
|----------|----------|
| 皮肤头像 / Avatar | `Skin\{文件夹名}\head_{MainID}.dds` |
| 换衣间图 | `Skin\{文件夹名}\changingroom_{MainID}.dds` |
| 球员全身图 | `Skin\{文件夹名}\skin{MainID}.dds`（无下划线） |
| 合卡文字图 | `Skin\{文件夹名}\textskin_{MainID}.dds` |
| 出场背景 | `Skin\{文件夹名}\Intro_R_Bkg.dds` |
| 标题图 | `Skin\{文件夹名}\Title_{MainID}.dds` |
| 页签1背景 | `Skin\{文件夹名}\L_Bkg_{MainID}_Intro.dds` |
| 页签2背景 | `Skin\{文件夹名}\L_Bkg_{MainID}_Scene.dds` |
| 徽章背景 | `Skin\{文件夹名}\L_Bkg_{MainID}_Badge.dds` |
| 入场视频封面 | `Skin\{文件夹名}\Entrance_{MainID}.dds` |
| 入场视频 | `Skin\{文件夹名}\V_Entrance_{MainID}.usm` |
| 徽章视频 | `Skin\{文件夹名}\V_{版本缩写}{球员英文名}_Bdg_{徽章类型}_TC.usm`（版本缩写=版本标签括号内数字，如75版→`75`） |
| 球衣背景 | `Skin\{文件夹名}\Jersey_Bkg.dds` |
| 主场球衣 | `Skin\{文件夹名}\Jersey_Home_{MainID}`（无扩展名） |
| 客场球衣 | `Skin\{文件夹名}\Jersey_Away_{MainID}`（无扩展名） |

---

## ⚠️ 尚未完整定义的关联表（待补充）

遇到以下场景时，**必须明确告知用户**规则尚未录入，并按以下方式处理：

| 关联表 | 触发场景 | 处理方式 |
|--------|----------|----------|
| `PlayerSkin.xlsx` CelebratePanel sheet | 用户选择了庆祝动作（MiscAnimationSetID 非空） | 询问用户提供 CelebratePanel 的字段值（ID、各列内容），手工记录后写入 skin_data.json 的 `"CelebratePanel"` 键下，write_skin_rows.py 已支持该 sheet 写入 |
| `SerialRule.xlsx` Main sheet | 陈列室大时刻 SerialRuleID ≠ 0 | 提示用户需手动在 SerialRule.xlsx 中新增对应的贴纸规则行，skill 不负责该表写入 |

**CelebratePanel 字段收集模板**（用于询问用户）：
```
CelebratePanel 规则尚未录入本技能，需要您手动提供以下字段：
- ID：（推断值为 CelebratePanel 当前最大 ID +1 = {值}）
- 各列内容：请参考已有行的格式填写

如您提供字段值，我会一并写入 PlayerSkin.xlsx。如暂时不配置，可跳过此项，后续手动补充。
```

---

## 通用 Excel 写入安全规范

### 1. 写N行 = 先插N个空行

在表格中间插入多行数据时，**必须先在同一位置连续插入N个空行**：

```python
insert_pos = max_row + 1
for _ in range(N):
    sheet.range(f'A{insert_pos}').api.EntireRow.Insert()
# 验证原数据未被覆盖
assert int(sheet.range(insert_pos + N, 1).value) == expected_next_id
```

### 2. 格式继承

写入数据前，先从上一行复制整行格式：

```python
sheet.range(f'{prev_row}:{prev_row}').api.Copy()
sheet.range(f'{first_new_row}:{last_new_row}').api.PasteSpecial(Paste=-4122)
app.api.CutCopyMode = False
```

### 3. 路径字符串

- Python 中用单转义：`'Skin\\Kawhi_Leonard\\PSP70071'`
- 不要双转义：~~`'Skin\\\\Kawhi_Leonard\\\\'`~~
- Icon 路径统一不带 .dds 后缀（CommonExchange、Item 表均适用）

### 4. 插入后行号偏移

插入行后，后续操作必须**重新扫描**获取最新行号，不得使用插入前缓存的行号。

### 5. 写入后必须验证

- 逐单元格读回对比
- 验证上下文完整性（上方/下方原数据未被覆盖）
- 验证相邻列未被污染

### 6. 错误恢复策略

**写入失败或验证不通过时，按以下顺序处理：**

1. **立即停止**：不要继续后续阶段，避免错上加错
2. **诊断原因**：读取当前 Excel 状态，确认是部分写入还是完全失败
3. **用户确认**：将错误详情展示给用户，等待用户指示
4. **恢复方式**（按场景）：
   - **ID 重复 / 已存在**：说明该 ID 已被占用，建议用户检查是否为之前配置的残留，确认后跳过或分配新 ID
   - **验证不通过（部分字段错误）**：如果用户要求回滚重配，需先手动删除已写入的行（告知用户行号），然后从阶段4开始重新走流程；不要尝试局部修正
   - **文件锁定**：提示用户关闭 Excel，然后从当前步骤重试
   - **脚本报错（Python 异常）**：xlwings 的 finally 块会保证 app.quit()，Excel 进程不会残留；检查错误信息后重试
5. **SVN 安全网**：提醒用户重要操作前先 SVN commit，写入失败时可通过 SVN revert 恢复

---

## 阶段 6~11：关联表配置

> **进入阶段 6 时，必须先读取详细规则文件：**
> ```
> read_file: <skill_dir>/references/stages-6-11.md
> ```
> 该文件包含 Equipment / Condition / ClothesSet / ID2StringMapTable / Item / CommonExchange 六张表的完整字段规则、JSON 示例和操作流程。

以下为各阶段摘要（详细规则见 `references/stages-6-11.md`）：

| 阶段 | 表格 | 操作 | 脚本 |
|------|------|------|------|
| **6+7** | Equipment + Condition | 新增 Equip_PlayerSkin（70XXX）+ Equip_Clothes（88XXX）两行；首次配置时同步新增 Condition | `write_equipment.py` |
| **8** | ClothesSet | 新增1行（88XXX），需收集 HomeUniformID/AwayUniformID | `write_clothesset.py` |
| **9** | ID2StringMapTable | 追加 PlayerName/TitleDes/TipsDes 本地化文本 | `write_id2string.py` |
| **10** | Item | 碎片×2+完整×2+服装×2，80XXX 中间插入 + 88XXX 末尾追加 | `write_item.py` |
| **11** | CommonExchange | 合成+分解行（<10000号段），写完后回填 Item 碎片 UseLinkID | `write_exchange.py` |

所有写入脚本均支持 `--dry-run`，均内置锁定检查、格式继承、ID 占用校验、写入后验证。
