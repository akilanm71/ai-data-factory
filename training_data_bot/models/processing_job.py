from datetime import datetime
from pydantic import BaseModel, Field


class ProcessingJob(BaseModel):

    job_id: str

    status: str

    progress: float = 0.0

    documents_processed: int = 0

    total_documents: int = 0

    started_at: datetime = Field(
        default_factory=datetime.now
    )

    completed_at: datetime | None = None