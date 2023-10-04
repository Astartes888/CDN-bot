import asyncio
import aiohttp
import json
#import pydantic
from iiko_api_methods.methods import IikoTransport



#current_session = aiohttp.ClientSession()

API_TOKEN = 'ebd53133-dd1'

ORG_ID = '2ccfa2c5-95e7-4a6a-b0be-e96bef2cf7ec'


async def test():
    async with aiohttp.ClientSession() as current_session:
        api = IikoTransport(API_TOKEN, session=current_session, return_dict=True)
        response = await api.organizations()
        print(response)
        print(len(asyncio.all_tasks()))



asyncio.run(test())