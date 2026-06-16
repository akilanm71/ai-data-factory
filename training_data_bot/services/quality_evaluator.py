# services/quality_evaluator.py

from typing import List

from ..models import QualityReport


class QualityEvaluator:

    def filter(self, items: List):

        return [item for item in items if self.is_valid(item)]

    def is_valid(self, item) -> bool:

        if hasattr(item, "question"):
            return bool(item.question and item.answer)

        if hasattr(item, "summary"):
            return bool(item.summary)
        
        if hasattr(item, "label"):
            return bool(item.label)

        return False

    async def score(self, item) -> float:

        completeness = self._completeness_score(item)

        readability = self._readability_score(item)

        consistency = self._consistency_score(item)

        return (completeness + readability + consistency) / 3

    async def eval_dataset(self, items: List) -> QualityReport:

        if not items:

            return QualityReport(overall_score=0, completeness_score=0,
                consistency_score=0, readability_score=0, issues=["Dataset is empty"],
                recommendations=["Generate more records"])

        completeness_scores = []
        readability_scores = []
        consistency_scores = []

        issues = []

        for item in items:

            completeness_scores.append(self._completeness_score(item))

            readability_scores.append(self._readability_score(item))

            consistency_scores.append(self._consistency_score(item))

            if hasattr(item, "answer"):

                 if len(item.answer) < 20:

                      issues.append("Short answer detected")

        completeness = (sum(completeness_scores) / len(completeness_scores))

        readability = (sum(readability_scores) / len(readability_scores))

        consistency = (sum(consistency_scores) / len(consistency_scores))

        overall = (completeness + readability + consistency) / 3

        recommendations = []

        if overall < 80:

            recommendations.append("Regenerate low quality samples")

        return QualityReport(
            overall_score=overall,
            completeness_score=completeness,
            consistency_score=consistency,
            readability_score=readability,
            issues=issues,
            recommendations=recommendations)

    def _completeness_score(self, item):
 
        if hasattr(item, "question"):
               
               score = 0

               if item.question:
                    score += 50

               if item.answer:
                    score += 50

               return score
        elif hasattr(item, "summary"):

               return 100 if item.summary else 0

        return 0

    def _readability_score(self, item):

        if hasattr(item, "answer"):

                   text = item.answer

        elif hasattr(item, "summary"):

                   text = item.summary

        elif hasattr(item, "label"):

                  text = item.label

        else:

                  return 0

        answer_length = len(text)

        if answer_length > 100:
            return 100

        if answer_length > 50:
            return 90

        if answer_length > 20:
            return 75

        return 50

    def _consistency_score(self, item):

        print("TYPE:", type(item))
        print("ITEM:", item)

        if hasattr(item, "question") and hasattr(item, "answer"):

             if item.question.lower() in item.answer.lower():

                    return 70

             return 90

        return 100