import os
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
from model import Model

app = Flask(__name__)
model = Model()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = None
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        content = model.extract_file_content(filepath)
        return jsonify({
            "filename": filename,
            "content": content,
            "type": filename.rsplit(".", 1)[1].lower(),
            "size": os.path.getsize(filepath),
        })
    return jsonify({"error": "File type not allowed"}), 400


@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        data = request.get_json()
        messages = data.get("messages", [])
        query = messages[-1]["content"] if messages else ""
        reply = model.get_answer(query)
        return jsonify({"content": [{"text": reply}]})

    return render_template("chat.html")


app.run(debug=True, host="127.0.0.1", port="1648")