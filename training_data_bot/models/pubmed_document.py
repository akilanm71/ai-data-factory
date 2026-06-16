from typing import Optional
from .base import BaseEntity
from pydantic import Field

class PubMedDocument(BaseEntity):

    pmid: str

    title: str

    content: str

    source: str = "pubmed"

    authors: list[str] = Field(default_factory=list)

    journal: Optional[str] = None

    publication_date: Optional[str] = None

    doi: Optional[str] = None

    doi_url: Optional[str] = None

    pubmed_url: Optional[str] = None

    word_count: int

    char_count: int