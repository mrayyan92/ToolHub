from flask import Flask, render_template, request, send_file
from PIL import Image
from rembg import remove
import pythoncom
from docx2pdf import convert
import img2pdf
from PyPDF2 import PdfMerger
from pdf2docx import Converter
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ================= HOME =================

@app.route("/")
def index():
    return render_template("pages/index.html")


# ================= IMAGE COMPRESSOR =================


@app.route("/compressor")
def compressor():
    return render_template("compressor.html")


@app.route("/compress-image", methods=["POST"])
def compress_image():

    if "image" not in request.files:
        return "No image uploaded."

    file = request.files["image"]

    if file.filename == "":
        return "No file selected."

    filename = secure_filename(file.filename)

    quality = int(request.form.get("quality", 70))

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    file.save(input_path)

    img = Image.open(input_path)

    if img.mode == "RGBA":
        img = img.convert("RGB")

    img.save(output_path, optimize=True, quality=quality)

    return send_file(output_path, as_attachment=True)


# ================= BACKGROUND REMOVER =================

@app.route("/remover")
def remover():
    return render_template("remover.html")


@app.route("/remove-background", methods=["POST"])
def remove_background():

    if "image" not in request.files:
        return "No image uploaded."

    file = request.files["image"]

    if file.filename == "":
        return "No file selected."

    filename = secure_filename(file.filename)

    input_path = os.path.join(UPLOAD_FOLDER, filename)

    output_filename = "no_bg_" + filename
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    file.save(input_path)

    with open(input_path, "rb") as f:
        input_data = f.read()

    output_data = remove(input_data)

    with open(output_path, "wb") as f:
        f.write(output_data)

    return send_file(output_path, as_attachment=True)


# ================= PDF TO WORD =================

@app.route("/pdf-to-word")
def pdf_to_word():
    return render_template("tools/pdf_to_word.html")

@app.route("/word-to-pdf")
def word_to_pdf():
    return render_template("tools/word_to_pdf.html")


@app.route("/convert-pdf", methods=["POST"])
def convert_pdf():

    if "pdf" not in request.files:
        return "No PDF uploaded."

    file = request.files["pdf"]

    if file.filename == "":
        return "No file selected."

    filename = secure_filename(file.filename)

    pdf_path = os.path.join(UPLOAD_FOLDER, filename)

    docx_filename = os.path.splitext(filename)[0] + ".docx"
    docx_path = os.path.join(OUTPUT_FOLDER, docx_filename)

    file.save(pdf_path)

    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()

    return send_file(docx_path, as_attachment=True)

@app.route("/convert-word", methods=["POST"])
def convert_word():

    pythoncom.CoInitialize()

    try:
        if "word" not in request.files:
            return "No Word file uploaded."

        file = request.files["word"]

        if file.filename == "":
            return "No file selected."

        filename = secure_filename(file.filename)

        word_path = os.path.join(UPLOAD_FOLDER, filename)

        pdf_filename = os.path.splitext(filename)[0] + ".pdf"
        pdf_path = os.path.join(OUTPUT_FOLDER, pdf_filename)

        file.save(word_path)

        convert(word_path, pdf_path)

        return send_file(pdf_path, as_attachment=True)

    finally:
        pythoncom.CoUninitialize()

        # ================= JPG TO PDF =================

@app.route("/jpg-to-pdf")
def jpg_to_pdf():
    return render_template("tools/jpg_to_pdf.html")

@app.route("/convert-jpg", methods=["POST"])
def convert_jpg():

    if "images" not in request.files:
        return "No images uploaded."

    files = request.files.getlist("images")

    image_paths = []

    for file in files:

        if file.filename == "":
            continue

        filename = secure_filename(file.filename)

        image_path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(image_path)

        image_paths.append(image_path)

    output_pdf = os.path.join(OUTPUT_FOLDER, "converted_images.pdf")

    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(image_paths))

    return send_file(output_pdf, as_attachment=True)

# ================= MERGE PDF =================

@app.route("/merge-pdf")
def merge_pdf():
    return render_template("tools/merge_pdf.html")


@app.route("/merge-pdf-files", methods=["POST"])
def merge_pdf_files():

    if "pdfs" not in request.files:
        return "No PDF files uploaded."

    files = request.files.getlist("pdfs")

    merger = PdfMerger()

    for file in files:

        if file.filename == "":
            continue

        filename = secure_filename(file.filename)

        pdf_path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(pdf_path)

        merger.append(pdf_path)

    output_pdf = os.path.join(OUTPUT_FOLDER, "merged.pdf")

    merger.write(output_pdf)
    merger.close()

    return send_file(output_pdf, as_attachment=True)

# ================= SPLIT PDF =================

@app.route("/split-pdf")
def split_pdf():
    return render_template("tools/split_pdf.html")


@app.route("/split-pdf-file", methods=["POST"])
def split_pdf_file():

    if "pdf" not in request.files:
        return "No PDF uploaded."

    pdf = request.files["pdf"]

    start = int(request.form["start"])
    end = int(request.form["end"])

    filename = secure_filename(pdf.filename)

    input_path = os.path.join(UPLOAD_FOLDER, filename)

    pdf.save(input_path)

    from PyPDF2 import PdfReader, PdfWriter

    reader = PdfReader(input_path)

    writer = PdfWriter()

    for page in range(start - 1, end):

        writer.add_page(reader.pages[page])

    output_path = os.path.join(OUTPUT_FOLDER, "split.pdf")

    with open(output_path, "wb") as output:

        writer.write(output)

    return send_file(output_path, as_attachment=True)

@app.route("/compress-pdf")
def compress_pdf():
    return render_template("tools/compress_pdf.html")


# ================= ABOUT =================

@app.route("/about")
def about():
    return "<h1>About ToolHub</h1><p>Coming Soon...</p>"


# ================= CONTACT =================

@app.route("/contact")
def contact():
    return "<h1>Contact</h1><p>Coming Soon...</p>"


# ================= START APP =================

if __name__ == "__main__":
    app.run(debug=True)