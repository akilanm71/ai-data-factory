from .pdf_loader import PDFLoader
from .document_loader import DocumentLoader
from .web_loader import WebLoader
from .csv_loader import CSVLoader
from pathlib import Path


class UnifiedLoader:

    def __init__(self):

        self.pdf_loader = PDFLoader()

        self.doc_loader = DocumentLoader()

        self.web_loader = WebLoader()

        self.csv_loader = CSVLoader()
    
    async def load_single(self, source):

         source = str(source)

         if source.startswith(("http://", "https://")):

                     return await self.web_loader.load(source)
         

         suffix = Path(source).suffix.lower()

         if suffix == ".pdf":

                      return await self.pdf_loader.load(source)

         elif suffix in [".txt",".docx",".md"]:

                      return await self.doc_loader.load(source)
         
         elif suffix == ".csv":
                      
                      return await self.csv_loader.load(source)

         raise ValueError(f"Unsupported source {source}")

    async def load_directory(self,directory):

             documents = []

             directory = Path(directory)

             for file in directory.iterdir():

                   if file.is_file():

                         doc = await self.load_single(file)

                         documents.append(doc)

             return documents            