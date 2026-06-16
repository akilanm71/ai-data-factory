from langchain_groq import ChatGroq

from langchain_huggingface import (HuggingFaceEmbeddings)

from langchain_chroma import Chroma

from langchain_core.documents import Document as LCDocument

from ..core.config import GROQ_API_KEY


class AIClient:

    def __init__(self):

        # LLM

        self.llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile",
                            temperature=0.3)

        # Embeddings

        self.embeddings = (HuggingFaceEmbeddings(
                          model_name="sentence-transformers/all-MiniLM-L6-v2"))

        # Vector Store

        self.vectorstore = Chroma(persist_directory="./vectordb",
                           embedding_function=self.embeddings)
        
        self.web_vectorstore = Chroma(persist_directory="./web_vectordb",
                              embedding_function=self.embeddings)

        
        self.retriever = (self.vectorstore.as_retriever(search_kwargs={"k": 15}))

        self.web_retriever = self.web_vectorstore.as_retriever()

    async def generate(self,prompt: str):

        docs = self.web_retriever.invoke(prompt)

        context = "\n\n".join(doc.page_content for doc in docs)

        final_prompt = f"""Context:{context}

        Question:
        {prompt}

        Answer:
        """

        response = self.llm.invoke(final_prompt)

        return response.content
    
    async def generate_norm(self, prompt):

             response = self.llm.invoke(prompt)

             return response.content
    
    async def generate_pubmed(self, query, template):

            docs = self.retriever.invoke(query)
            
            if not docs:
                    
                    return "No PubMed documents found in vector store."
            
            context = "\n\n".join(doc.page_content for doc in docs)

            final_prompt = template.format(text=context)

            response = self.llm.invoke(final_prompt)

            return response.content

    def add_documents(self, documents):
         
         if not documents:
              print("No documents to add")
              return
        
         lc_documents = []

         for doc in documents:
              
             if not doc.content:
                    
                    continue
            
             words = doc.content.split()

             chunk_size = 500
             
             for i in range(0, len(words), chunk_size):

                     chunk = " ".join(words[i:i + chunk_size])
                     
                     lc_documents.append(LCDocument( page_content=chunk,
                                   metadata={"title": doc.title,
                                            "source": doc.source}))
         if not lc_documents:
               print("No chunks generated")
               return

         self.vectorstore.add_documents(lc_documents)

         self.retriever = self.vectorstore.as_retriever()

         print("Number of documents:", len(documents))
         print("Number of chunks:", len(lc_documents))

    def add_documents_web(self, documents, forget=False):

        if forget:

            try:
                    self.web_vectorstore.delete_collection()
            except:
                    pass

            self.web_vectorstore = Chroma( persist_directory="./web_vectordb",
                                   embedding_function=self.embeddings)
            self.web_retriever = self.web_vectorstore.as_retriever()

        lc_documents = []

        for doc in documents:

               words = doc.content.split()

               for i in range(0, len(words), 500):

                    chunk = " ".join(words[i:i+500])

                    lc_documents.append(LCDocument(
                                    page_content=chunk,
                                    metadata={
                                         "title": doc.title,
                                        "source": doc.source} ))

        self.web_vectorstore.add_documents(lc_documents)

        self.web_retriever = self.web_vectorstore.as_retriever()

        print("Web Documents:", len(documents))
        print("Web Chunks:", len(lc_documents))

    def clear_pubmed_store(self):
        
        print("CLEAR PUBMED CALLED")
        
        try:

               self.vectorstore.delete_collection()

        except Exception as e:

                print(f"Error clearing PubMed store: {e}")

        self.vectorstore = Chroma(persist_directory="./vectordb",
                             embedding_function=self.embeddings)

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 15})

        print("PubMed vector store cleared")

    def clear_web_store(self):

                        try:
        
                              self.web_vectorstore.delete_collection()
                        
                        except:
                                 
                                pass

                        self.web_vectorstore = Chroma(
                                 persist_directory="./web_vectordb",
                                 embedding_function=self.embeddings)

                        self.web_retriever = self.web_vectorstore.as_retriever()

    async def close(self):
        
        pass