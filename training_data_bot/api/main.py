
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from training_data_bot.bot import TrainingDataBot

from training_data_bot.services.research_assistant import PubMedResearchAssistant
from training_data_bot.tasks.templates import PubMedTemplate

import logging

logger = logging.getLogger(__name__)



app = FastAPI(title="Training Data Bot")

@app.on_event("startup")
async def startup():
    global bot
    bot = TrainingDataBot()
    logger.info("Application started")

class WebLoadRequest(BaseModel):
    source: str
    forget: bool = False


class QuestionRequest(BaseModel):
    question: str


class PubMedRequest(BaseModel):
    query: str
    limit: int = 20


class DatasetRequest(BaseModel):
    source: str

class AnswerResponse(BaseModel):
    answer: str

@app.get("/")
async def root():
    return {"message": "Training Data Bot API Running"}

@app.post("/web/load")
async def load_web(req: WebLoadRequest):

    docs = await bot.load_web_documents(sources=req.source, forget=req.forget)

    return {
        "status": "success",
        "documents": len(docs)}

@app.post("/web/ask", response_model=AnswerResponse)
async def ask_web(req: QuestionRequest):

    answer = await bot.ask_web(req.question)

    if not answer:
        raise HTTPException(
            status_code=400,
            detail="No Web documents found"
        )

    return {"answer": answer}


@app.post("/pubmed/load")
async def load_pubmed(req: PubMedRequest):

    docs = await bot.load_pubmed_documents(query=req.query, limit=req.limit)

    return {"documents": len(docs)}

@app.post("/pubmed/ask", response_model=AnswerResponse)
async def ask_pubmed(req: QuestionRequest):

    answer = await bot.ask_pubmed(req.question)

    if not answer:
        raise HTTPException(
            status_code=400,
            detail="No PubMed documents found")

    return {"answer": answer}

@app.post("/pubmed/research")
async def research_pubmed(req: PubMedRequest):

    assistant = PubMedResearchAssistant()

    result = await assistant.research(req.query, PubMedTemplate.LITERATURE_REVIEW)

    return { "result": result}

@app.post("/dataset/build")
async def build_dataset(req: DatasetRequest):

    result = await bot.dataset_pipeline(req.source)

    return {
        "report": str(result["report"]),
        "stats": result["stats"]}

@app.get("/stats")
async def stats():

    return bot.get_statistics()

@app.delete("/pubmed/delete")
async def delete_pubmed():

    return await bot.clear_pubmed()

@app.delete("/web/delete")
async def delete_web():

    return await bot.clear_web_store()