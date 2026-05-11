# Example Usage

> Read this file to see concrete end-to-end workflow examples for each image quality mode.

## Example 1: Default Layer (Recommended)

**User request:** "帮我解读这个 Figma 设计并生成文档：https://www.figma.com/design/abc123/RotationSettings?node-id=0-1"

**Workflow:**
1. Extract fileKey (`abc123`), fileName (`RotationSettings`), nodeId (`0:1`)
2. **Phase 1.1:** No `--image-quality` specified → auto-detect
3. **Phase 2:** `get_metadata` for root node → 15 total nodes
4. **Phase 2.1:** "Medium complexity" (15 nodes) → Auto-select Layer 1
   - Report: "检测到中等复杂度设计 (15个节点)。使用 Layer 1 精度 (1/3分辨率截图)，预计增加准确度 +40-60%"
5. Identify 8 key nodes
6. **Phase 3.1:** Per node: `get_metadata` → `get_screenshot(scale=0.333)` → extract visual data
7. **Phase 4:** Aggregate summaries with colors, layout, typography
8. **Phase 5:** Save XML + screenshots + `figma-visual-analysis.json`
9. **Phase 6:** 9-section documentation (+ Visual Design System)

**Result:** Comprehensive doc with color palette extraction, typography, layout analysis.

---

## Example 2: Metadata-Only (--no-images)

**User request:** "分析这个设计，但不要下载图片：https://www.figma.com/design/xyz789/UserFlow?node-id=1:50 --no-images"

**Workflow:**
1. Detected: `--no-images` → Override to Layer 0
   - Report: "参数设置: --no-images。使用 Layer 0 (仅元数据)，零额外 token 开销"
2. **Phase 2:** Root metadata → 45 total nodes
3. **Phase 2.1:** "High complexity" + Layer 0 → Select 8 representative nodes (core flows + annotations)
4. **Phase 3.1:** Metadata only, NO screenshot per node
5. **Phase 4-6:** 8-section documentation, no Visual Design System section

**Result:** Fast generation, 3KB/node, no image tokens.

---

## Example 3: High Precision (--image-quality high)

**User request:** "我需要详细的设计分析，包括色彩、排版、组件规范 --image-quality high"

**Workflow:**
1. Detected: `--image-quality high` → Layer 2 (960×540, ~250 tokens/node)
   - Report: "参数设置: --image-quality high。使用 Layer 2 精度 (1/2分辨率)，预计增加准确度 +50-70%"
2. **Phase 2:** 28 nodes → "Medium-High complexity" → Select 6-8 nodes
3. **Phase 3.1:** Per node: `get_metadata` + `get_screenshot(scale=0.5)`
   - Extract detailed visual info: component styles, border-radius, shadows, detailed color palette
4. **Phase 4:** Enhanced color analysis (10+ colors), typography with line-height/letter-spacing
5. **Phase 6:** Detailed Visual Design System + component visual specifications

**Result:** Highly detailed doc with visual design tokens and accessibility notes.

---

## Example 4: Intent-Detected Layer (no explicit flag)

**User request:** "看看这个设计的色彩系统和布局：https://www.figma.com/design/def456/ColorSystem?node-id=2:100"

**Workflow:**
1. No `--image-quality` parameter
2. **Phase 1.1:** Keyword detection: "色彩" + "布局" → Visual context → Layer 1
   - Report: "检测到需求: 视觉分析 (色彩+布局)。推荐使用 Layer 1 (1/3分辨率)"
3. **Phase 2:** 12 nodes → Auto-confirm Layer 1
4. **Phase 3.1:** Layer 1 two-step sequential
5. **Phase 4-6:** Documentation focused on color system and layout

**Result:** Targeted visual analysis doc tailored to stated interests.
