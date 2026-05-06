立即執行一次報告並發送 LINE，用於驗證環境與通知是否正常。

執行以下指令：

```bash
PYTHONIOENCODING=utf-8 python stock_tracker.py once
```

執行完成後確認輸出中每支股票都有 `→ 抓取` 記錄，且最後出現 `[LINE] ✅ 成功`。若有錯誤，回報錯誤訊息並協助排查。
