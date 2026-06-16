from .pubmed_service import PubMedService
from ..ai.client import AIClient
from ..tasks.templates import TaskTemplate, PubMedTemplate
from ..core.logging import get_logger

logger = get_logger(__name__)

class PubMedResearchAssistant:

    def __init__(self):

        self.pubmed_service = PubMedService()

        self.ai_client = AIClient()

    async def research(self, topic, prompt):

        docs = self.pubmed_service.ingest_papers( topic, limit=50)

        if not docs:

                logger.info("Using existing vector store")

                return await self.ai_client.generate_pubmed(topic, prompt)
        

       

        self.ai_client.add_documents(docs)
  
        result = await self.ai_client.generate_pubmed(topic, prompt)

        return result