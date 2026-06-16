
import json

import pandas as pd



from pathlib import Path

class DatabaseManager:

    def __init__(self, db_path="storage/dataset.db"):
        
        self.db_path = db_path
        
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        Path(self.db_path).touch(exist_ok=True)
       

    async def save_record(self, record):

        with open(self.db_path,"a") as f:

            f.write(json.dumps(record))

            f.write("\n")

    async def save_many(self, records):
            
            for record in records:

                 await self.save_record(record)

    async def load_records(self):
             
            records = []

            with open(self.db_path,"r") as f:

                for line in f:

                       records.append(json.loads(line))

            return records

    async def delete_record(self, record_id):

             records = await self.load_records()

             filtered = [r for r in records if r.get("id") != record_id]

             with open(self.db_path, "w") as f:

                    for record in filtered:

                          f.write(json.dumps(record))
                          f.write("\n")

    async def export_csv(self, output_file):
            
                records = await self.load_records()

                df = pd.DataFrame(records)

                df.to_csv(output_file, index=False)

    async def export_json(self, output_file):
                
                records = await self.load_records()

                with open( output_file, "w") as f:

                       json.dump(records, f, indent=4)

       
   