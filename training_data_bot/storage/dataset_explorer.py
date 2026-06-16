from collections import Counter


class DatasetExplorer:

    def __init__(self, database_manager):
        
        self.db = database_manager 

    async def count_records(self):

        records = await self.db.load_records()

        return len(records)

    async def get_class_distribution(self):

        records = await self.db.load_records()

        labels = []

        for record in records:

            if "label" in record:

                labels.append(record["label"])

        return dict(Counter(labels))

    async def preview(self,limit=10):

        records = await self.db.load_records()

        return records[:limit]

    async def dataset_summary(self):

        records = await self.db.load_records()

        total_records = len(records)

        class_distribution = (await self.get_class_distribution())

        return { "total_records": total_records, "class_distribution": class_distribution }