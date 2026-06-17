import asyncio
import traceback

import pandas as pd
from pathlib import Path
from typing import Dict, Optional, List, Union, Any
from uuid import UUID

from .core.config import Settings
from .core.logging import get_logger, LogContent
from .core.exceptions import TrainingDataBotError, ConfigurationError

from .sources import UnifiedLoader
from .sources.pubmed_loader import PubMedLoader
 
from .tasks import  QAGenerator, ClassificationGenerator , SummarizationGenerator , TaskTemplate


from .services.decodo_client import DecodoClient
from .services.pubmed_service import PubMedService
from .services.research_assistant import PubMedResearchAssistant

from .ai import AIClient

from .models import (Document, Dataset, ProcessingJob, QualityReport)

from .models.enums import (TaskType, DocumentType, ExportFormat)

from .tasks import TaskManager
from .tasks.templates import TaskTemplate, PubMedTemplate
from .services import TextPreprocessor
from .services import QualityEvaluator
from .storage import DatasetExplorer, DatabaseManager, IncrementalManager
from .services import DatasetExporter

class TrainingDataBot:
           """
           Main Training Bot class
           
           This Class provides a high-level interface for :
           
            - Loading documents from various sources
            - Procvessing text with task Template
            -Quality assessment and filetering
            - Dastaset creation and exporrt
             """
           def __init__( self, config: Optional[Dict[str, Any]]= None):
                      self.logger = get_logger("training_data_bot")
                      self.config = config or {}
                      self._init_components()
                      self.logger.info("Training Dta Bot initialized sucessfully")
                      
           def _init_components(self):
                      """ Initialize all bot components"""
                      try:
                             self.loader = UnifiedLoader()
                             self.decodo_client = DecodoClient()
                             self.ai_client = AIClient()
                             self.task_manager = TaskManager(self.ai_client)
                             self.preprocessor = TextPreprocessor()
                             self.evaluation = QualityEvaluator()
                             self.database_manager = DatabaseManager("storage/data.jsonl")
                             self.data_explorer = DatasetExplorer(self.database_manager)
                             self.incremental_manager = IncrementalManager()
                             self.pubmed_loader =  PubMedLoader()
                             self.exporter = DatasetExporter()
                             self.pubmed_service = PubMedService()
                             # State (Memory boxes)
                             self.documents : Dict [ UUID , Document ] = {}
                             self.datasets : Dict [ UUID , Dataset ] = {}
                             self.jobs : Dict [ UUID , ProcessingJob ] = {}
                            
                      except Exception as e:
                             
                             traceback.print_exc()

                             raise 
           
                        
           async def __aenter__ ( self ):
                             print("Connecting database")

                             await self.db_manager.connect()
                             return self
            
           async def run(self):
                        print("Bot running")
                        print("Loader:", self.loader)
                        print("AI:", self.ai_client)
                        print("Task Manager:", self.task_manager)

                        print("Initialization successful")     


           async def load_documents(self, sources: Union[str, Path, List[Union[str, Path]]], doc_types: Optional[List[DocumentType]] = None, 
                                                      metadata: Optional[Dict[str, Any]] = None, **kwargs) -> List[Document]:
       

                   if isinstance(sources, (str, Path)):
                            
                            sources = [sources]

                   documents = []

                   for source in sources:

                   # URL
                            if str(source).startswith(("http://", "https://")):

                                doc = await self.loader.load_single(source)

                                if metadata:
                                   
                                   doc.metadata.update(metadata)

                                documents.append(doc)

                                continue

                            source_path = Path(source)

                   # Document type filtering
                            if doc_types:

                                  extension = (source_path.suffix.lower().replace(".", ""))

                                  allowed_types = [doc_type.value for doc_type in doc_types]

                                  if extension not in allowed_types:
                                         continue

                   # Directory loading
                            if source_path.is_dir():

                                  dir_docs = await self.loader.load_directory(source_path)

                                  documents.extend(dir_docs)

                   # Single file loading
                            else:

                                   doc = await self.loader.load_single(source_path)

                                   if metadata:
                                          doc.metadata.update(metadata)

                                   documents.append(doc)

                   # Store in memory
                   for doc in documents:

                           self.documents[doc.id] = doc

                   self.logger.info(f"Loaded {len(documents)} documents")

                   return documents
            
           async def process_documents (self ,documents : Optional [ List [ Document ]] = None ,
                                         task_types : Optional [ List [ TaskType ]] = None , quality_filter : bool = True , ** kwargs) -> Dataset :
                             if documents is None:
                                       
                                       documents = list(self.documents.values())
                             if task_types is None:
                                       
                                       task_types = [TaskType.QA_GENERATION]
                             
                             processed_items = []

                             for doc in documents:

                                      cleaned_doc = self.preprocessor.clean(doc)

                                      chunks = self.preprocessor.chunk(cleaned_doc)

                                      tasks = await self.task_manager.generate_tasks(chunks,task_types)

                                      processed_items.extend(tasks)

                                      if quality_filter:

                                            processed_items = self.evaluation.filter(processed_items)

                             dataset = Dataset(items=processed_items)

                             return dataset
                
           async def evaluate_dataset(self,dataset: Dataset) -> QualityReport:

                       if not dataset.items:

                             return await self.evaluation.eval_dataset([])

                       scores = []

                       for item in dataset.items:

                              score = await self.evaluation.score(item)

                              scores.append(score)

                       average_score = sum(scores) / len(scores)

                       print("Average Score:", average_score)

                       return await self.evaluation.eval_dataset(dataset.items)

           async def export_dataset(self, dataset: Dataset, output_path: Union[str, Path], format: ExportFormat = ExportFormat.JSONL, split_data: bool = True, **kwargs) -> Path:
                             """ Export Data to Disk"""

                               
                             try:

                                         output_path = Path(output_path)

                                         if not dataset.items:
                                             raise TrainingDataBotError("Dataset is empty")

                                         if split_data:

                                               train_data, test_data = (self.exporter.split_dataset(dataset))

                                               await self.exporter.export(train_data, output_path / "train.jsonl", format)

                                               await self.exporter.export(test_data, output_path / "test.jsonl", format)

                                         else:

                                               await self.exporter.export(dataset, output_path, format )

                                         self.logger.info("Dataset exported successfully")

                                         return output_path

                             except Exception as e:

                                         raise TrainingDataBotError(f"Export failed: {e}")
           def _count_by_type(self):

                      counts = {}

                      for doc in self.documents.values():

                                 counts[doc.doc_type] = (counts.get(doc.doc_type, 0) + 1)

                      return counts
            
           def get_statistics(self) -> Dict[str, Any]:
                 return {
                         "documents" : {
                                 "total" : len(self.documents) , 
                                 "by_type" : self._count_by_type(),
                                 "total_size": sum(doc.word_count for doc in self.documents.values())

                         }, 
                         "datasets" :{"total" :len(self.datasets),
                                      "total_exaples": sum(len(ds.items) for ds in self.datasets.values() )},
                                      "jobs": {"total": len(self.jobs)}}
           
           async def load_web_documents(self, sources: Union[str, Path, List[Union[str, Path]]],
                             doc_types: Optional[List[DocumentType]] = None,
                             metadata: Optional[Dict[str, Any]] = None,
                            forget: bool = False):

                         documents = await self.load_documents(sources=sources,
                                     doc_types=doc_types, metadata=metadata)

                         self.ai_client.add_documents_web( documents, forget=forget)

                         return documents
           
           async def ask_web(self, question):

                    return await self.ai_client.generate(question)
           
           async def load_pubmed_documents(self, query: str, limit: int = 20):

                    documents = self.pubmed_service.ingest_papers(query=query, limit=limit)

                    self.ai_client.add_documents(documents)

                    return documents
           async def ask_pubmed(self, question: str):

                    return await self.ai_client.generate_pubmed(question, PubMedTemplate.LITERATURE_REVIEW)
           
           async def build_dataset(self, documents):

                   dataset = await self.process_documents(documents)

                   return dataset
           
           async def evaluate(self, dataset):

                   report = await self.evaluate_dataset(dataset)

                   return report
           async def export(self, dataset, output_dir="output"):

                   return await self.export_dataset(dataset=dataset, output_path=output_dir)

           async def dataset_pipeline(self, source):

                documents = await self.load_documents(source)

                dataset = await self.process_documents(documents)

                report = await self.evaluate_dataset(dataset)

                await self.export_dataset( dataset, "output")

                stats = self.get_statistics()

                return {"dataset": dataset,
                        "report": report,
                        "stats": stats}
           
           async def clear_pubmed(self):

                self.ai_client.clear_pubmed_store()

                return {
                    "status": "success",
                    "message": "PubMed vector store cleared"}

           async def cleanup(self):

                        try:

                         ### await self.database_manager.close() 

                             if hasattr(self.decodo_client, "close"):
                                      await self.decodo_client.close()

                             if hasattr(self.ai_client, "close"):
                                      await self.ai_client.close()

                             self.logger.info("Bot cleanup completed")

                        except Exception as e:
                             self.logger.error(f"Cleanup failed: {e}")

           async def clear_web_store(self):

                        self.ai_client.clear_web_store()

           async def __aexit__ ( self , exc_type , exc_val , exc_tb ) :
          
                             await self.cleanup ()


"""

import asyncio

from training_data_bot.bot import TrainingDataBot


async def main():

    bot = TrainingDataBot()

    result = await bot.dataset_pipeline(
        "https://medium.com/@codeidoscope/load-testing-and-improving-the-performance-of-my-http-server-ab6ff70ced60"
    )

    print("\n=== PIPELINE SUCCESS ===")

    print(result.keys())

    print("\nDataset:")
    print(result["dataset"])

    print("\nReport:")
    print(result["report"])

    print("\nStats:")
    print(result["stats"])

"""
   



'''async def main():

    bot = TrainingDataBot()

    print("\n=== Load PubMed ===")

    docs = await bot.load_pubmed_documents(
        query="lung cancer",
        limit=5
    )

    print(f"Loaded {len(docs)} papers")

    print("\n=== Ask PubMed ===")

    answer = await bot.ask_pubmed(
        "Summarize lung cancer research"
    )

    print(answer)

    print("\n=== Delete PubMed Store ===")

    await bot.clear_pubmed()

    print("PubMed vector store deleted")

    print("\n=== Verify Delete ===")

    docs = bot.ai_client.retriever.invoke("cancer")

    print("Retrieved docs:", len(docs))

    answer = await bot.ask_pubmed(
        "Summarize lung cancer research"
    )

    print(answer)'''



"""assistant = PubMedResearchAssistant()

    result = await assistant.research("lung cancer",PubMedTemplate.LITERATURE_REVIEW)

    print(result)


if __name__ == "__main__":

    asyncio.run(main())

       docs = await bot.load_documents("https://pubmed.ncbi.nlm.nih.gov/?term=carcinoma")

             print(f"Loaded {len(docs)} docs")
           
             
             dataset = await bot.process_documents(docs, task_types=[ TaskType.SUMMARIZATION])

             print(f"Generated {len(dataset.items)} items")

             report = await bot.evaluate_dataset(dataset)

             print(report)

             stats = bot.get_statistics()

             df = pd.DataFrame([
                {
        "total_documents": stats["documents"]["total"],
        "total_size": stats["documents"]["total_size"],
        "total_datasets": stats["datasets"]["total"],
        "total_examples": stats["datasets"]["total_exaples"],
        "total_jobs": stats["jobs"]["total"]   
    }
])

             print(df) 
             """
             
             
                         

