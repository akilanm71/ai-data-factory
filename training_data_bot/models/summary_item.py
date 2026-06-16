from pydantic import BaseModel

class SummaryItem(BaseModel):

    original_text: str

    summary: str