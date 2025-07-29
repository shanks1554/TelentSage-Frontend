from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
BACKEND_URL = "https://talentsage-backend.onrender.com/evaluate"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        resume = request.files.get("resume")
        position = request.form.get("position")

        if resume and position:
            files = {"resume": (resume.filename, resume.stream, resume.mimetype)}
            data = {"position": position}
            try:
                response = requests.post(BACKEND_URL, files=files, data=data)
                result = response.json()
            except Exception as e:
                result = {"error": str(e)}
        else:
            result = {"error": "Please upload a resume and enter a position."}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
