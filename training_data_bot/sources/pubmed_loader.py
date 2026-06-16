import requests

import xml.etree.ElementTree as ET

class PubMedLoader:

    def __init__(self):

        self.esearch_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi")

        self.efetch_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi")


    def search(self,query: str , limit= 10):

        params = {"db":"pubmed", "term":query, "retmax":limit, "retmode":"json"}

        response = requests.get(self.esearch_url, params=params)
        print("Status:", response.status_code)
        print("URL:", response.url)
        print("Response:")
        print(response.text[:500])
        print("="*50)

        return (response.json()["esearchresult"]["idlist"])

    def fetch_abstract(self, pmid):

        params = {"db":"pubmed","id":pmid,"rettype":"abstract",
                    "retmode":"text"}

        response = requests.get(self.efetch_url, params=params)

        return response.text
    
    def fetch_metadata(self, pmid):

           params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"}

           response = requests.get(self.efetch_url, params=params)

           root = ET.fromstring(response.text)

           title = root.findtext(".//ArticleTitle", default="")

           authors = []

           for author in root.findall(".//Author"):

                   lastname = author.findtext("LastName", "")
                   firstname = author.findtext("ForeName", "")

           if lastname or firstname:
                   authors.append(f"{firstname} {lastname}")

           journal = root.findtext(".//Journal/Title", default="")

           doi = root.findtext(".//ArticleId[@IdType='doi']", "")

           doi_url = f"https://doi.org/{doi}" if doi else ""

           pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

           return {
        "title": title,
        "authors": authors,
        "journal": journal,
        "doi": doi,
        "doi_url": doi_url,
        "pubmed_url": pubmed_url}