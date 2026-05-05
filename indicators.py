"""
indicators.py — 技術指標計算
"""

import pandas as pd
from config import RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL


def calculate_ma(prices: pd.Series, periods: list[int]) -> dict:
    """計算多條均線，回傳 {MA5: 值, MA20: 值, ...}"""
    result = {}
    for p in periods:
        if len(prices) >= p:
            result[f"MA{p}"] = round(prices.rolling(p).mean().iloc[-1], 2)
    return result


def calculate_rsi(prices: pd.Series, period: int = RSI_PERIOD) -> float | None:
    """計算 RSI"""
    if len(prices) < period + 1:
        return None
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi.iloc[-1], 2)


def calculate_macd(prices: pd.Series) -> tuple[float, float, float] | tuple[None, None, None]:
    """計算 MACD，回傳 (macd, signal, histogram)"""
    if len(prices) < MACD_SLOW:
        return None, None, None
    ema_fast   = prices.ewm(span=MACD_FAST, adjust=False).mean()
    ema_slow   = prices.ewm(span=MACD_SLOW, adjust=False).mean()
    macd       = ema_fast - ema_slow
    signal     = macd.ewm(span=MACD_SIGNAL, adjust=False).mean()
    histogram  = macd - signal
    return (
        round(macd.iloc[-1], 4),
        round(signal.iloc[-1], 4),
        round(histogram.iloc[-1], 4),
    )


def rsi_label(rsi: float | None) -> str:
    """RSI 超買超賣標籤"""
    if rsi is None:
        return ""
    if rsi > 70:
        return " ⚠️超買"
    if rsi < 30:
        return " ⚠️超賣"
    return ""


def macd_label(histogram: float | None) -> str:
    """MACD 金叉死叉標籤"""
    if histogram is None:
        return ""
    return "↑金叉" if histogram > 0 else "↓死叉"
