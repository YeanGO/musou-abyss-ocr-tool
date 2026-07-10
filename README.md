# 無雙深淵英傑截圖 OCR 輔助匯入工具

這是供人工覆核的半自動工具：將《無雙深淵》英傑資訊截圖裁切為固定區域、進行 OCR、解析 traits 與條件，最後輸出一列可供 `musou-abyss-guideWeb` 使用的 CSV 草稿。它只會寫入本專案的 `output/`，絕不會直接修改正式網站或 `officers.csv`。

## 安裝

建議使用 Python 3.10 以上，於此專案資料夾執行：

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## 放入圖片與執行

將英傑資訊截圖放入 `input/screenshots/`，例如 `input/screenshots/sample.jpg`，再執行：

```bash
python main.py --image input/screenshots/sample.jpg
```

若要逐欄確認或修正結果，使用互動模式。按 Enter 會保留方括號中的值，輸入文字會覆蓋該欄。

```bash
python main.py --image input/screenshots/sample.jpg --interactive
```

程式會產生：

- `output/crops/`：各欄位裁切圖，先檢查這裡是否切到正確位置。
- `output/officer-draft.json`：保留原始 OCR、解析結果與 warnings，方便覆核。
- `output/officer-draft.csv`：UTF-8 的單列 CSV 草稿，會自動處理逗號、雙引號與換行。

## 調整裁切位置

`config/crop_boxes.json` 採 normalized coordinates：`[x1, y1, x2, y2]`，每個數字均為圖片寬或高的比例（0 到 1），不是固定像素。不同解析度可共用設定；若 `output/crops/` 顯示裁切錯位，調整這個檔案的比例後重新執行。

## 將人工確認結果接到 guideWeb

先開啟 `output/officer-draft.csv` 與 `output/officer-draft.json` 檢查內容與 warnings。確認後，**手動**將草稿 CSV 中的資料列複製到 `musou-abyss-guideWeb/data-source/officers.csv`；請依該專案既有資料規範補齊或修正 `id`、勢力與待補欄位。此工具不會自動 append 或寫入正式資料。

## 常見問題

### OCR 辨識錯怎麼辦？

使用 `--interactive` 逐欄修正。可優先查看 `output/crops/`，確認問題是 OCR 還是裁切。

### 裁切位置錯怎麼辦？

修改 `config/crop_boxes.json` 的 normalized coordinates，重新執行後比較 `output/crops/`。

### trait 對不起來怎麼辦？

檢查 JSON 的 `warnings`。在 `data/trait_aliases.csv` 增加 OCR 常見誤判（`alias,traitId`）；程式會優先使用 alias，再使用 `data/traits.csv` 的正式名稱。

### PaddleOCR 安裝失敗怎麼辦？

PaddleOCR 與 PaddlePaddle 體積較大，請依你的 Python 版本與平台選擇相容的 PaddlePaddle 套件後再安裝。也可先執行 `--interactive`：即使 OCR 無法載入，程式仍會輸出裁切圖並讓你手動輸入辨識結果。未來也可以改以 `pytesseract` 作為 OCR 引擎。
