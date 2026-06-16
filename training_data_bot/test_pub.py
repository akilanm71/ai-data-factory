'''import requests

url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

params = {
    "db": "pubmed",
    "term": "lung cancer",
    "retmode": "json"
}

r = requests.get(url, params=params)

print(r.url)
print(r.status_code)
print(r.text[:500])'''

from training_data_bot.services.pubmed_service import PubMedService

service = PubMedService()

docs = service.ingest_papers(
    query="lung cancer",
    limit=2
)

print(f"Docs found: {len(docs)}")