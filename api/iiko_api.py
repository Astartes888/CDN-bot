import asyncio
import aiohttp
import pydantic


API_TOKEN = '50859c16-293'

BASE_URL = "https://api-ru.iiko.services"

auth_url = "/api/1/access_token"

temp_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcGlMb2dpbklkIjoiMTA1OWVjOGYtZmU4Ni00YTA4LTlhOTUtNWVkMTE5YzQ5NzUwIiwibmJmIjoxNjk1Mzg4Mjk1LCJleHAiOjE2OTUzOTE4OTUsImlhdCI6MTY5NTM4ODI5NSwiaXNzIjoiaWlrbyIsImF1ZCI6ImNsaWVudHMifQ.N2Mwtq7_0eSp-2sEagfeKAd2nI5mjVfZOmcV0wjepVI'

headers = {
            "Content-Type": "application/json",
            "Timeout": "15",
        }

headers_2 = {"Content-Type": "application/json", 
             'Authorization': temp_token}

data = {"apiLogin": API_TOKEN}


async def get_response():
    async with aiohttp.ClientSession() as session:
            # async with session.post(BASE_URL+auth_url, headers=headers, json=data) as response:

            #     print("Status:", response.status)
            #     print("Content-type:", response.headers['content-type'])
            #     html = await response.text()
            #     print(html)



        async with session.post(BASE_URL+'/api/1/organizations', headers=headers) as response:
            print("Status:", response.status)
            resp = await response.text()
            print(resp)



asyncio.run(get_response())