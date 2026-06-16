from ..models import (Document, DocumentType)


from bs4 import BeautifulSoup

import aiohttp


class WebLoader:

    async def _fetch_html(self, url):

        async with aiohttp.ClientSession( headers={"User-Agent": "TrainingDataBot/1.0"}) as session:

            async with session.get(url) as response:

                return await response.text()
            



    def _extract_text(self, html):

        soup = BeautifulSoup(html,"html.parser")

        return soup.get_text(separator=" ", strip=True)


    async def load(self, url):

        html = await self._fetch_html(url)

        text = self._extract_text(html)

        return Document(
            title=url,
            content=text,
            source=url,
            doc_type=DocumentType.WEB,
            word_count=len(text.split()),
            char_count=len(text))