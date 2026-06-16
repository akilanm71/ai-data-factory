

from ..sources.pubmed_loader import PubMedLoader
from ..storage.incremental_manager import IncrementalManager
from ..models.pubmed_document import PubMedDocument

from ..core.logging import get_logger

logger = get_logger(__name__)

class PubMedService:

    def __init__(self):

        self.loader = PubMedLoader() 

        self.incremental_manager = IncrementalManager()

    def ingest_papers(self, query: str, limit: int = 10):
        
        print(f"Searching PubMed for: {query}")

        pmids = self.loader.search(query, limit)

        print(f"PMIDs found: {len(pmids)}")

        new_pmids = self.incremental_manager.get_new_pmids(pmids) 

        print(f"New PMIDs: {new_pmids}")

        if new_pmids is None:

                 logger.info("First run detected. Processing all PMIDs.")

                 new_pmids = pmids

        elif len(new_pmids) == 0:

                 logger.info("No new PMIDs found.")

                 return []

        documents = []

        for pmid in new_pmids:

            try:

                  abstract = self.loader.fetch_abstract(pmid)

                  metadata = self.loader.fetch_metadata(pmid) or {}

                  print("METADATA TYPE =", type(metadata))
                  print("METADATA =", metadata)

                  if not abstract:
                        
                        logger.warning(f"No abstract found for PMID={pmid}")
                        continue

                  doc = PubMedDocument(
                                    pmid=pmid,
                                    title=metadata.get("title", ""),
                                    content=abstract,
                                    authors=metadata.get("authors", []),
                                    journal=metadata.get("journal", ""),
                                    publication_date=metadata.get("publication_date", ""),
                                    doi=metadata.get("doi", ""),
                                    doi_url=metadata.get("doi_url", ""),
                                    pubmed_url=metadata.get("pubmed_url", ""),
                                    word_count=len(abstract.split()),
                                    char_count=len(abstract))

                  documents.append(doc)
        
                  self.incremental_manager.save_id(pmid)
                  
            except Exception as e:

                  logger.error(f"Failed processing PMID={pmid}: {e}")

        logger.info(f"PubMed ingestion completed | "
                     f"PMIDs={len(pmids)} | "
                     f"New PMIDs={len(new_pmids)} | "
                     f"Documents={len(documents)}")
        
        return documents

       