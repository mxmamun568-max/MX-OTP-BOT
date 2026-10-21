import http.server
import threading
import requests
import json
import time

# [ CONFIGURATIONS ] - আপনার তথ্য এখানে বসিয়ে নিন
BOT_TOKEN = "7872695:AAEw9v21tKA-y_y4DYbMP-sJ7uUJa4V04Q"
CHAT_ID = "-1002636261441"
OTP_TOKEN = "MAMUNMAPIN"
MINI_BOT_URL = "https://2009-Cloud/WebApp/news/public/api? # noqa: E501 /MXFASTOTP_BOT/panel"
BUTTON_TEXT = "Open Mini Bot"

# টেলিক্রামের জন্য নতুন টুলের ফেসকাট ইত্যাদি
def get_formatted_number(num):
    if not num:
        return {"country": "Unknown", "string": str(num)}
    if len(num) == 6:
        return {"country": "Bangladesh", "string": str(num)}
    elif len(num) == 5:
        return {"country": "India", "string": str(num)}
    else:
        return {"country": "Unknown", "string": str(num)}

def send_telegram_message(number, country_service, otp_code, ram_message, time_str):
    # অফিসিয়াল ফরম্যাট রেডি করা হচ্ছে ***
    caption = f"""<b>⚡️ FAST OTP PANEL — NEW OTP RECEIVED</b><br><br>"
    f"<b>📞 Phone Number:</b> <code>{number}</code><br>"
    f"<b>🌍 Country:</b> {country_service}<br>"
    f"<b>📱 Service:</b> {country_service}<br>"
    f"<b>🔑 OTP Code:</b> <code>{otp_code}</code><br>"
    f"<b>🕒 Time:</b> {time_str}<br><br>"
    f"<b>🛡️ Automated Secure OTP System</b>"""

    payload = {
        "chat_id": CHAT_ID,
        "text": caption,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": BUTTON_TEXT,
                        "url": f"https://{MINI_BOT_URL}" if not MINI_BOT_URL.startswith("http") else MINI_BOT_URL
                    }
                ]
            ]
        }
    }

    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def check_and_forward_otps():
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            headers = {"Cache-Control": "no-cache"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.get('result', [])
                for msg in data:
                    # প্রয়োজনীয় প্রসেসিং এখানে করা যেতে পারে
                    pass
        except Exception as e:
            print(f"Error fetching OTP: {e}")
        time.sleep(5)

# Render-এর জন্য পোর্টিং রাখার ডামি সার্ভার
PORT = 10000

class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    server = http.server.HTTPServer(('0.0.0.0', PORT), SimpleHandler)
    server.serve_forever()

if __name__ == '__main__':
    # ব্যাকগ্রাউন্ডে বট ও সার্ভার রান করা হচ্ছে
    threading.Thread(target=check_and_forward_otps, daemon=True).start()
    run_server()
    
