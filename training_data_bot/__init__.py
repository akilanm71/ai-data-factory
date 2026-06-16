"""Training Data Curated Bot """


__version__ = "0.1.0"
__author__ ="Training DAta BOt"
__email__ = "akilanjai71@gmail.com" 
__description__ = "Trying to Implement CHATBOT for Research"





from .core.config import Settings
from .core.logging import  get_logger
from .core.exceptions import TrainingDataBotError


from .sources.pdf_loader import PDFLoader
from .sources.web_loader import WebLoader
from .sources.document_loader import DocumentLoader
from .sources.unified_loader import UnifiedLoader
from .sources.pubmed_loader import PubMedLoader

from .tasks.qa_generator import QAGenerator
from .tasks.classification_generator import ClassificationGenerator
from .tasks.summarization_generator import SummarizationGenerator
from .tasks.templates import TaskTemplate
from .tasks.task_manager import TaskManager

from .services.decodo_client import DecodoClient
from .services.text_preprocessor import TextPreprocessor
from .services.quality_evaluator import QualityEvaluator
from .services.dataset_explorer import DatasetExporter
from .services.pubmed_service import PubMedService
from .services.research_assistant import PubMedResearchAssistant
from .storage.incremental_manager import IncrementalManager

from .ai.client import AIClient

__all__ = [
    
    "settings",
    "get_logger",
    "TrainingDataBotError",
    "TrainingDataBotError",

    "PDFLoader",
    "WebLoader",
    "DocumentLoader",
    "UnifiedLoader",
    "PubMedLoader"

    "QAGenerator",
    "ClassificationGenerator",
    "SummarizationGenerator",
    "TaskTemplate",
    "TaskManager"

    "DecodoClient",
    "TextPreprocessor",
    "QualityEvaluator",
    "DatasetExporter",
    "PubMedResearchAssistant"
    "PubMedService"
    "IncrementalManager"

    "AIClient"
]