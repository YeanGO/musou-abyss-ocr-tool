import os
from pathlib import Path


def recognise_images(crop_paths, language="japan"):
    """Run PaddleOCR for every crop (compatible with PaddleOCR 2.x and 3.x)."""
    try:
        # PaddleOCR 3.x otherwise stores models under the user home directory.
        # Keeping its cache inside this project prevents a broken or restricted
        # ~/.paddlex cache from stopping the tool.
        project_root = Path(__file__).resolve().parents[1]
        os.environ.setdefault("PADDLE_PDX_CACHE_HOME", str(project_root / ".paddlex-cache"))
        from paddleocr import PaddleOCR
    except ImportError as error:
        raise RuntimeError(
            "PaddleOCR is unavailable. Install requirements.txt, or use --interactive to enter values manually."
        ) from error

    try:
        if hasattr(PaddleOCR, "predict"):
            # Screenshot crops do not need the heavyweight document correction
            # pipeline. Disabling it also avoids downloading/reading UVDoc.
            ocr = PaddleOCR(
                lang=language,
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
            )
        else:
            ocr = PaddleOCR(lang=language, use_angle_cls=True)
    except Exception as error:
        raise RuntimeError(f"PaddleOCR 無法初始化：{error}") from error
    values = {}
    try:
        for field, path in crop_paths.items():
            lines = []
            if hasattr(ocr, "predict"):
                # PaddleOCR 3.x: predict() returns result objects/dictionaries,
                # with recognised strings in the rec_texts field.
                for page in ocr.predict(str(path)):
                    try:
                        texts = page.get("rec_texts", [])
                    except AttributeError:
                        texts = page["rec_texts"] if "rec_texts" in page else []
                    lines.extend(str(text) for text in texts if str(text).strip())
            else:
                # PaddleOCR 2.x legacy result format.
                for page in ocr.ocr(str(path), cls=True) or []:
                    for item in page or []:
                        lines.append(item[1][0])
            values[field] = "\n".join(lines)
    except Exception as error:
        raise RuntimeError(f"PaddleOCR 辨識失敗：{error}") from error
    return values
