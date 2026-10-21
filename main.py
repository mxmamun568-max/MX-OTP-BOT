import http.server
import json
import socketserver
import threading
import time
import requests

# ================= CONFIGURATIONS =================
BOT_TOKEN = "8850726955:AAEGe0VztKA-aLY_y4dYBHP-sz7UJa4V0kQ"
CHAT_ID = "-1004360696144"
API_TOKEN = "MXMPJURD1"
BASE_URL = "https://api.2009.cloud/WK547FLFKOU/tnews/8public/api"
MINI_BOT_URL = "t.me/MXFastOTP1_Bot/panel"
BUTTON_TEXT = "🚀 Open Mini Bot"

# ডুপ্লিকেট মেসেজ রোধ করার জন্য সেট
sent_otp_keys = set()

def get_formatted_number(num):
    if not num:
        return "Unknown"
    clean = "".join(filter(str.isdigit, str(num)))
    if len(clean) < 6:
        return str(num)
    prefix = clean[:3]
    suffix = clean[-3:]
    return f"{prefix}***{suffix}"

def send_telegram_message(number, country, service, otp_code, ram_message, time_str):
    masked_num = get_formatted_number(number)
    caption = f"""<b>⚡️ FAST OTP PANEL - NEW OTP RECEIVED</b>

📞 Phone Number: <code>{masked_num}</code>
🌐 Country: <b>{country}</b>
⚙️ Service: <b>{service}</b>
🔑 OTP Code: <code>{otp_code}</code>
🕒 Time: <b>{time_str}</b>

💬 Message:
<code>{ram_message}</code>

🤖 Automated Secure OTP System"""

    payload = {
        "chat_id": CHAT_ID,
        "text": caption,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": BUTTON_TEXT, "url": f"https://{MINI_BOT_URL}"}]
            ]
        }
    }

    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def check_and_forward_otps():
    while True:
        headers = {"AuthAPI": API_TOKEN}
        try:
            # API থেকে OTP ডাটা চেক করা
            response = requests.get(f"{BASE_URL}/otp", headers=headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                ots = result.get("data", [])
                for item in ots:
                    num = item.get("number", "")
                    msg = item.get("message", "")
                    country = item.get("country", "Global")
                    service = item.get("service", "System")
                    otp_code = item.get("otp", "")
                    time_val = item.get("time", "Just Now")
                    
                    unique_key = f"{num}_{msg}_{time_val}"
                    
                    if unique_key not in sent_otp_keys:
                        send_telegram_message(num, country, service, otp_code, msg, time_val)
                        sent_otp_keys.add(unique_key)
                        
                if len(sent_otp_keys) > 500:
                    sent_otp_keys.clear()
                    
        except Exception as e:
            print(f"Error checking OTPs: {e}")
            
        time.sleep(3)

# Render সার্ভার সচল রাখার জন্য ডামি ওয়েব সার্ভার
PORT = 10000

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running live!")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

def run_server():
    server = socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler)
    print("Serving at port", PORT)
    server.serve_forever()

if __name__ == '__main__':
    # ব্যাকগ্রাউন্ডে ওটিপি চেক করার থ্রেড চালু
    threading.Thread(target=check_and_forward_otps, daemon=True).start()
    # ওয়েব সার্ভার চালু
    run_server()
                        
