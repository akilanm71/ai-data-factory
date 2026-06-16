
import aiohttp

class DecodoClient:

    def __init__(self):
        self.session = None

    async def initialize(self):

        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def fetch_page(self, url):

        await self.initialize()

        async with self.session.get(url) as response:
            return await response.text()

    async def close(self):

        if self.session:
            await self.session.close()
            self.session = None