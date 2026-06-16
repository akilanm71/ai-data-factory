from pathlib import Path
from typing import Tuple

from ..models import Dataset


class DatasetExporter:

    def split_dataset(self, dataset: Dataset, train_ratio: float = 0.8) -> Tuple[Dataset, Dataset]:

        split_index = int(len(dataset.items) * train_ratio)

        train_items = dataset.items[:split_index]

        test_items = dataset.items[split_index:]

        train_dataset = Dataset(name=f"{dataset.name}_train",items=train_items)

        test_dataset = Dataset(name=f"{dataset.name}_test", items=test_items)

        return train_dataset, test_dataset

    async def export(self, dataset: Dataset, output_path: Path, format):

        output_path.parent.mkdir( parents=True, exist_ok=True)

        if format.value == "jsonl":

            with open(output_path, "w", encoding="utf-8") as f:

                for item in dataset.items:

                    f.write(item.model_dump_json()+ "\n")

        return output_path