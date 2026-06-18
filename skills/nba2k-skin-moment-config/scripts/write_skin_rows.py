"""
write_skin_rows.py
用途：向 PlayerSkin.xlsx 各 sheet 写入新皮肤条目
      接受 JSON 格式的行数据，按指定顺序逐表写入

用法：
    python write_skin_rows.py --data skin_data.json
    python write_skin_rows.py --data skin_data.json --dry-run

skin_data.json 格式示例见本文件末尾的 EXAMPLE 注释

依赖：xlwings（写入时必须使用，读取使用 openpyxl）
"""

import argparse
import json
import os
import sys

try:
    import xlwings as xw
except ImportError:
    print("ERROR: 缺少 xlwings，请先安装：pip install xlwings")
    sys.exit(1)

try:
    import openpyxl
except ImportError:
    print("ERROR: 缺少 openpyxl，请先安装：pip install openpyxl")
    sys.exit(1)

FILE_PATH = r"F:\OL2wc\NBA2KOL2Doc_proj\PlayerSkin.xlsx"

# 写入顺序（依赖链从底层到顶层，UserInfoPanel 在 Main 之后独立写入）
WRITE_ORDER = ["UniformPanel", "PicPanel", "VideoPanel", "CelebratePanel", "IntroPanel", "Main", "UserInfoPanel"]


def check_lock():
    lock = os.path.join(os.path.dirname(FILE_PATH), "~$" + os.path.basename(FILE_PATH))
    if os.path.exists(lock):
        print(f"ERROR: 检测到锁定文件 {lock}")
        print("请先关闭 Excel 中的 PlayerSkin.xlsx，然后重试")
        sys.exit(1)


def get_last_data_row(ws_openpyxl):
    """用 openpyxl 读取最后一个有效数据行号（1-based）"""
    last_row = 1
    for row in ws_openpyxl.iter_rows(values_only=False):
        if row[0].value is not None:
            try:
                int(row[0].value)
                last_row = row[0].row
            except (ValueError, TypeError):
                pass
    return last_row


def write_sheet(wb_xw, wb_openpyxl, sheet_name, rows_data, dry_run=False):
    """
    向指定 sheet 写入一行或多行数据
    rows_data: list of dict，每个 dict 格式为 {列号(1-based): 值}
    """
    if sheet_name not in [s.name for s in wb_xw.sheets]:
        print(f"  ERROR: sheet '{sheet_name}' 不存在，跳过")
        return False

    ws_xw = wb_xw.sheets[sheet_name]
    ws_opx = wb_openpyxl[sheet_name]
    last_row = get_last_data_row(ws_opx)

    for i, row_data in enumerate(rows_data):
        # JSON key 为字符串，统一转为整数
        row_data = {int(k): v for k, v in row_data.items()}
        target_id = row_data.get(1)
        new_row = last_row + 1 + i

        # 写入前验证：检查该 ID 是否已存在
        existing_id = ws_xw.range(new_row, 1).value
        if existing_id is not None:
            try:
                if int(existing_id) == int(target_id):
                    print(f"  [SKIP] {sheet_name} ID={target_id} 已存在，跳过")
                    continue
                else:
                    print(f"  WARNING: 行 {new_row} 已有数据（ID={existing_id}），不覆盖")
                    continue
            except (ValueError, TypeError):
                pass

        print(f"  {'[DRY-RUN] ' if dry_run else ''}写入 {sheet_name} 行 {new_row}：ID={target_id}")

        if not dry_run:
            # 逐列写入，空值字段跳过（不写 None 或空字符串）
            for col, val in row_data.items():
                if val is None or val == "":
                    continue  # 空值保持单元格为空
                # 数字类型确保写入 int（而非 float 或字符串）
                if isinstance(val, float) and val == int(val):
                    val = int(val)
                cell = ws_xw.range(new_row, col)
                cell.value = val
                cell.api.HorizontalAlignment = -4131  # xlLeft 左对齐

            # 写入后验证
            verify_id = ws_xw.range(new_row, 1).value
            try:
                assert int(verify_id) == int(target_id), f"验证失败：期望 {target_id}，实际 {verify_id}"
                print(f"    [OK] 验证通过")
            except AssertionError as e:
                print(f"    [FAIL] {e}")
                return False

    return True


def main():
    parser = argparse.ArgumentParser(description="向 PlayerSkin.xlsx 写入新皮肤条目")
    parser.add_argument("--data", "-d", required=True, help="JSON 数据文件路径")
    parser.add_argument("--dry-run", action="store_true", help="预演模式，只打印不实际写入")
    parser.add_argument("--excel-dir", default=None, help="Excel 文件目录（默认使用内置路径）")
    args = parser.parse_args()

    # 读取数据文件
    if not os.path.exists(args.data):
        print(f"ERROR: 数据文件不存在：{args.data}")
        sys.exit(1)

    with open(args.data, "r", encoding="utf-8") as f:
        skin_data = json.load(f)

    file_path = FILE_PATH
    if args.excel_dir:
        file_path = os.path.join(args.excel_dir, "PlayerSkin.xlsx")

    print(f"=== PlayerSkin 写入工具 {'[预演模式]' if args.dry_run else ''} ===")
    print(f"数据文件：{args.data}")

    # 检查锁定文件
    lock_file = os.path.join(os.path.dirname(file_path), "~$" + os.path.basename(file_path))
    if os.path.exists(lock_file):
        print(f"ERROR: 检测到锁定文件 {lock_file}")
        print("请先关闭 Excel 中的 PlayerSkin.xlsx，然后重试")
        sys.exit(1)

    # 用 openpyxl 读取末尾行信息（只读）
    wb_opx = openpyxl.load_workbook(file_path, read_only=True, data_only=True)

    app = None
    wb_xw = None

    try:
        if not args.dry_run:
            app = xw.App(visible=False)
            app.display_alerts = False
            app.screen_updating = False
            wb_xw = app.books.open(file_path)
        else:
            # dry-run 时用 openpyxl 模拟（不实际写入）
            wb_xw = None

        success = True
        for sheet_name in WRITE_ORDER:
            if sheet_name not in skin_data:
                continue

            rows = skin_data[sheet_name]
            if not isinstance(rows, list):
                rows = [rows]  # 兼容单行写法

            print(f"\n--- {sheet_name} ({len(rows)} 行) ---")

            if not args.dry_run:
                ok = write_sheet(wb_xw, wb_opx, sheet_name, rows, dry_run=False)
            else:
                # dry-run 只打印
                for row in rows:
                    row_int = {int(k): v for k, v in row.items()}
                    print(f"  [DRY-RUN] 将写入 ID={row_int.get(1)}：{row_int}")
                ok = True

            if not ok:
                print(f"  ERROR: {sheet_name} 写入失败，中止")
                success = False
                break

        if not args.dry_run and success and wb_xw is not None:
            print("\n保存文件...")
            # 先关闭 openpyxl 只读 workbook，释放文件锁
            wb_opx.close()
            wb_opx = None
            wb_xw.save(file_path)
            wb_xw.close()
            wb_xw = None
            print("[OK] 保存成功")

    except Exception as e:
        print(f"\nERROR: 写入异常：{e}")
        import traceback
        traceback.print_exc()
        success = False

    finally:
        if wb_opx is not None:
            wb_opx.close()
        if wb_xw and not args.dry_run:
            try:
                wb_xw.close()
            except Exception:
                pass
        if app:
            try:
                app.quit()
            except Exception:
                pass
        # 检查残留锁定文件
        if not args.dry_run and os.path.exists(lock_file):
            print(f"警告：仍有锁定文件残留，请手动删除：{lock_file}")

    if not success:
        sys.exit(1)
    print("\n[OK] 所有 sheet 写入完成")


# =============================================================================
# EXAMPLE: skin_data.json 格式说明
# =============================================================================
# {
#   "PicPanel": [
#     {
#       "1": 142,          列1: ID
#       "2": "朱利叶斯.欧文(75版) 页签1 时刻介绍",  列2: 备注
#       "3": "Skin\\Julius_Erving\\L_Bkg_70068_Intro.dds",  列3: BkgRes
#       "4": "Skin\\Julius_Erving\\Entrance_70068.dds",     列4: VideoPic（可留空则不填此键）
#       "5": "Skin\\Julius_Erving\\V_Entrance_70068.usm",   列5: VideoRes
#       "6": 994,          列6: PostionX
#       "7": 509           列7: PostionY
#     },
#     {
#       "1": 143,
#       "2": "朱利叶斯.欧文(75版) 页签2 卡面效果",
#       "3": "Skin\\Julius_Erving\\L_Bkg_70068_Scene.dds"
#       // 列4~7 不填（留空）
#     }
#   ],
#   "VideoPanel": [
#     {
#       "1": 68,
#       "2": "Bdg_TCSlithery",
#       "3": "Skin\\Julius_Erving\\L_Bkg_70068_Badge.dds",
#       "4": "Skin\\Julius_Erving\\V_75Julius_Erving_Bdg_Slithery_TC.usm"
#     }
#   ],
#   "IntroPanel": [ ... ],
#   "Main": [ ... ]
# }
# 注意：
# - 列号为字符串键（JSON 不支持整数键），写入时会转换为 int
# - 空值字段不填（不要填 null 或 ""），脚本会跳过不写入
# - 数字值写数字，不要写成字符串
# =============================================================================

if __name__ == "__main__":
    main()
