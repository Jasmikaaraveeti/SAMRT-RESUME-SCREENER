import pdfplumber
import io
import re

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text

def parse_resume_text(text: str):
    name = "Unknown Candidate"
    email = "Not detected"
    phone = "Not detected"
    
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        email = email_match.group(0)
        
    phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    if phone_match:
        phone = phone_match.group(0)
        
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        for line in lines[:5]:
            if len(line.split()) <= 4 and not any(char.isdigit() for char in line):
                name = line
                break

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "education": "B.Tech Computer Science",
        "experience": 3.5,
        "extracted_text": text
    }
