from flask import Flask, request, jsonify
import fitz
from PIL import Image
import pytesseract

app = Flask(__name__)

@app.route('/')
def home():
    return "ربات تلگرام فعال است!"

@app.route('/upload', methods=['POST'])
def handle_update():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"status": "no message"}), 400  # پاسخ 400 در صورت نبود پیام

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "بدون متن")
    
    # ارسال پاسخ به کاربر
    send_message(chat_id, f"متن دریافت شد: {text}")
    return jsonify({"status": "ok"}), 200

def send_message(chat_id, text):
    import requests
    TOKEN = "توکن جدید شما"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
