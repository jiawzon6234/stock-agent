"""
stock_tracker.py — 主程式：排程 + 協調各模組
用法：
  python stock_tracker.py             # 排程模式（正式啟動）
  python stock_tracker.py test        # 測試模式（立即發送台股+美股）
  python stock_tracker.py once        # 立即發送台股+美股，發完即退出
  python stock_tracker.py once 台股  # 立即發送指定市場，發完即退出
  python stock_tracker.py once 美股
"""

import sys
import time
import schedule
import pytz
from datetime import datetime

from config import WATCH_LIST, TW_MARKET_CLOSE, US_MARKET_CLOSE
from fetcher import get_stock_data
from notifier import format_stock_message, send_line_chunked


def run_report(market: str):
    """執行單一市場報告並發送 LINE"""
    now = datetime.now(pytz.timezone("Asia/Taipei")).strftime("%Y/%m/%d %H:%M")
    symbols = WATCH_LIST.get(market, [])

    emoji = "📊" if market == "台股" else "🌏"
    header = f"\n{emoji} {market}盤後報告\n🕐 {now}\n"

    print(f"\n[{now}] 開始處理 {market}（共 {len(symbols)} 支）")

    stock_messages = []
    for sym in symbols:
        sym = sym.strip()
        print(f"  → 抓取 {sym}...")
        data = get_stock_data(sym)
        stock_messages.append(format_stock_message(data))
        time.sleep(1)   # 避免 yfinance 限速

    send_line_chunked(stock_messages, header)
    print(f"[完成] {market} 報告已發送")


def setup_schedule():
    """設定排程：台股週一~五 14:35，美股週二~六 05:10（台灣時間）"""

    # 台股
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        getattr(schedule.every(), day).at(TW_MARKET_CLOSE).do(run_report, market="台股")

    # 美股（美東收盤約台灣隔日 05:00）
    for day in ["tuesday", "wednesday", "thursday", "friday", "saturday"]:
        getattr(schedule.every(), day).at(US_MARKET_CLOSE).do(run_report, market="美股")

    print("✅ 排程已啟動")
    print(f"   台股：週一～週五 {TW_MARKET_CLOSE}")
    print(f"   美股：週二～週六 {US_MARKET_CLOSE}")
    print("   等待中... (Ctrl+C 離開)\n")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""

    if mode == "test":
        print("🧪 測試模式：立即發送一次")
        run_report("台股")
        run_report("美股")
    elif mode == "once":
        market = sys.argv[2] if len(sys.argv) > 2 else None
        if market:
            print(f"⚡ once 模式：發送 {market}")
            run_report(market)
        else:
            print("⚡ once 模式：發送台股 + 美股")
            run_report("台股")
            run_report("美股")
    else:
        setup_schedule()
