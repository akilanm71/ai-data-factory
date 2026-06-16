import pandas as pd
from pathlib import Path
from ..models import (Document, DocumentType)


class CSVLoader:

    async def load(self, source):

        df = pd.read_csv(source, nrows =10)

        content = df.to_csv(index=False)

        return Document(
            title=Path(source).stem,
            content=content,
            source=source,
            doc_type=DocumentType.CSV,
            word_count=len(content.split()),
            char_count=len(content))