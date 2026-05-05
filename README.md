# 📈 股票自動追蹤系統

台股 & 美股每日盤後自動分析，透過 LINE Notify 發送報告。

## 快速開始

```bash
# 1. 安裝套件
pip install -r requirements.txt

# 2. 建立設定檔
cp .env.example .env
# 編輯 .env，填入 LINE Token 和想追蹤的股票

# 3. 測試
python stock_tracker.py test

# 4. 正式啟動
python stock_tracker.py
```

## 專案結構

```
stock_tracker/
├── CLAUDE.md          # Claude Code 專案記憶（自動載入）
├── .env               # 你的私人設定（不進 git）
├── .env.example       # 設定範本
├── stock_tracker.py   # 主程式（排程）
├── config.py          # 設定讀取
├── fetcher.py         # 數據抓取
├── indicators.py      # 技術指標
├── notifier.py        # LINE 發送
└── .claude/
    ├── settings.json  # Claude Code 權限設定
    └── commands/
        ├── test-report.md   # /test-report 指令
        └── add-stock.md     # /add-stock 指令
```

## Claude Code 指令

在 Claude Code 中可以使用這些自訂指令：

| 指令 | 功能 |
|------|------|
| `/test-report` | 立即發送測試報告 |
| `/add-stock 2330.TW` | 新增股票到追蹤清單 |

## 排程時間

| 市場 | 時間（台灣） | 說明 |
|------|------------|------|
| 台股 | 週一～五 14:35 | 台股收盤後 5 分鐘 |
| 美股 | 週二～六 05:10 | 美東收盤後（隔日凌晨）|

## LINE Token 取得方式

1. 前往 https://notify-bot.line.me/
2. 登入 LINE 帳號
3. 點選「Generate token」
4. 選擇接收通知的聊天室
5. 複製 Token 填入 `.env`
