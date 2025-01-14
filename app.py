import os
from flask import Flask, request
import fitz
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

    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img, lang='fas+ara')
        full_text += text + '\n'  # از \\n به \n تغییر یافت

    return {"text": full_text}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # دریافت پورت از متغیر محیطی PORT
    app.run(host='0.0.0.0', port=port)
