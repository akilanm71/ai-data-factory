from pathlib import Path
from pypdf import PdfReader
from ..models.document import Document, DocumentType


def extract_pdf_text(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        text += page.extract_text() or ""

    return text

class PDFLoader:

    async def load(self, file_path):
              file_path = Path(file_path)
              text = extract_pdf_text(file_path)

              return Document(
                              title=file_path.stem,
                              content=text,
                              source= str(file_path),
                              doc_type= DocumentType.PDF,
                              word_count=len(text.split()),
                              char_count=len(text))