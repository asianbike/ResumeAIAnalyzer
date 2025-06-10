from flask import Flask
from dotenv import load_dotenv
from flask import render_template, request
import os
import pdfplumber
from groq import Groq

load_dotenv(override=True)
api_key= os.getenv("GROQ_API_KEY")
client=Groq(api_key=api_key) # load API KEY

def build_prompt(resume_text, jd_text): #prompt function
    return f"""
너는 사람을 뽑는 리크루터야. 아래 두 텍스트를 읽고, 이 이력서가 이 직무에 적합한지 평가해줘.
부족한 점과 점수, 개선점 말해줘. 무조건 한국어로 답변해. 또, 100점 만점의 점수도 제공해줘.
[이력서]
{resume_text}
[채용공고]
{jd_text}
"""

def call_model(model_name, prompt): # reuseable
    response = client.chat.completions.create(
    model=model_name,  
    messages=[
        {"role": "user", 
         "content": prompt}
    ],
    temperature=0.2,
    max_completion_tokens=2048,
    )
    return response.choices[0].message.content
app = Flask(__name__)
app.config["UPLOAD_FOLDER"]= "Flask/uploads" #upload dir

@app.route("/", methods=["GET","POST"])
def index():
    llama_result = None
    deepseek_result = None

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
        prompt=build_prompt(resume_text,jd_text)
        llama_result=call_model("llama-3.3-70b-versatile",prompt)
        deepseek_result=call_model("deepseek-r1-distill-llama-70b",prompt)
        return render_template("result.html", llama_result=llama_result, deepseek_result=deepseek_result)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
 

    