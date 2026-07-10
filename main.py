import argparse
from pathlib import Path

from src.cropper import crop_image, load_boxes
from src.csv_writer import FIELDS, write_drafts
from src.ocr import recognise_images
from src.parser import parse_raw
from src.trait_mapper import TraitMapper

ROOT = Path(__file__).resolve().parent
RAW_FIELDS = ["name", "level", "traits", "summonSkill", "summonUpgradeConditions", "uniqueTactic", "uniqueTacticConditions", "effects"]


def prompt(label, value):
    shown = str(value).replace("\n", " / ")
    answer = input(f"{label} [{shown}]: ").strip()
    return answer if answer else value


def interactive_edit(raw, parsed):
    print("\n按 Enter 保留目前值；可直接輸入新文字覆蓋。")
    for key in RAW_FIELDS:
        raw[key] = prompt(key, raw.get(key, ""))
    print("\n以下為可直接寫入 CSV 的欄位：")
    for key in FIELDS:
        parsed[key] = prompt(key, parsed.get(key, ""))


def main():
    cli = argparse.ArgumentParser(description="無雙深淵英傑截圖 OCR 草稿匯入工具")
    cli.add_argument("--image", required=True, help="遊戲英傑資訊截圖路徑")
    cli.add_argument("--interactive", action="store_true", help="逐欄確認與修改結果")
    args = cli.parse_args()
    image = Path(args.image)
    if not image.exists():
        cli.error(f"找不到圖片：{image}")

    crops = crop_image(image, load_boxes(ROOT / "config" / "crop_boxes.json"), ROOT / "output" / "crops")
    raw = {field: "" for field in RAW_FIELDS}
    try:
        raw.update(recognise_images(crops))
    except RuntimeError as error:
        if not args.interactive:
            cli.error(str(error))
        print(f"OCR 未執行：{error}")
        print("請依裁切圖片手動輸入欄位。")

    mapper = TraitMapper(ROOT / "data" / "traits.csv", ROOT / "data" / "trait_aliases.csv")
    parsed, warnings = parse_raw(raw, mapper)
    if args.interactive:
        interactive_edit(raw, parsed)
        # Recalculate warnings only for values the user left in raw OCR; direct CSV edits are intentional.
        _, warnings = parse_raw(raw, mapper)
    write_drafts(raw, parsed, warnings, ROOT / "output")
    print("\n已建立 output/officer-draft.json 與 output/officer-draft.csv")
    print("裁切圖片在 output/crops/")
    if warnings:
        print("Warnings：")
        for warning in warnings:
            print(f"- {warning}")


if __name__ == "__main__":
    main()
