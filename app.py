from flask import Flask, request, jsonify
import fitz  # PyMuPDF
from PIL import Image
import pytesseract

app = Flask(__name__)

@app.route('/')
def home():
    return "ربات تلگرام فعال است!"

@app.route('/upload', methods=['POST'])
def upload_pdf():
    pdf_file = request.files['file']
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    full_text = ''
    
    # پردازش هر صفحه از PDF
    for page_num, page in enumerate(doc):
        print(f"Processing page {page_num + 1}")  # برای لاگ گرفتن
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))  # تبدیل صفحه به تصویر با کیفیت بالاتر
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # تبدیل پیکسل‌ها به تصویر

        # انجام OCR روی تصویر
        text = pytesseract.image_to_string(img, lang='fas+ara')  # زبان فارسی و عربی
        full_text += text + '\n'  # افزودن متن استخراج‌شده به متن کلی

    return jsonify({"text": full_text})  # ارسال متن استخراج‌شده به عنوان پاسخ

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
