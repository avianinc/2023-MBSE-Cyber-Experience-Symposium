from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["json_file"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        with open(filepath, "r") as f:
            data = json.load(f)

        keys = list(data.keys())
        return render_template("index.html", keys=keys)

    return render_template("index.html", keys=None)

@app.route("/data/<key>")
def get_data(key):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], request.args.get("file"))
    with open(filepath, "r") as f:
        data = json.load(f)
    return jsonify(data[key])

if __name__ == "__main__":
    app.run(debug=True)
