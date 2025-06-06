import pdfplumber
with pdfplumber.open("readpdf.pdf") as pdf:
    full_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text
print(full_text[:500])
