from pydantic import BaseModel

class ClassificationItem(BaseModel):

    text: str

    label: str