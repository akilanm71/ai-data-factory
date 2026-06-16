# AI Data Factory

Production-ready AI system for:

- Web RAG
- PubMed Research Assistant
- Dataset Generation
- Dataset Evaluation
- ChromaDB Vector Search
- FastAPI APIs

## Features

- Load web documents
- Load PubMed papers
- Ask questions over documents
- Generate training datasets
- Evaluate dataset quality
- Clear vector stores

## Tech Stack

- Python
- FastAPI
- ChromaDB
- LangChain
- Groq
- HuggingFace Embeddings
- Airflow
- Docker (coming soon)

## Run

uvicorn training_data_bot.api.main:app --reload
