from flask import Flask
from flask import render_template, request
import os
import pdfplumber
from dotenv import load_dotenv

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]= "Flask/uploads" #upload dir

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        #1 file upload
        resume_file=request.files["resume"]
        jd_text=request.form["jd_text"]

        resume_path = os.path.join(app.config["UPLOAD_FOLDER"],resume_file.filename)
        resume_file.save(resume_path)

        resume_text=""
        with pdfplumber.open(resume_path) as pdf :
            for page in pdf.pages:
                text=page.extract_text()
                if text:
                    resume_text+=text+"\n"

        print("✅ JD 텍스트:")
        print(jd_text[:300])
        print("✅ 이력서 텍스트:")
        print(resume_text[:300])
        return "입력 처리 성공"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
 

    