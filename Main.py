import os
import time
import requests

# ==========================================
# ⚙️ [CONFIGURATIONS] - তোমার সব এপিআই দেওয়া আছে
# ==========================================
BOT_TOKEN = "8858726595:AAEGt6vzteA-ALY_y4GfBWP-sz7UJ4v0K5Q"
GROUP_CHAT_ID = "-1004366096144"
API_TOKEN = "MWMFJUUNQRI"
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"
MINI_BOT_URL = "t.me/MXFastOTP1_Bot/panel"
BUTTON_TEXT = "🚀 Open Mini Bot"

# ইতিমধ্যে সেন্ড হওয়া ওটিপি ট্র্যাক রাখার মেমোরি
sent_otp_keys = set()

def get_formatted_number(num):
    """ ফোন নম্বরের মাঝখানে ❖MX❖ বসিয়ে হাইড করার ফাংশন """
    if not num:
        return "Unknown"
    clean = "".join(filter(str.isdigit, str(num)))
    if len(clean) < 6:
        return str(num)
    prefix = clean[:3]
    suffix = clean[-3:]
    return f"{prefix}❖MX❖{suffix}"

def send_telegram_message(number, country, service, otp_code, raw_message, time_str):
    """ টেলিগ্রাম গ্রুপে অটো মেসেজ পাঠানোর ফাংশন """
    masked_num = get_formatted_number(number)
    
    caption = f"""⚡ <b>MX FAST OTP PANEL - NEW OTP RECEIVED</b> ⚡
━━━━━━━━━━━━━━━━━━━━━━
📱 <b>Phone Number:</b> <code>{masked_num}</code>
🌍 <b>Country:</b> <b>{country}</b>
🏷️ <b>Service:</b> <b>{service}</b>
🔑 <b>OTP Code:</b> <code>{otp_code}</code>
⏰ <b>Time:</b> {time_str}

📩 <b>Message:</b>
<i>{raw_message}</i>
━━━━━━━━━━━━━━━━━━━━━━
<i>🛡️ Automated Secure OTP System</i>"""

    payload = {
        "chat_id": GROUP_CHAT_ID,
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
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def check_and_forward_otps():
    """ ভোল্টেক্স এপিআই থেকে ডাটা চেক করার ফাংশন """
    headers = {"mauthapi": API_TOKEN}
    try:
        response = requests.get(f"{BASE_URL}/success-otp", headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("meta", {}).get("code") == 200:
                otps = result.get("data", {}).get("otps", [])
                for item in otps:
                    num = item.get("number", "")
                    msg = item.get("message", "")
                    time_val = item.get("time", "Just Now")
                    
                    # ইউনিক কি তৈরি
                    unique_key = f"{num}_{msg}"
                    if unique_key in sent_otp_keys:
                        continue
                    
                    # মেসেজ থেকে ওটিপি কোড বের করা
                    import re
                    otp_match = re.search(r'\b\d{4,8}\b', msg)
                    otp_code = otp_match.group(0) if otp_match else "------"
                    
                    if otp_code != "------":
                        # মেসেজ সার্ভিস ডিটেক্ট করা
                        msg_lower = msg.lower()
                        service = "SYSTEM"
                        if "facebook" in msg_lower or "fb" in msg_lower:
                            service = "FACEBOOK"
                        elif "instagram" in msg_lower or "ig" in msg_lower:
                            service = "INSTAGRAM"
                        elif "whatsapp" in msg_lower:
                            service = "WHATSAPP"
                        elif "telegram" in msg_lower:
                            service = "TELEGRAM"

                        send_telegram_message(num, "Global Route 🌐", service, otp_code, msg, time_val)
                        sent_otp_keys.add(unique_key)
                        
                        # মেমোরি খালি রাখা
                        if len(sent_otp_keys) > 500:
                            sent_otp_keys.clear()
    except Exception as e:
        print(f"API Fetch Error: {e}")

if __name__ == "__main__":
    print("🚀 MX FAST OTP BOT IS RUNNING 24/7...")
    while True:
        check_and_forward_otps()
        time.sleep(3)  # প্রতি ৩ সেকেন্ড পর পর এপিআই চেক করবে
      
