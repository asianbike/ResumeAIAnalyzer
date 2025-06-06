import os
from openai import OpenAI
import pdfplumber
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client=OpenAI(api_key=api_key)
print("✅ Loaded API key:", api_key)
