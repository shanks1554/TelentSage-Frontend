from flask import Flask, render_template, request
import requests

app = Flask(__name__)
BACKEND_URL = "https://talentsage-backend.onrender.com/evaluate"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume = request.files.get('resume')
        position = request.form.get('position', '').strip()

        if not resume or resume.filename == '' or not position:
            return render_template("index.html", error="Please enter a position and upload your resume.")

        files = {'resume': (resume.filename, resume.stream, resume.mimetype)}
        data = {'position': position}

        try:
            response = requests.post(BACKEND_URL, files=files, data=data, timeout=30)
            result = response.json()
            result['position'] = position  # fallback in case backend doesn't echo it
            return render_template("result.html", result=result)
        except Exception:
            return render_template("index.html", error="Backend is unreachable. Please try again later.")
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)