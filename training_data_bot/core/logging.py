from enum import Enum
from pydantic import BaseModel
from typing import Dict, Any


import logging

def get_logger(name: str) -> logging.Logger:
    
    logger = logging.getLogger(name)

    if not logger.handlers:
        
        handler = logging.StreamHandler()

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        handler.setFormatter(formatter)

        logger.addHandler(handler)
        
        logger.setLevel(logging.INFO)

    return logger


class LogContentType(str, Enum):

      DOCUMENT = "document"

      DATASET = "dataset"

      PROCESSING = "processing"

      EXPORT = "export"

      ERROR = "error"

class LogContent(BaseModel):

      action: str

      status: str

      details: Dict[str, Any] = {}

