from flask import Flask, jsonify, render_template, request
from model import Model

app = Flask(__name__)
model = Model()


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