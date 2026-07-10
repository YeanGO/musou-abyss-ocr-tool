from pathlib import Path
import json

from PIL import Image


def load_boxes(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def crop_image(image_path, boxes, output_dir):
    """Crop normalized [x1, y1, x2, y2] boxes and return their file paths."""
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    for field, (x1, y1, x2, y2) in boxes.items():
        pixels = (round(x1 * width), round(y1 * height), round(x2 * width), round(y2 * height))
        target = output_dir / f"{field}.png"
        image.crop(pixels).save(target)
        results[field] = target
    return results
