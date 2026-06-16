from .templates import TaskTemplate


from ..models.summary_item import SummaryItem

class SummarizationGenerator:

    def __init__(self, ai_client):

        self.ai_client = ai_client

    async def generate(self, text):

        prompt = TaskTemplate.SUMMARIZATION.format(text=text)

        output = await self.ai_client.generate(prompt)

        summary = ""

        for line in output.split("\n"):

            if line.startswith("Summary:"):

                summary = line.replace("Summary:","").strip()

        return SummaryItem(
            original_text=text,
            summary=summary )