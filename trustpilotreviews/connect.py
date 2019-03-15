import aiohttp
import asyncio

class GetResponse:
    def __init__(self, url):
        self.url = url

    async def fetch(self, session, params):
        async with session.get(self.url, params=params) as response:
            return await response.json()

    async def get_data(self, params):
        async with aiohttp.ClientSession() as session:
            resp = await self.fetch(session, params=params)
            print(resp)

    def run(self, params):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.get_data(params))

    
url = 'https://www.trustpilot.com/businessunit/search'
params = {'country': 'dk', 'query': 'mate.bike'}

get_reponse = GetResponse(url)
get_reponse.run(params)
