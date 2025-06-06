import os
from openai import OpenAI
import pdfplumber
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client=OpenAI(api_key=api_key)
print("✅ Loaded API key:", api_key)

with pdfplumber.open("readpdf.pdf") as pdf:
    resume_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            resume_text += text + "\n"

with open("JD1.txt","r",encoding="utf-8") as f:
    jd_text=f.read() #JD 텍스트 빼기

prompt = f"""
너는 사람을 뽑는 리크루터야. 아래 두 텍스트를 읽고, 이 이력서가 이 직무에 적합한지 평가해줘.
부족한 점과 점수, 개선점 말해줘.

[이력서]
{resume_text}

[채용공고]
{jd_text}
"""
response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # out of quota, shift to groq - llama 3 / deepseek model
    messages=[
        {"role": "user", "content": prompt}
    ]
)
result = response.choices[0].message.content
print(result)