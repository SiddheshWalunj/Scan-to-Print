from PyPDF2 import PdfReader

def get_pdf_page_count(file):
    reader = PdfReader(file)
    return len(reader.pages)
