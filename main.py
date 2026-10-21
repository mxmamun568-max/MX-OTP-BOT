
import os
import time
import threading
import http.server
import socketserver
import requests

# ============== CONFIGURATION ==============

BOT_TOKEN = os.getenv("8858726595:AAEGt6vzteA-ALY_y4GfBWP-sz7UJ4v0K5Q", "")
CHAT_ID = os.getenv("-1004366096144", "")
API_TOKEN = os.getenv("MWMFJUUNQRI", "")
BASE_URL = os.getenv("https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api", "").rstrip("/")

PORT = int(os.getenv("PORT", "10000"))

session = requests.Session()


def check_telegram():
    """Check bot token and Telegram group access."""

    if not BOT_TOKEN or not CHAT_ID:
        print("ERROR: BOT_TOKEN or CHAT_ID is missing.")
        return False

    try:
        r = session.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getMe",
            timeout=15
        )
        data = r.json()

        if not data.get("ok"):
            print("Telegram getMe error:", data)
            return False

        print("Telegram bot connection: OK")

        test = session.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": "✅ MX OTP BOT — Connection Test Successful"
            },
            timeout=15
        )

        result = test.json()

        if not result.get("ok"):
            print("Telegram sendMessage error:", result)
            return False

        print("Telegram group message: SUCCESS")
        return True

    except Exception as e:
        print("Telegram connection error:", str(e))
        return False


def check_api():
    """Check API availability without forwarding OTP contents."""

    if not API_TOKEN or not BASE_URL:
        print("ERROR: API_TOKEN or BASE_URL is missing.")
        return

    headers = {"mauthapi": API_TOKEN}

    try:
        r = session.get(
            f"{BASE_URL}/success-otp",
            headers=headers,
            timeout=15
        )

        print("API HTTP status:", r.status_code)

        if r.status_code != 200:
            print("API request failed. Check API access and endpoint.")
            return

        try:
            result = r.json()
        except ValueError:
            print("API error: response is not valid JSON.")
            return

        if not isinstance(result, dict):
            print("API error: unexpected response format.")
            return

        records = result.get("data", [])

        if not isinstance(records, list):
            print("API error: 'data' is not a list.")
            return

        print("API connection: OK")
        print("Records returned:", len(records))
        print("OTP contents are not displayed or forwarded.")

    except requests.RequestException as e:
        print("API connection error:", str(e))


def diagnostic_loop():
    while True:
        check_api()
        time.sleep(30)


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"MX OTP BOT diagnostic service is running."

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def run_server():
    with socketserver.ThreadingTCPServer(
        ("0.0.0.0", PORT), Handler
    ) as server:
        server.allow_reuse_address = True
        print("Web server listening on port:", PORT)
        server.serve_forever()


if __name__ == "__main__":
    check_telegram()

    threading.Thread(
        target=diagnostic_loop,
        daemon=True
    ).start()

    run_server()
    
