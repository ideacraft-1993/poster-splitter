
from flask import Flask, request, render_template, send_file
from PIL import Image, ImageOps
import os
import math
import zipfile
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "poster_pages"
ZIP_FILENAME = "poster_pages.zip"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        num_pages_wide = int(request.form["num_pages_wide"])
        if not file:
            return "No file uploaded", 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        img = Image.open(filepath)

        a4_width_mm, a4_height_mm = 210, 297
        dpi = 300
        a4_width_px = int((a4_width_mm / 25.4) * dpi)
        a4_height_px = int((a4_height_mm / 25.4) * dpi)

        aspect_ratio = img.height / img.width
        total_width = num_pages_wide * a4_width_px
        total_height = int(total_width * aspect_ratio)
        num_pages_high = math.ceil(total_height / a4_height_px)

        img_resized = img.resize((total_width, total_height), Image.LANCZOS)

        for f in os.listdir(OUTPUT_FOLDER):
            os.remove(os.path.join(OUTPUT_FOLDER, f))

        border_size = 20
        count = 1
        for row in range(num_pages_high):
            for col in range(num_pages_wide):
                left = col * a4_width_px
                upper = row * a4_height_px
                right = min(left + a4_width_px, img_resized.width)
                lower = min(upper + a4_height_px, img_resized.height)
                page = img_resized.crop((left, upper, right, lower))
                page_with_border = ImageOps.expand(page, border=border_size, fill="white")
                page_with_border.save(os.path.join(OUTPUT_FOLDER, f"page_{row+1}_{col+1}.jpg"), "JPEG")
                count += 1

        with zipfile.ZipFile(ZIP_FILENAME, "w") as zipf:
            for root, _, files in os.walk(OUTPUT_FOLDER):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)

        return send_file(ZIP_FILENAME, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
