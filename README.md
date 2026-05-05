# 股票自動追蹤系統

台股 & 美股每日盤後自動分析，透過 LINE Messaging API 發送報告。

## 專案結構

```
stock_agent/
├── stock_tracker.py   # 主程式（排程 + 模式切換）
├── config.py          # 設定讀取（.env）
├── fetcher.py         # yfinance 數據抓取
├── indicators.py      # 技術指標計算
├── notifier.py        # LINE 訊息格式化與發送
├── run_tw.bat         # 執行台股一次性報告
├── run_us.bat         # 執行美股一次性報告
├── .env               # 機密設定（不進 git）
├── .env.example       # 設定範本
└── requirements.txt
```

## 快速開始

**1. 安裝套件**
```bash
pip install -r requirements.txt
```

**2. 建立 `.env`**
```bash
copy .env.example .env
```
填入 LINE Messaging API 的 Channel Access Token 與你的 User ID（格式 `Uxxxxxxxxxx`）。

**3. 測試**
```bash
python stock_tracker.py once
```

## 執行模式

| 指令 | 說明 |
|------|------|
| `python stock_tracker.py` | 排程模式，長時間掛載 |
| `python stock_tracker.py test` | 立即發送台股 + 美股（測試用） |
| `python stock_tracker.py once` | 立即發送台股 + 美股，發完即退出 |
| `python stock_tracker.py once 台股` | 只發台股，發完即退出 |
| `python stock_tracker.py once 美股` | 只發美股，發完即退出 |

## Windows 工作排程器

`run_tw.bat` 與 `run_us.bat` 已登錄至工作排程器（`StockTracker\` 資料夾）：

| 工作 | 觸發時間（台灣） | 說明 |
|------|----------------|------|
| 台股盤後報告 | 週一～五 14:35 | 台股收盤後 5 分鐘 |
| 美股盤後報告 | 週二～六 05:10 | 美東收盤後（凌晨）|

手動重建排程（若更換電腦）：
```bat
schtasks /create /tn "StockTracker\台股盤後報告" /tr "%CD%\run_tw.bat" /sc WEEKLY /d MON,TUE,WED,THU,FRI /st 14:35 /f
schtasks /create /tn "StockTracker\美股盤後報告" /tr "%CD%\run_us.bat" /sc WEEKLY /d TUE,WED,THU,FRI,SAT /st 05:10 /f
```

## .env 設定說明

```ini
# LINE Messaging API
LINE_CHANNEL_TOKEN=你的_Channel_Access_Token
LINE_USER_ID=你的_User_ID

# 追蹤股票（逗號分隔）
TW_STOCKS=2330.TW,2317.TW,2454.TW
US_STOCKS=AAPL,NVDA,TSLA

# 警報門檻（可選）
ALERT_DROP_PCT=-3.0   # 跌超過此 % 加警示
ALERT_RISE_PCT=5.0    # 漲超過此 % 加提示

# 發送時間，台灣時間（可選）
TW_MARKET_CLOSE=14:35
US_MARKET_CLOSE=05:10
```

## 股票代號格式

- 台股上市：`2330.TW`
- 台股上櫃：`6488.TWO`
- 美股：`AAPL`、`NVDA`
