from .templates import TaskTemplate

from ..models.qa_item import QAItem

class QAGenerator:

    def __init__(self, ai_client):

        self.ai_client = ai_client

    async def generate(self, text):

        prompt = TaskTemplate.QA.format(text=text)

        output = await self.ai_client.generate(prompt)

        lines = output.split("\n")

        question = ""
        answer = ""

        for line in lines:

            if line.startswith("Question:"):
                question = line.replace("Question:", "").strip()

            elif line.startswith("Answer:"):
                answer = line.replace("Answer:", "").strip()

        return QAItem(
            question=question,
            answer=answer)