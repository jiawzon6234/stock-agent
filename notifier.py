"""
notifier.py — LINE Messaging API 訊息格式化與發送
（已從 LINE Notify 遷移至 Messaging API）
"""

import time
import requests
from config import LINE_CHANNEL_TOKEN, LINE_USER_ID, ALERT_DROP_PCT, ALERT_RISE_PCT
from fetcher import format_market_cap
from indicators import rsi_label, macd_label

MAX_LINE_MSG = 2000   # Messaging API 單則上限 5000 字，保守設 2000


def send_line(message: str):
    """用 LINE Messaging API 發送訊息給指定 User ID"""
    if not LINE_CHANNEL_TOKEN or not LINE_USER_ID:
        print("[LINE] ⚠️ LINE_CHANNEL_TOKEN 或 LINE_USER_ID 未設定，略過發送")
        return
    try:
        resp = requests.post(
            "https://api.line.me/v2/bot/message/push",
            headers={
                "Authorization": f"Bearer {LINE_CHANNEL_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "to": LINE_USER_ID,
                "messages": [{"type": "text", "text": message}],
            },
            timeout=10,
        )
        status = "✅ 成功" if resp.status_code == 200 else f"❌ 失敗({resp.status_code}): {resp.text}"
        print(f"[LINE] {status}")
    except Exception as e:
        print(f"[LINE] 發送錯誤：{e}")


def send_line_chunked(messages: list[str], header: str):
    """
    將多則股票訊息合併後發送。
    超過 MAX_LINE_MSG 字元時自動拆分成多則。
    """
    chunks = []
    current = header
    for msg in messages:
        if len(current) + len(msg) > MAX_LINE_MSG:
            chunks.append(current)
            current = msg
        else:
            current += msg
    chunks.append(current)

    import time
    for i, chunk in enumerate(chunks, 1):
        prefix = f"({i}/{len(chunks)}) " if len(chunks) > 1 else ""
        send_line(f"{prefix}{chunk}")
        if i < len(chunks):
            time.sleep(2)


def format_stock_message(data: dict) -> str:
    """將股票 dict 格式化成 LINE 訊息區塊"""
    if data.get("error"):
        return f"\n❌ {data['symbol']}：{data['error']}"

    sym = data["symbol"]
    price = data["price"]
    chg   = data["change"]
    pct   = data["change_pct"]
    sign  = "+" if chg >= 0 else ""

    # 漲跌 emoji
    if pct >= ALERT_RISE_PCT:
        arrow = "🚀"
    elif pct > 0:
        arrow = "📈"
    elif pct <= ALERT_DROP_PCT:
        arrow = "🔴⚠️"
    elif pct < 0:
        arrow = "📉"
    else:
        arrow = "➡️"

    lines = [
        f"\n{'='*26}",
        f"📌 {sym}",
        f"💰 {price}  {arrow} {sign}{chg} ({sign}{pct:.2f}%)",
    ]

    # 均線
    if data["ma"]:
        ma_str = "  ".join(f"{k}:{v}" for k, v in data["ma"].items())
        lines.append(f"📊 {ma_str}")

    # RSI
    rsi = data["rsi"]
    if rsi is not None:
        lines.append(f"📉 RSI：{rsi}{rsi_label(rsi)}")

    # MACD
    if data["macd"] is not None:
        lines.append(
            f"📈 MACD：{data['macd']} / 訊號：{data['macd_signal']} "
            f"{macd_label(data['macd_hist'])}"
        )

    # 財報
    eps = data["eps"]
    pe  = data["pe"]
    if eps or pe:
        eps_str = f"{eps:.2f}" if eps else "N/A"
        pe_str  = f"{pe:.1f}"  if pe  else "N/A"
        lines.append(f"📋 EPS：{eps_str}  本益比：{pe_str}")

    if data["market_cap"]:
        lines.append(f"🏢 市值：{format_market_cap(data['market_cap'])}")

    # 新聞
    if data["news"]:
        lines.append("📰 最新：")
        for title in data["news"]:
            short = (title[:33] + "…") if len(title) > 33 else title
            lines.append(f"  • {short}")

    return "\n".join(lines)
