---
name: 2D地图生成
description: "2D游戏地图/场景生成技能。当用户需要生成游戏地图、场景背景、RPG地图、横版关卡、塔防场景、平台跳跃关卡、视差背景等2D游戏场景资产时使用此技能。支持像素风/HD风格，生成底图、分层地图、道具包、碰撞元数据，以及可导入Godot/Unity的场景文件。触发词：生成地图/场景/关卡、生成背景、制作RPG地图、生成横版场景、生成视差背景、generate map/scene/level/background。"
---

# generate2dmap（WorkBuddy / CodeBuddy 适配版）

基于 [agent-sprite-forge](https://github.com/0x0funky/agent-sprite-forge) 改造，适配 WorkBuddy/CodeBuddy Agent 环境。

**与原版差异：**
- ✅ 使用内置 `image_gen` 生成图像（保持不变）
- ✅ 使用本地 Python 脚本做道具提取和预览合成
- ❌ 去掉 `view_image`：视觉参考改为通过对话中已显示的图片实现（用户粘贴图片进对话）
- ❌ 不依赖 `$CODEX_HOME` 路径，所有路径由 `image_gen` 工具直接返回

**脚本路径（固定）：**
```
SCRIPTS = C:\Users\tiannuoxie\真心姑娘\agent-sprite-forge-main\skills\generate2dmap-workbuddy\scripts\
PYTHON  = C:\Users\tiannuoxie\AppData\Local\Programs\Python\Python310\python.exe
```

---

## 第一步：选择地图模式（map_mode）

这是最重要的第一个决策，从游戏类型自动推断：

| 游戏类型 | map_mode |
|---------|---------|
| RPG / 宠物捕捉 / 俯视角探索 | `tile_mode` |
| 塔防 / 幸存者类 / 俯视角竞技场 | `scene_mode` |
| 横版动作 / 跑酷 / 银河城 | `side_scroll_mode` |
| 战棋 / 工厂自动化 / 棋盘类 | `grid_mode` |
| Roguelike房间 / 模块化地牢 | `room_chunk_mode` |
| 纯背景 / 战斗背景 / 非交互场景 | `baked_scene_mode` |

---

## 核心工作流

### tile_mode / scene_mode（俯视角地图）

```
步骤1：生成 foundation-only 底图（纯地面，无道具无角色）
        image_gen prompt 要点：
        - "ground only, no props, no trees, no rocks, no buildings"
        - "clean top-down RPG map, HD hand-painted style"（或 pixel art）
        - 输出路径：<output_dir>/assets/map/<name>-base.png

步骤2：基于底图生成 dressed-reference（带道具的参考图，不是最终资产）
        prompt 要点：
        - "use the base map above as visual reference"
        - "in-world reference mockup, natural game objects placed on map"
        - "NO labels, NO arrows, NO text, NO UI overlays"
        - 最多9个不同道具候选
        - 输出路径：<output_dir>/assets/map/<name>-dressed-reference.png

步骤3：逐个生成道具（透明PNG，洋红背景 → 后处理去背）
        - compact_prop（小型装饰）→ 3x3 prop_pack
        - wide/tall/碰撞关键 → 单独生成
        - 使用 generate2dsprite skill 的脚本处理

步骤4：提取道具包
        python scripts/extract_prop_pack.py \
          --input <prop_sheet.png> \
          --rows <N> --cols <N> \
          --output-dir <output_dir>/assets/props/<name>/

步骤5：合成分层预览
        python scripts/compose_layered_preview.py \
          --base <base.png> \
          --props-json <props.json> \
          --output <output_dir>/assets/map/<name>-layered-preview.png

步骤6：生成碰撞/区域元数据（JSON）
        写入 <output_dir>/data/<name>-collision.json
        写入 <output_dir>/data/<name>-props.json（道具位置）
```

### side_scroll_mode（横版关卡）

```
步骤0：确定 stage_canvas（默认 1536x864，16:9）

步骤1：生成多层视差背景（每层都是纯景观，无可交互元素）
        - <name>-sky.png      ← 天空/远景
        - <name>-far-bg.png   ← 远处建筑/山脉
        - <name>-mid-bg.png   ← 中景
        - <name>-near-bg.png  ← 近景（无地板/平台）
        所有层必须相同尺寸（stage_canvas）

步骤2：生成 stage-reference（关卡布局参考图，不是最终资产）
        - 显示平台/地形/道具候选的自然摆放
        - 最多9个不同对象候选
        - 不含箭头/标签/spawn点/碰撞标注

步骤3：生成独立平台/地形/道具资产（透明PNG）
        - 平台：platform_strip 1x3 或 1x4（左帽/中间/右帽）
        - 大型道具：单独生成
        - 特效/陷阱：单独生成

步骤4：生成元数据
        - data/<name>-objects.json（平台/道具位置）
        - data/<name>-collision.json（碰撞几何）
        - data/<name>-scene-hooks.json（玩家出生点/触发区/相机边界）

步骤5：合成 stage-preview（仅QA用，不是运行时资产）
```

### baked_scene_mode（纯背景）

```
步骤1：直接 image_gen 生成完整背景图
步骤2：可选生成碰撞/区域元数据
步骤3：交付 PNG + 元数据
```

---

## 道具分类规则（决定生成策略）

| 类型 | 特征 | 生成策略 |
|------|------|---------|
| compact_prop | 小型方正装饰物（石头/灌木/箱子/路灯） | prop_pack 3x3 |
| wide_or_long | 宽高比 > 1.6（平台/桥/栅栏/墙） | 单独生成 或 platform_strip |
| tall_or_large | 高宽比 > 1.6（大树/门/塔/建筑） | 单独生成 |
| collision_bearing | 需要精确碰撞对齐（门/检查点/出口） | 单独生成 |

**绝对不能**把 wide/tall/collision_bearing 类型塞进方形 prop_pack。

---

## image_gen prompt 要点

**底图（foundation-only）必须包含：**
```
ground only, paths, water, terrain boundaries
NO props, NO trees, NO rocks, NO buildings, NO characters
clean top-down 2D RPG game map, HD hand-painted style
sharp readable terrain shapes, no chunky pixels
solid composition, camera from above
```

**视差背景层必须包含：**
```
scenery only, no platforms, no floors, no pickups, no characters
sky / far mountains / distant buildings（根据层级）
same <W>x<H> canvas, same horizon line position
```

**dressed-reference / stage-reference：**
```
use the map/background image above as visual reference
preserve exact camera framing, terrain shapes, horizon
in-world mockup: natural game objects placed as they would appear in game
NO text, NO labels, NO arrows, NO UI overlays, NO highlighted boxes
at most 9 distinct prop/object candidates
```

---

## 脚本用法

```powershell
# 道具包提取（洋红背景 → 透明PNG切割）
C:\Users\tiannuoxie\AppData\Local\Programs\Python\Python310\python.exe `
  "C:\Users\tiannuoxie\真心姑娘\skills\generate2dmap\scripts\extract_prop_pack.py" `
  --input "<prop_sheet.png>" `
  --rows <N> --cols <N> `
  --output-dir "<output_dir>"

# 分层预览合成
C:\Users\tiannuoxie\AppData\Local\Programs\Python\Python310\python.exe `
  "C:\Users\tiannuoxie\真心姑娘\skills\generate2dmap\scripts\compose_layered_preview.py" `
  --base "<base.png>" `
  --props-json "<props.json>" `
  --output "<preview.png>"
```

---

## 输出目录结构

```
<output_dir>/
├── assets/
│   ├── map/
│   │   ├── <name>-base.png
│   │   ├── <name>-dressed-reference.png（或 stage-reference.png）
│   │   ├── <name>-sky.png（side_scroll_mode）
│   │   ├── <name>-far-bg.png
│   │   ├── <name>-mid-bg.png
│   │   ├── <name>-near-bg.png
│   │   └── <name>-layered-preview.png（QA用）
│   └── props/
│       └── <prop_name>/
│           └── prop.png
└── data/
    ├── <name>-props.json
    ├── <name>-collision.json
    └── <name>-scene-hooks.json
```

---

## 交付

用 `deliver_attachments` 按重要性交付：
1. `layered-preview.png` 或 `stage-preview.png`（主要交付物）
2. `base.png` / 视差背景层
3. 道具 PNG 文件
4. JSON 元数据文件

---

## 参考文件

- `references/map-strategies.md`：pipeline 选择指南
- `references/layered-map-contract.md`：分层地图合约
- `references/prop-pack-contract.md`：道具包规范
- `scripts/extract_prop_pack.py`：道具包切割脚本
- `scripts/compose_layered_preview.py`：分层预览合成脚本

---

## 用户偏好

（记录 Summer哥 的固定习惯，触发 skill 时自动带入）

- **默认美术风格**：pixel_art，除非明确说 HD 或 clean_hd
- **默认输出目录**：`C:\Users\tiannuoxie\WorkBuddy\maps\<描述slug>\`
- **视角偏好**：俯视角（top-down），未确定具体游戏类型时默认 tile_mode
- **游戏背景**：考虑制作独立游戏，类型待确定，具备0-1策划经验

---

## 踩坑经验

（以下由 AI 在实际调用中自动积累，经历 2 次及以上尝试才成功的情况）

（暂无，首次使用时记录）
