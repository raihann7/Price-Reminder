import urllib.request
import json
import time
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8080832559:AAHnDO1ORZtTMLl2odzluqCX_-9hnmN-hQc")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "-1003857108371")

def get_price(symbol: str) -> float:
    # Transform BTCUSDT -> BTC-USD for Coinbase API
    pair = f"{symbol[:3]}-USD"
    url = f"https://api.coinbase.com/v2/prices/{pair}/spot"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        return float(data["data"]["amount"])

def send_telegram(text: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or TELEGRAM_BOT_TOKEN
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10)

def main():
    try:
        btc = get_price("BTCUSDT")
        sol = get_price("SOLUSDT")
        now = time.strftime("%H:%M")
        msg = (
            f"<b>Crypto Price Update</b>\n"
            f"BTC = <b>${btc:,.2f}</b>\n"
            f"SOL = <b>${sol:,.2f}</b>\n"
        )
        send_telegram(msg)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
