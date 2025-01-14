from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TOKEN = "7869566708:AAHi0MbRRoMgwIsI-ekKvQOAAlc1qkGvomk"  

@app.route('/')
def home():
    return "ربات تلگرام فعال است!"

@app.route('/upload', methods=['POST'])
def handle_update():
    try:
        # چاپ هدرها و داده‌ها برای بررسی
        print("Headers:", request.headers)  # چاپ هدرهای درخواست
        data = request.get_json()
        print("Received data:", data)  # چاپ داده‌ها برای بررسی

        # بررسی اینکه آیا پیام معتبر است
        if not data or "message" not in data:
            print("Invalid data received:", data)  # نمایش داده‌های نادرست
            return jsonify({"status": "no valid message"}), 400

        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "بدون متن")

        # ارسال پاسخ به کاربر
        send_message(chat_id, f"پیام شما دریافت شد: {text}")
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Error processing the request: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # پورت را از محیط دریافت می‌کند
    app.run(host='0.0.0.0', port=port)
