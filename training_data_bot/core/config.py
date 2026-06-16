from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("Loaded key:", GROQ_API_KEY)


class Settings(BaseModel):

    # Application
    app_name: str = "TrainingDataBot"
    version: str = "1.0"

    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Dataset
    train_split: float = 0.8

    # Quality
    quality_threshold: float = 0.7

    # Database
    database_url: str = "sqlite:///bot.db"

    # AI
    model_name: str = "gpt-4"

    # Export
    export_format: str = "jsonl"


