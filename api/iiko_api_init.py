import asyncio
import aiohttp
import json
#import pydantic
from iiko_api_methods.methods import IikoTransport



#curent_session = aiohttp.ClientSession()

API_TOKEN = 'ebd53133-dd1'

ORG_ID = '2ccfa2c5-95e7-4a6a-b0be-e96bef2cf7ec'

api = IikoTransport(API_TOKEN, return_dict=True)

async def main():
    response = api.organizations()
    print(response)



# BASE_URL = "https://api-ru.iiko.services"

# auth_url = "/api/1/access_token"

# temp_token = 'Bearer '


# headers = {
#             "Content-Type": "application/json",
#             "Timeout": "15",
#         }


# headers_2 = {"Content-Type": "application/json", 
#              'Authorization': temp_token}
             

# data = {"apiLogin": API_TOKEN}



# async def get_marker(session, url):
#     async with session.post(BASE_URL+url, headers=headers, json=data) as response:

#                 print("Status:", response.status)
#                 #print("Content-type:", response.headers['content-type'])
#                 resp = await response.json()
#                 resp_dict = json.load(resp)
#                 print(resp_dict['token'])


# async def get_response():
#     async with aiohttp.ClientSession() as session:
#            return await session
            # 

        # async with session.post(BASE_URL+'/api/1/loyalty/iiko/program', headers=headers_2, json={'organizationId': org_id}) as response:
        #     print("Status:", response.status)
        #     resp = await response.json()
        #     resp_dict = json.dump(resp)
        #     print(resp_dict)


asyncio.run(main())