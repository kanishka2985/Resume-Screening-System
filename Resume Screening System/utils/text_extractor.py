import pdfplumber
from docx import Document


#  PDF TEXT EXTRACTION 
def extract_text_from_pdf(file_path):
    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

    except Exception as e:
        print(f"Error reading PDF: {e}")

    return text.strip()


# DOCX TEXT EXTRACTION 
def extract_text_from_docx(file_path):
    text = ""

    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    except Exception as e:
        print(f"Error reading DOCX: {e}")

    return text.strip()


#  AUTO DETECT FILE TYPE 
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)

    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")