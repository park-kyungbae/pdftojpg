from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

# poppler 경로 설정 (윈도우 사용자만 필요)
POPPLER_PATH = r'C:\path\to\poppler-xx\Library\bin'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    if 'pdfFile' not in request.files:
        return jsonify({'error': '파일이 없습니다.'}), 400

    file = request.files['pdfFile']

    if file.filename == '':
        return jsonify({'error': '파일명이 없습니다.'}), 400

    filename = secure_filename(file.filename)
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(pdf_path)

    # PDF → JPG 변환
    images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)

    jpg_filename = filename.rsplit('.', 1)[0] + '.jpg'
    jpg_path = os.path.join(app.config['OUTPUT_FOLDER'], jpg_filename)

    # 첫 페이지만 변환 (필요시 for문으로 전체 변환 가능)
    images[0].save(jpg_path, 'JPEG')

    download_url = url_for('download_file', filename=jpg_filename)

    return jsonify({'download_url': download_url})


@app.route('/output/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)