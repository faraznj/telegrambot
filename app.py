from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

TOKEN = "توکن جدید شما"

@app.route('/')
def home():
    return "ربات تلگرام فعال است!"

@app.route('/upload', methods=['POST'])
def handle_update():
    data = request.get_json()
    
    # بررسی اینکه آیا پیام معتبر است
    if not data or "message" not in data:
        return jsonify({"status": "no valid message"}), 400

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "بدون متن")

    # ارسال پیام به کاربر
    send_message(chat_id, f"پیام شما دریافت شد: {text}")
    return jsonify({"status": "ok"}), 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
