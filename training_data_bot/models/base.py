import pydantic

from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Dict, Any, Optional


class BaseEntity(BaseModel):

    id: UUID = Field(default_factory=uuid4)

    created_at: datetime = Field(default_factory=datetime.now)

    updated_at: Optional[datetime] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def touch(self):

        self.updated_at = datetime.now()




        