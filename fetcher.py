"""
fetcher.py — 從 Yahoo Finance 抓取股票數據
"""

import yfinance as yf
import pandas as pd
from config import MA_PERIODS
from indicators import calculate_ma, calculate_rsi, calculate_macd


def get_stock_data(symbol: str) -> dict:
    """
    抓取單一股票完整數據，回傳標準化 dict。
    失敗時 error 欄位會有錯誤訊息。
    """
    try:
        ticker = yf.Ticker(symbol)

        # 取 3 個月歷史（技術指標需要足夠資料點）
        hist = ticker.history(period="3mo")
        if hist.empty:
            return {"symbol": symbol, "error": "無法取得歷史數據"}

        closes = hist["Close"]
        latest  = closes.iloc[-1]
        prev    = closes.iloc[-2]
        change  = latest - prev
        chg_pct = (change / prev) * 100

        # 技術指標
        macd, macd_sig, macd_hist = calculate_macd(closes)

        # 基本資訊（財報數據）
        info = ticker.info

        # 最新新聞（前 3 則）
        news_titles = []
        try:
            for n in (ticker.news or [])[:3]:
                title = n.get("title", "").strip()
                if title:
                    news_titles.append(title)
        except Exception:
            pass

        return {
            "symbol":      symbol,
            "price":       round(latest, 2),
            "change":      round(change, 2),
            "change_pct":  round(chg_pct, 2),
            "volume":      int(hist["Volume"].iloc[-1]),
            "ma":          calculate_ma(closes, MA_PERIODS),
            "rsi":         calculate_rsi(closes),
            "macd":        macd,
            "macd_signal": macd_sig,
            "macd_hist":   macd_hist,
            "eps":         info.get("trailingEps"),
            "pe":          info.get("trailingPE"),
            "market_cap":  info.get("marketCap"),
            "news":        news_titles,
            "error":       None,
        }

    except Exception as e:
        return {"symbol": symbol, "error": str(e)}


def format_market_cap(cap) -> str:
    """格式化市值：自動切換億 / M 單位"""
    if cap is None:
        return "N/A"
    if cap >= 1e8:
        return f"{cap / 1e8:.1f}億"
    if cap >= 1e6:
        return f"{cap / 1e6:.1f}M"
    return str(cap)
