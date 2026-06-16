from datetime import datetime
from typing import List, Dict, Any
from .base import BaseEntity

from pydantic import BaseModel, Field


class Dataset(BaseEntity):

    name: str = "training_dataset"

    task_type: str = "mixed"

    items: List[Any]

    total_records: int = 0

   