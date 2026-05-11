---
name: 2D精灵生成
description: "2D游戏精灵生成技能。当用户需要生成游戏角色、怪物、NPC、法术特效、投射物、道具等2D游戏美术资产时使用此技能。支持像素风/HD风格，自动生成精灵表（sprite sheet）、逐帧PNG和GIF动图，并完成去背景后处理。触发词：生成精灵/sprite、生成角色/怪物/NPC、生成法术/特效/投射物、生成游戏资产、制作pixel art、generate sprite/character/monster/effect。"
---

# generate2dsprite（WorkBuddy / CodeBuddy 适配版）

基于 [agent-sprite-forge](https://github.com/0x0funky/agent-sprite-forge) 改造，适配 WorkBuddy/CodeBuddy Agent 环境。

**与原版差异：**
- ✅ 使用内置 `image_gen` 生成图像（保持不变）
- ✅ 使用本地 Python 脚本做后处理（去背、切帧、GIF 导出）
- ❌ 不使用 `view_image`（不在工具集内，改为用 `read_file` 读图片或跳过参考图流程）
- ❌ 不依赖 `$CODEX_HOME` 路径，图片路径由 `image_gen` 工具直接返回

---

## 脚本路径（固定，不要修改）

```
SCRIPT  = C:\Users\tiannuoxie\真心姑娘\agent-sprite-forge-main\skills\generate2dsprite-workbuddy\scripts\generate2dsprite.py
PYTHON  = C:\Users\tiannuoxie\AppData\Local\Programs\Python\Python310\python.exe
```

---

## 参数推断

从用户需求自动判断，**不要问用户网格大小或帧数**：

| 参数 | 可选值 |
|------|--------|
| `asset_type` | player / npc / creature / character / spell / projectile / impact / prop / summon / fx |
| `action` | single / idle / cast / attack / shoot / jump / hurt / combat / walk / run / hover / charge / projectile / impact / explode / death |
| `art_style` | pixel_art / clean_hd / pixel_inspired / retro_pixel |
| `sheet` | 2x2 / 2x3 / 3x3 / 3x4 / 4x4 / 1x4 等 |

**`--target` 映射（脚本参数）：**
- `creature` / `npc` / `player` → 直接对应
- 其他所有类型 → `asset`

---

## 网格默认值

| 动作/场景 | 网格 | `--target` | `--mode` |
|-----------|------|-----------|---------|
| idle（小/中型） | 2x2 | creature/asset | idle |
| idle（大型boss） | 3x3 | creature | idle |
| cast / death | 2x3 | asset | cast / death |
| attack / hurt / combat / walk / run / fx | 2x2 | creature/asset | 对应名称 |
| projectile | 1x4 | asset | projectile |
| 4方向行走（RPG主角） | 4x4 | player | player_sheet |

---

## 工作流（严格按此顺序执行）

### 步骤1：推断资产方案

根据用户描述确定：`asset_type`、`action`、`sheet`（rows x cols）、`art_style`、`output_dir`。

`output_dir` 默认值：`C:\Users\tiannuoxie\WorkBuddy\sprites\<描述slug>\`

### 步骤2：写 image_gen prompt

**必须包含的约束（每次都要写）：**

```
solid #FF00FF background, no gradients, no shadow
exact <rows>x<cols> grid, <N> equal cells, NO borders NO lines between cells
NO text, NO labels, NO numbers anywhere
same character/asset identity in every cell, same bounding box, same pixel scale
nothing crosses cell edges, full body inside central 60-70% safe area
```

**art_style 选择：**
- 像素风角色/怪物 → `pixel art, strong outlines, dynamic`
- HD 地图道具 → `clean hand-painted HD game art`
- 混合 → `pixel-inspired`

### 步骤3：调用 image_gen

```
size: 1024x1024
quality: medium
output_dir: <output_dir>
```

### 步骤4：后处理（必须执行）

`image_gen` 返回路径后，立即执行：

```powershell
C:\Users\tiannuoxie\AppData\Local\Programs\Python\Python310\python.exe `
  "C:\Users\tiannuoxie\真心姑娘\agent-sprite-forge-main\skills\generate2dsprite-workbuddy\scripts\generate2dsprite.py" `
  process `
  --input "<image_gen返回的PNG绝对路径>" `
  --target <asset|creature|player|npc> `
  --mode <idle|combat|walk|cast|attack|hurt|hover|charge|projectile|impact|explode|death|fx|single|player_sheet> `
  --rows <N> `
  --cols <N> `
  --output-dir "<output_dir>" `
  --align <bottom|center> `
  --component-mode <largest|all> `
  --shared-scale
```

**参数选择规则：**
- `--align bottom`：有脚的角色、怪物、NPC
- `--align center`：漂浮特效、投射物、法术
- `--component-mode largest`：body 类资产（角色/怪物/NPC）
- `--component-mode all`：特效/投射物/impact（保留所有组件）
- `--shared-scale`：多帧资产默认加（保持帧间比例一致）

### 步骤5：交付

用 `deliver_attachments` 交付（按重要性排序）：
1. `<output_dir>/sheet-transparent.png`
2. `<output_dir>/animation.gif`
3. （可选）逐帧 PNG：`<output_dir>/frame-*.png` 或对应 label 名称

---

## QC 检查

读取 `pipeline-meta.json`，检查：
- `edge_touch_frames` 是否为空（为空=优秀，有值=某帧碰边需注意）
- 每帧 `edge_touch: false` = 通过

---

## 触发示例

```
生成一个火焰狼怪物的 idle 动画
生成像素风法师施法动画（cast）
生成顶视角RPG主角四方向行走精灵表
生成火球投射物飞行循环
生成大型boss idle，3x3网格
```

---

## 参考文件

- `references/modes.md`：asset_type、action、bundle、sheet 选择指南
- `references/prompt-rules.md`：prompt 写法规范
- `scripts/generate2dsprite.py`：后处理脚本
- `scripts/make_layout_guide.py`：可选布局参考图生成器

---

## 用户偏好

（记录 Summer哥 的固定习惯，触发 skill 时自动带入，无需每次重复说）

- **默认美术风格**：pixel_art，除非明确说 HD 或 clean_hd
- **默认输出目录**：`C:\Users\tiannuoxie\WorkBuddy\sprites\<描述slug>\`
- **命名偏好**：简洁务实，不要中二/夸张命名
- **游戏背景**：考虑制作独立游戏，类型待确定，具备0-1策划经验

---

## 踩坑经验

（以下由 AI 在实际调用中自动积累，经历 2 次及以上尝试才成功的情况）

- `process` 命令 / 必填参数遗漏：`--target` 和 `--mode` 是必填参数，不是可选的。`--target` 取值：`asset`/`creature`/`player`/`npc`；`--mode` 取值对应动作名。最初 SKILL.md 里遗漏了这两个参数，导致脚本报错。
- `--target` 映射 / 非标准 asset_type：除 creature/npc/player 外，所有类型（spell/projectile/impact/prop/summon/fx/character）统一映射为 `asset`，不能直接用 asset_type 名称。
