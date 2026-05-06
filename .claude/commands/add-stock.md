新增股票到追蹤清單。用法：`/add-stock 代號` 例如 `/add-stock 2330.TW` 或 `/add-stock AAPL`。

根據 $ARGUMENTS 判斷市場：
- 結尾為 `.TW` 或 `.TWO` → 加入 `TW_STOCKS`
- 其他 → 加入 `US_STOCKS`

步驟：
1. 讀取 `.env` 目前的 `TW_STOCKS` 或 `US_STOCKS` 值
2. 確認代號尚未存在於清單中，若已存在則告知使用者不需要重複新增
3. 將新代號附加到對應變數末尾（逗號分隔），更新 `.env`
4. 顯示更新後的完整清單
