def recognise_images(crop_paths, language="japan"):
    """Run PaddleOCR for every crop. Import lazily so manual mode still works."""
    try:
        from paddleocr import PaddleOCR
    except ImportError as error:
        raise RuntimeError(
            "PaddleOCR is unavailable. Install requirements.txt, or use --interactive to enter values manually."
        ) from error

    ocr = PaddleOCR(lang=language, use_angle_cls=True)
    values = {}
    for field, path in crop_paths.items():
        result = ocr.ocr(str(path), cls=True)
        lines = []
        for page in result or []:
            for item in page or []:
                lines.append(item[1][0])
        values[field] = "\n".join(lines)
    return values
