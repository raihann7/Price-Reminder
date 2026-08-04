# PRD: Crypto Price Monitor Telegram Bot

## 1. Overview
Bot otomatis pemantau harga crypto (BTC & SOL) per 5 menit ke Channel/Group Telegram tanpa API Key berbayar/terdaftar, menggunakan public endpoint tanpa otentikasi.

## 2. Technical Stack
- **Language**: Python 3.x (Standard library: `urllib.request`, `json`, `time`, `os`).
- **Data Source**: Binance Public Ticker API (`api.binance.com`).
- **Notifier**: Telegram Bot API (`api.telegram.org`).
- **Runtime**: Linux Systemd / Docker / Cron.

## 3. Minimal Production Code (`bot.py`)
```python
import urllib.request
import json
import time
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "@your_channel")

def get_price(symbol: str) -> float:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return float(json.loads(resp.read().decode())["price"])

def send_telegram(text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10)

def main():
    while True:
        try:
            btc = get_price("BTCUSDT")
            sol = get_price("SOLUSDT")
            now = time.strftime("%H:%M")
            msg = f"<b>Crypto Price Update (Live!)</b>\nBTC = <b>${btc:,.2f}</b>\nSOL = <b>${sol:,.2f}</b>\n👁️ 1 {now}"
            send_telegram(msg)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(300)

if __name__ == "__main__":
    main()
```

## 4. Execution Roadmap (AI Agent Prompting)
1. **Fetch**: Minta AI generate fungsi `get_price` pakai `urllib`.
2. **Notify**: Minta AI buat fungsi `send_telegram`.
3. **Deploy**: Minta AI generate `Dockerfile` / `systemd.service`.
