# core/exceptions.py

# core/exceptions.py

from typing import Optional


class TrainingDataBotError(Exception):
    """
    Base exception for the entire TrainingDataBot project.
    All custom exceptions should inherit from this class.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# =========================
# Configuration Errors
# =========================

class ConfigurationError(TrainingDataBotError):
    """Invalid or missing configuration."""
    pass


# =========================
# Document & Loading Errors
# =========================

class DocumentError(TrainingDataBotError):
    """Document-related errors."""
    pass


class LoaderError(TrainingDataBotError):
    """Errors during document loading."""
    pass


class FileFormatError(LoaderError):
    """Unsupported file format."""
    pass


class EmptyDocumentError(DocumentError):
    """Document contains no content."""
    pass


# =========================
# Preprocessing Errors
# =========================

class PreprocessingError(TrainingDataBotError):
    """Text preprocessing failures."""
    pass


# =========================
# Task Generation Errors
# =========================

class TaskError(TrainingDataBotError):
    """Task generation failures."""
    pass


class UnsupportedTaskError(TaskError):
    """Unsupported task type."""
    pass


# =========================
# AI Errors
# =========================

class AIError(TrainingDataBotError):
    """AI provider failures."""
    pass


class RateLimitError(AIError):
    """AI API rate limit exceeded."""
    pass


class ModelResponseError(AIError):
    """Invalid AI response."""
    pass


# =========================
# Scraping / Decodo Errors
# =========================

class ScrapingError(TrainingDataBotError):
    """Web scraping failures."""
    pass


class URLFetchError(ScrapingError):
    """Failed to fetch URL."""
    pass


# =========================
# Evaluation Errors
# =========================

class EvaluationError(TrainingDataBotError):
    """Quality evaluation failures."""
    pass


# =========================
# Storage Errors
# =========================

class StorageError(TrainingDataBotError):
    """Storage-related failures."""
    pass


class ExportError(StorageError):
    """Dataset export failures."""
    pass


class DatabaseError(StorageError):
    """Database-related failures."""
    pass


# =========================
# Processing Job Errors
# =========================

class JobError(TrainingDataBotError):
    """Processing job failures."""
    pass


class JobTimeoutError(JobError):
    """Processing job timed out."""
    pass


class TrainingDataBotError(Exception):
    """
    Base exception for the entire TrainingDataBot project.
    All custom exceptions should inherit from this class.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# =========================
# Configuration Errors
# =========================

class ConfigurationError(TrainingDataBotError):
    """Invalid or missing configuration."""
    pass


# =========================
# Document & Loading Errors
# =========================

class DocumentError(TrainingDataBotError):
    """Document-related errors."""
    pass


class LoaderError(TrainingDataBotError):
    """Errors during document loading."""
    pass


class FileFormatError(LoaderError):
    """Unsupported file format."""
    pass


class EmptyDocumentError(DocumentError):
    """Document contains no content."""
    pass


# =========================
# Preprocessing Errors
# =========================

class PreprocessingError(TrainingDataBotError):
    """Text preprocessing failures."""
    pass


# =========================
# Task Generation Errors
# =========================

class TaskError(TrainingDataBotError):
    """Task generation failures."""
    pass


class UnsupportedTaskError(TaskError):
    """Unsupported task type."""
    pass


# =========================
# AI Errors
# =========================

class AIError(TrainingDataBotError):
    """AI provider failures."""
    pass


class RateLimitError(AIError):
    """AI API rate limit exceeded."""
    pass


class ModelResponseError(AIError):
    """Invalid AI response."""
    pass


# =========================
# Scraping / Decodo Errors
# =========================

class ScrapingError(TrainingDataBotError):
    """Web scraping failures."""
    pass


class URLFetchError(ScrapingError):
    """Failed to fetch URL."""
    pass


# =========================
# Evaluation Errors
# =========================

class EvaluationError(TrainingDataBotError):
    """Quality evaluation failures."""
    pass


# =========================
# Storage Errors
# =========================

class StorageError(TrainingDataBotError):
    """Storage-related failures."""
    pass


class ExportError(StorageError):
    """Dataset export failures."""
    pass


class DatabaseError(StorageError):
    """Database-related failures."""
    pass


# =========================
# Processing Job Errors
# =========================

class JobError(TrainingDataBotError):
    """Processing job failures."""
    pass


class JobTimeoutError(JobError):
    """Processing job timed out."""
    pass