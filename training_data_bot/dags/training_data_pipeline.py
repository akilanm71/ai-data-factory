from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

import sys
import os

PROJECT_ROOT = "/mnt/c/Users/AKILAN M/Documents/Akilan_chat_bot/Project"

if PROJECT_ROOT not in sys.path:
             sys.path.insert(0, PROJECT_ROOT)

from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def ingest_pubmed():


    from training_data_bot.services.pubmed_service import PubMedService

    service = PubMedService()

    docs = service.ingest_papers(query="lung cancer", limit=50)

    logger.info("Documents fetched: %s", len(docs))

    return docs


def update_vectorstore(**context):

    from training_data_bot.ai.client import AIClient


    docs = context["ti"].xcom_pull(task_ids="ingest_pubmed")

    if not docs:
        logger.warning("No documents found from ingest_pubmed")
        return
    
    client = AIClient()

    logger.info("Adding %s docs to vector store", len(docs))

    client.add_documents(docs)

    logger.info("Documents added successfully")


with DAG(
    dag_id="training_data_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily", catchup=False,) as dag:

    ingest_task = PythonOperator(task_id="ingest_pubmed",
        python_callable=ingest_pubmed,)

    vector_task = PythonOperator(task_id="update_vectorstore",
        python_callable=update_vectorstore,)

    ingest_task >> vector_task
    
'''


from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def test():
    print("Hello Airflow")

with DAG(
    dag_id="training_data_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,) as dag:

    task = PythonOperator(task_id="test", python_callable=test)  '''