import http.server
import socketserver
import threading

import requests

# ==========================================
# ( CONFIGURATIONS ) - আপনার সব সেটিং এখানে আছে
# ==========================================

BOT_TOKEN = "8850726955:AAEGe0VztKA-aLY_y4dYBHP-sz7UJa4V0kQ"
CHAT_ID = "-1004360696144"
API_TOKEN = "MXMPJURD1"
BASE_URL = (
    "https://api.2009.cloud/WK547FLFKOU/tnews/8public/api"  # noqa: E501
)
PANEL_URL = "https://t.me/MXFASTOTP_Bot/panel"
BUTTON_TEXT = "🚀 Open Mini Bot"


# টেলিগ্রাম থেকে নতুন টোকেন ট্র্যাকার গ্লোবালি
sent_otp_keys = set()


def get_formatted_number(num):
    # * থেকে কোনো নাম্বার বা অক্ষর থাকলে তা বাদ করা হবে ***
    if not num:
        return "unknown"
    clean = "".join(filter(str.isdigit, str(num)))
    if len(clean) < 6:
        return str(num)
    prefix = clean[:3]
    suffix = clean[-3:]
    return f"{prefix}***{suffix}"


def send_telegram_message(
    number, country, service, otp_code, ram_message, time_str
):
    # * প্রমিজ মেসেজ পাঠাতে সাহায্য করবেন ***
    masked_num = get_formatted_number(number)

    caption = f"""<b><# FAST OTP PANEL - NEW OTP RECEIVED#></b>

📞Phone Number: <code>{masked_num}</code>
🌐Country: <b>{country}</b>
⚙️Service: <b>{service}</b>
🔑OTP Code: <code>{otp_code}</code>
🕒Time: <b>{time_str}</b>

💬Message:
<code>{ram_message}</code>

🤖Automated Secure OTP System"""

    payload = {
        "chat_id": CHAT_ID,
        "text": caption,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": BUTTON_TEXT,
                        "url": f"https://{MINI_BOT_URL}"
                        if not MINI_BOT_URL.startswith("http")
                        else MINI_BOT_URL,
                    }
                ]
            ]
        },
    }

    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json=payload,
            timeout=10,
        )
    except Exception as e:
        print(f"Error sending to Telegram: {e}")


def check_and_forward_otps():
    # * রেন্ডারকে সচল রাখতে এবং চেক করার কাজ করবেন ***
    headers = {"AuthAPI": API_TOKEN}
    try:
        response = requests.get(
            f"{BASE_URL}/otp", headers=headers, timeout=10
        )
        if response.status_code == 200:
            ots = response.get("data", [])
            for ot in ots:
                num = ot.get("number", "")
                msg = ot.get("message", "")
                time_get = ot.get("time", "Just Now")
                # বাকি কোড...
    except Exception as e:
        print(f"Error checking OTPs: {e}")


# Render-এর জন্য পোর্টের ব্যবস্থা (HTTP সার্ভার)
def run_server():
    PORT = 10000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()
    
