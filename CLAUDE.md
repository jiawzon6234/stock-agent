# 股票自動追蹤系統 — Claude Code 專案記憶

## 專案概述
每日自動抓取台股 & 美股盤後數據，計算技術指標，透過 LINE Messaging API 發送報告。
Windows 工作排程器（Task Scheduler）負責定時觸發，不需要長時間掛載程序。

## 技術棧
- **語言**：Python 3.10+
- **主要套件**：yfinance、pandas、numpy、schedule、requests、pytz、python-dotenv
- **通知**：LINE Messaging API（push message，非 LINE Notify）
- **排程**：Windows 工作排程器（`StockTracker\` 資料夾）

## 目錄結構
```
stock_agent/
├── CLAUDE.md              # 本檔案
├── README.md
├── requirements.txt
├── .env                   # 機密設定（不進 git）
├── .env.example           # 範本
├── .gitignore
├── stock_tracker.py       # 主程式：排程 + 模式切換
├── config.py              # 從 .env 讀取所有設定
├── fetcher.py             # yfinance 數據抓取 + 市值格式化
├── indicators.py          # MA / RSI / MACD 計算
├── notifier.py            # LINE 訊息格式化與發送（send_line / send_line_chunked）
├── run_tw.bat             # 台股一次性執行腳本（Task Scheduler 用）
├── run_us.bat             # 美股一次性執行腳本（Task Scheduler 用）
└── .claude/
    ├── settings.json
    └── commands/
        ├── test-report.md # /test-report：立即發送測試報告
        └── add-stock.md   # /add-stock <代號>：新增追蹤股票
```

## 執行模式
| 指令 | 說明 |
|------|------|
| `python stock_tracker.py` | 排程模式，長時間掛載（once 模式出現前的舊做法） |
| `python stock_tracker.py test` | 立即發送台股 + 美股（測試用，不退出） |
| `python stock_tracker.py once` | 立即發送台股 + 美股，發完即退出 |
| `python stock_tracker.py once 台股` | 只發台股，發完即退出 |
| `python stock_tracker.py once 美股` | 只發美股，發完即退出 |

## Windows 工作排程器
兩個排程已登錄於 `StockTracker\` 資料夾：
- **台股盤後報告**：週一～五 14:35，執行 `run_tw.bat`
- **美股盤後報告**：週二～六 05:10，執行 `run_us.bat`

bat 腳本內含 `chcp 65001` 與 `PYTHONIOENCODING=utf-8`，避免 Windows cp950 編碼問題。

## 重要規則
- 機密資訊（LINE Token、User ID）只放 `.env`，絕對不能 hardcode
- LINE 使用 Messaging API（`api.line.me/v2/bot/message/push`），不是已停止的 LINE Notify
- 台股代號格式：`2330.TW`（上市）/ `6488.TWO`（上櫃）
- 美股代號格式：`AAPL`、`NVDA`
- yfinance 請求之間 sleep 1 秒避免被限速
- LINE 訊息保守設 2000 字上限，超過自動拆分（`send_line_chunked`）

## 各模組職責
- **config.py**：唯一讀取 `.env` 的地方，其他模組從這裡 import 設定
- **fetcher.py**：`get_stock_data(symbol)` 回傳標準化 dict，失敗時有 `error` 欄位
- **indicators.py**：純計算，無副作用；`rsi_label` / `macd_label` 輸出標籤文字
- **notifier.py**：`format_stock_message(data)` 格式化單股訊息；`send_line_chunked` 負責拆分發送
- **stock_tracker.py**：協調以上模組，`run_report(market)` 是核心流程

## 常用指令
```bash
# 測試（立即發送並退出）
python stock_tracker.py once

# 只測試台股
python stock_tracker.py once 台股

# 重建 Windows 工作排程器（更換電腦時）
schtasks /create /tn "StockTracker\台股盤後報告" /tr "%CD%\run_tw.bat" /sc WEEKLY /d MON,TUE,WED,THU,FRI /st 14:35 /f
schtasks /create /tn "StockTracker\美股盤後報告" /tr "%CD%\run_us.bat" /sc WEEKLY /d TUE,WED,THU,FRI,SAT /st 05:10 /f
```

## Claude Code 指令
| 指令 | 功能 |
|------|------|
| `/test-report` | 立即執行 once 模式，驗證發送是否正常 |
| `/add-stock 2330.TW` | 新增股票到 .env 追蹤清單（自動判斷台股/美股） |
