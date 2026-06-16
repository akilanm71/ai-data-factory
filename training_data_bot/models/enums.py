from enum import Enum


class DocumentType(str, Enum):

    PDF = "pdf"
    TXT = "txt"
    DOCX = "docx"
    WEB = "web"
    CSV = "csv"
    PUBMED = "pubmed"


class TaskType(str, Enum):

    QA = "qa"
    SUMMARY = "summary"
    CLASSIFICATION = "classification"


class JobStatus(str, Enum):

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskType(str, Enum):

    QA_GENERATION = "qa_generation"

    CLASSIFICATION = "classification"

    SUMMARIZATION = "summarization"

    NER = "named_entity_recognition"

    RED_TEAMING = "red_teaming"

    INSTRUCTION_RESPONSE = "instruction_response"


class QualityMetric(str, Enum):

    TOXICITY = "toxicity"

    BIAS = "bias"

    DIVERSITY = "diversity"

    COHERENCE = "coherence"

    RELEVANCE = "relevance"


class ExportFormat(str, Enum):

    JSON = "json"

    JSONL = "jsonl"

    CSV = "csv"