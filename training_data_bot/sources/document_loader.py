from pathlib import Path

from ..models import (Document, DocumentType)


class DocumentLoader:
    
    def _extract_text(self, file_path):

          suffix = file_path.suffix.lower()

          if suffix == ".txt":

              return file_path.read_text(encoding="utf-8")

          elif suffix == ".md":

               return file_path.read_text(encoding="utf-8")

          else:

               raise ValueError(f"Unsupported file type {suffix}")
    


    def _get_doc_type(self, file_path):

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            return DocumentType.PDF

        elif suffix == ".txt":
            return DocumentType.TXT

        elif suffix == ".docx":
            return DocumentType.DOCX

        return DocumentType.TXT


    async def load(self, file_path):

        file_path = Path(file_path)

        text = self._extract_text(file_path)

        return Document(
            title=file_path.stem,
            content=text,
            source=str(file_path),
            doc_type=self._get_doc_type(file_path),
            word_count=len(text.split()),
            char_count=len(text)) 