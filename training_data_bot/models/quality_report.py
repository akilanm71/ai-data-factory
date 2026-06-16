from typing import List

from pydantic import BaseModel


class QualityReport(BaseModel):

    overall_score: float

    completeness_score: float

    consistency_score: float

    readability_score: float

    issues: List[str] = []

    recommendations: List[str] = []