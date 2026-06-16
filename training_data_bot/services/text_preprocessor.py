import re
from typing import List

from ..models import Document


class TextPreprocessor:

    def clean(self,document: Document) -> Document:

        text = document.content

        text = self.remove_extra_spaces(text)

        text = self.remove_urls(text)

        text = self.normalize_text(text)

        document.content = text

        return document

    def chunk(self, document: Document, chunk_size: int = 500) -> List[str]:

        text = document.content

        words = text.split()

        chunks = []

        for i in range(0,len(words),chunk_size):

            chunk = " ".join(words[i:i + chunk_size])

            chunks.append(chunk)

        return chunks

    def remove_urls(self, text: str) -> str:

        return re.sub(r"http\S+","",text)

    def remove_extra_spaces(self, text: str) -> str:

        return " ".join(text.split())

    def normalize_text(self,text: str) -> str:

        return text.strip()