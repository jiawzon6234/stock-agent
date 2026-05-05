"""
config.py — 從 .env 讀取所有設定
修改追蹤股票、指標參數、發送時間請改這裡
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── LINE Messaging API ────────────────────────────
LINE_CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN", "")   # Channel Access Token
LINE_USER_ID       = os.getenv("LINE_USER_ID", "")         # 你的 LINE User ID（Uxxxxxxxxxx）

# ── 追蹤股票 ──────────────────────────────────────
# 台股：加 .TW（上市）或 .TWO（上櫃）
# 美股：直接填代號
WATCH_LIST = {
    "台股": os.getenv("TW_STOCKS", "2330.TW,2317.TW,2454.TW").split(","),
    "美股": os.getenv("US_STOCKS", "AAPL,NVDA,TSLA").split(","),
}

# ── 技術指標參數 ──────────────────────────────────
MA_PERIODS   = [5, 20, 60]
RSI_PERIOD   = 14
MACD_FAST    = 12
MACD_SLOW    = 26
MACD_SIGNAL  = 9

# ── 警報門檻 ──────────────────────────────────────
ALERT_DROP_PCT = float(os.getenv("ALERT_DROP_PCT", "-3.0"))   # 跌超過 % 加警示
ALERT_RISE_PCT = float(os.getenv("ALERT_RISE_PCT", "5.0"))    # 漲超過 % 加提示

# ── 發送時間（台灣時間）──────────────────────────
TW_MARKET_CLOSE = os.getenv("TW_MARKET_CLOSE", "14:35")   # 台股盤後
US_MARKET_CLOSE = os.getenv("US_MARKET_CLOSE", "05:10")   # 美股盤後（台灣時間）
