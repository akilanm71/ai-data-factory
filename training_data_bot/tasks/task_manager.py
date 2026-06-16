from .qa_generator import QAGenerator
from .classification_generator import ClassificationGenerator
from .summarization_generator import SummarizationGenerator
from ..models.enums import TaskType


class TaskManager:

    def __init__(self, ai_client):

        self.qa_generator = QAGenerator(ai_client)

        self.classification_generator = (ClassificationGenerator(ai_client))

        self.summarization_generator = (SummarizationGenerator(ai_client))
   

    
    async def generate_tasks(self, chunks, task_types):

          examples = []

          for chunk in chunks:

                  for task_type in task_types:

                       if task_type == TaskType.QA_GENERATION:

                               result = await self.qa_generator.generate(chunk)

                       elif task_type == TaskType.SUMMARIZATION:

                               result = await self.summarization_generator.generate(chunk)

                       elif task_type == TaskType.CLASSIFICATION:

                               result = await self.classification_generator.generate(chunk)

                       examples.append(result)

          return examples