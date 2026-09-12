---
name: opencv
description: '用於 Python OpenCV（cv2）工作：影像與影片處理、相機擷取、前處理、特徵偵測、輪廓、幾何轉換、校正、物件偵測、效能問題與 cv2 偵錯。'
argument-hint: '請描述 OpenCV 輸入、預期輸出，以及目前的程式碼或錯誤。'
user-invocable: true
---

# OpenCV 開發

使用此工作流程，在 Python 中完成實用且可驗證的電腦視覺變更。

## 使用時機

- 讀取、寫入、調整大小、裁切、標註或轉換影像。
- 擷取、處理或匯出影片與相機影格。
- 實作閾值處理、形態學、輪廓、邊緣、特徵、校正或追蹤。
- 診斷 `cv2` 匯入錯誤、shape/dtype 問題、色彩空間錯誤或處理管線速度過慢。
- 為 OpenCV 行為新增聚焦測試。

## 執行步驟

1. **檢查專案**
   - 找出相關的 Python 入口點與附近的測試。
   - 使用 `python --version` 與 `python -c "import cv2; print(cv2.__version__)"` 檢查目前的直譯器。
   - 若缺少 OpenCV，只安裝一個套件：桌面 GUI 使用 `uv add opencv-python`，CI/伺服器使用 `uv add opencv-python-headless`。

2. **明確定義資料契約**
   - 確認輸入是 BGR、RGB、灰階或 BGRA。
   - 操作前檢查 `shape`、`dtype`、通道數與數值範圍。
   - 使用影像讀取結果或影片擷取結果前，先確認操作是否成功。
   - 像素座標維持 `(x, y)` 順序，陣列索引則使用 `[y, x]` 順序。

3. **實作最小處理管線**
   - 分離 I/O、前處理、視覺邏輯與輸出/視覺化。
   - 為閾值、核心大小、影格限制與輸出路徑使用具名參數。
   - 釋放 `VideoCapture` 與 `VideoWriter` 資源；啟用 GUI 模式時關閉 GUI 視窗。
   - 無頭環境避免使用 `imshow`，改為寫入輸出檔案或回傳陣列。

4. **驗證行為**
   - 優先使用合成 fixture，例如包含已知矩形或圓形的黑色影像。
   - 在適當情況下，斷言輸出 shape、dtype、結果非空，以及座標近似值。
   - 對影片驗證影格數、尺寸、FPS 處理方式，以及 writer 是否成功開啟。
   - 執行最相關的窄範圍測試，或使用小型 `uv run python ...` smoke check。

5. **清楚回報**
   - 說明使用的 OpenCV 套件變體與 Python 直譯器。
   - 附上驗證時使用的確切指令。
   - 說明媒體假設、已知失敗情況，以及是否需要 GUI 支援。

## 常見診斷

- `ModuleNotFoundError: cv2`：確認指令使用專案的 `.venv`；使用 `uv add` 安裝，並使用 `uv run` 執行。
- `imread` 回傳 `None`：檢查路徑、檔案權限、副檔名與目前工作目錄。
- 色彩異常：OpenCV 以 BGR 載入影像；傳給以 RGB 為主的函式庫前，使用 `cv2.cvtColor` 轉換。
- 輪廓或偵測結果為空：檢查閾值極性、灰階轉換、形態學參數與影像尺寸。
- 尺寸不一致：記住 NumPy 使用 `(height, width[, channels])`，許多 API 則描述為 `(width, height)`。
- 伺服器上的 GUI 錯誤：使用 headless 套件與檔案輸出，取代 HighGUI 視窗。

## 品質標準

- 對於無法讀取的影像、未開啟的相機或無法寫入的影片輸出，不允許靜默失敗。
- 不要不必要地複製大型影格；只有在需要變更資料或明確管理所有權時才使用 copy。
- 不要提出未經驗證的準確率、FPS 或偵測器效能宣稱。