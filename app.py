from flask import Flask, request, render_template, send_file
from PIL import Image, ImageOps
import os
import math
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        num_pages_wide = int(request.form["pages"])

        a4_width_mm, a4_height_mm = 210, 297
        dpi = 300
        a4_width_px = int((a4_width_mm / 25.4) * dpi)
        a4_height_px = int((a4_height_mm / 25.4) * dpi)

        img = Image.open(file)
        aspect_ratio = img.height / img.width
        total_width = num_pages_wide * a4_width_px
        total_height = int(total_width * aspect_ratio)
        num_pages_high = math.ceil(total_height / a4_height_px)
        img_resized = img.resize((total_width, total_height), Image.LANCZOS)

        output_dir = os.path.join(UPLOAD_FOLDER, "poster_pages")
        os.makedirs(output_dir, exist_ok=True)

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
                filename = f"page_{row+1:02}_{col+1:02}.jpg"
                page_with_border.save(os.path.join(output_dir, filename), "JPEG")
                count += 1

        zip_path = os.path.join(UPLOAD_FOLDER, "poster_pages.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for filename in os.listdir(output_dir):
                filepath = os.path.join(output_dir, filename)
                zipf.write(filepath, arcname=filename)

        return send_file(zip_path, as_attachment=True)

    return render_template("index.html")
