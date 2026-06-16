from .base import BaseEntity
from .enums import DocumentType


class Document(BaseEntity):

    title: str

    content: str

    source: str

    doc_type: DocumentType

    word_count: int

    char_count: int