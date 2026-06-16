from .templates import TaskTemplate

from ..models.classification_item import ClassificationItem

class ClassificationGenerator:

    def __init__(self, ai_client):

        self.ai_client = ai_client

    async def generate(self, text):

        prompt = TaskTemplate.CLASSIFICATION.format(text=text)

        output = await self.ai_client.generate(prompt)

        label = ""

        for line in output.split("\n"):

            if line.startswith("Label:"):

                label = line.replace(
                    "Label:",
                    ""
                ).strip()

        return ClassificationItem(text=text, label=label)