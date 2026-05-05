# 股票自動追蹤系統

## 專案概述
每日自動抓取台股 & 美股數據，計算技術指標，透過 LINE Notify 發送盤後報告。

## 技術棧
- **語言**：Python 3.10+
- **主要套件**：yfinance、pandas、numpy、schedule、requests
- **通知**：LINE Notify API
- **排程**：schedule 套件（本機執行）

## 目錄結構
```
stock_tracker/
├── CLAUDE.md                  # 本檔案
├── README.md
├── requirements.txt
├── .env                       # 機密設定（不進 git）
├── .env.example               # 範例設定檔
├── .gitignore
├── stock_tracker.py           # 主程式（排程 + 發送）
├── config.py                  # 設定讀取
├── indicators.py              # 技術指標計算
├── fetcher.py                 # 股票數據抓取
├── notifier.py                # LINE 通知發送
└── .claude/
    ├── settings.json
    └── commands/
        ├── test-report.md     # 立即發送測試報告
        └── add-stock.md       # 新增追蹤股票
```

## 執行方式
```bash
# 安裝套件
pip install -r requirements.txt

# 測試（立即發一次）
python stock_tracker.py test

# 正式啟動排程
python stock_tracker.py
```

## 重要規則
- 機密資訊（LINE Token）放 `.env`，絕對不能 hardcode 進程式碼
- 台股代號格式：`2330.TW`（上市）/ `6488.TWO`（上櫃）
- 美股代號格式：`AAPL`、`NVDA`
- LINE 單則訊息上限 1000 字，超過需自動拆分發送
- yfinance 請求之間需 sleep 1 秒避免被限速

## 常見指令
```bash
python stock_tracker.py test    # 立即測試發送
python stock_tracker.py         # 啟動排程模式
```
