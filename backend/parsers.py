import io
import logging
import pdfplumber
import PyPDF2

def parse_resume(file) -> str:
    """Extract raw text from uploaded PDF or TXT file object."""
    if not file or not hasattr(file, "name"):
        return ""

    file_name = file.name.lower()
    text = ""

    if file_name.endswith(".pdf"):
        try:
            bytes_data = file.getvalue()
            with pdfplumber.open(io.BytesIO(bytes_data)) as pdf:
                pages_text = [page.extract_text() for page in pdf.pages if page.extract_text()]
                text = "\n".join(pages_text)
        except Exception as e:
            logging.warning("pdfplumber failed for %s: %s. Using PyPDF2 fallback.", file.name, e)
            try:
                bytes_data = file.getvalue()
                reader = PyPDF2.PdfReader(io.BytesIO(bytes_data))
                pages_text = [p.extract_text() for p in reader.pages if p.extract_text()]
                text = "\n".join(pages_text)
            except Exception as e2:
                logging.error("PyPDF2 failed for %s: %s", file.name, e2)

    elif file_name.endswith(".txt"):
        try:
            data = file.read()
            text = data.decode("utf-8", errors="ignore") if isinstance(data, bytes) else str(data)
        except Exception as e:
            logging.error("Failed reading %s: %s", file.name, e)
    else:
        logging.warning("Unsupported file format: %s", file.name)

    return text.strip()
