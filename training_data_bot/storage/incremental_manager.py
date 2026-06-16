import json
from pathlib import Path
from ..core.logging import get_logger

logger = get_logger(__name__)

class IncrementalManager:

    def __init__(self):

        self.state_file = Path("storage/processed_pmids.json")

        if not self.state_file.exists():

            with open(self.state_file, "w") as f:
                
                json.dump([] , f)

    def load_ids(self):

        if not self.state_file.exists():

            return []

        with open(self.state_file, "r") as f:

            return json.load(f)

    def save_id(self, paper_id):

        ids = self.load_ids()

        if paper_id not in ids:

            ids.append(paper_id)

            with open(self.state_file, "w") as f:

                json.dump(ids,f,indent=4)

            logger.info(f"Saved PMID={paper_id}")

    def get_new_pmids(self, pmids):

            processed_ids = set(self.load_ids())

            new_pmids = []

            for pmid in pmids:

                 if pmid not in processed_ids:

                        new_pmids.append(pmid)

            processed_ids.update(new_pmids)

            with open(self.state_file, "w") as f:

                  json.dump(list(processed_ids), f, indent=4)

            return new_pmids