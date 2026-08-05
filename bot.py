from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import json
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8080832559:AAHnDO1ORZtTMLl2odzluqCX_-9hnmN-hQc")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "-1003857108371")

def get_price(symbol: str) -> float:
    pair = f"{symbol[:3]}-USD"
    url = f"https://api.coinbase.com/v2/prices/{pair}/spot"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return float(json.loads(resp.read().decode())["data"]["amount"])

GOLD_BOT_TOKEN = os.environ.get("GOLD_BOT_TOKEN", "BOT_TOKEN_GOLD_ANDA")
GOLD_CHAT_ID = os.environ.get("GOLD_CHAT_ID", "CHAT_ID_GOLD_ANDA")

def get_gold_price() -> float:
    url = "https://api.coinbase.com/v2/prices/PAXG-USD/spot"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return float(json.loads(resp.read().decode())["data"]["amount"])

def send_telegram(text: str, token: str = None, chat_id: str = None) -> None:
    token = token or os.environ.get("TELEGRAM_BOT_TOKEN") or TELEGRAM_BOT_TOKEN
    chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID") or TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10)

def trigger_check():
    # 1. Crypto Bot (BTC & SOL)
    btc = get_price("BTCUSDT")
    sol = get_price("SOLUSDT")
    crypto_msg = f"BTC=<b>${btc:,.2f}</b> | SOL=<b>${sol:,.2f}</b>"
    send_telegram(crypto_msg)

    # 2. Gold Bot (XAUUSD / Gold)
    try:
        gold = get_gold_price()
        gold_msg = f"XAUUSD=<b>${gold:,.2f}</b>"
        gold_token = os.environ.get("GOLD_BOT_TOKEN") or GOLD_BOT_TOKEN
        gold_chat = os.environ.get("GOLD_CHAT_ID") or GOLD_CHAT_ID
        if gold_token != "BOT_TOKEN_GOLD_ANDA":
            send_telegram(gold_msg, token=gold_token, chat_id=gold_chat)
    except Exception as e:
        print(f"Error fetching gold price: {e}")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            trigger_check()
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK - Price Sent")
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(str(e).encode())

def main():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    print(f"Server running on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    main()
