import asyncio
import aiohttp
import json
from iiko_api_methods.methods import IikoTransport


#current_session = aiohttp.ClientSession()


# ORG_ID = '2ccfa2c5-95e7-4a6a-b0be-e96bef2cf7ec'

# TEST_USER_ID = 'f8990000-6beb-ac1f-b4eb-08dbc570bbfd'
# TEST_WALLET_ID = 'f8990000-6beb-ac1f-c543-08dbc619fc54'

# async def test():
    #async with aiohttp.ClientSession() as current_session:
    # api = IikoTransport(API_TOKEN)
        #response = await api.organizations()
        #id_org = response['organizations'][0]['id']
    #id_customer = await api.customer_create_or_update(organization_id=ORG_ID, phone='79991234567', name='test')
    #wallet_test = await api.refill_balance(organization_id=ORG_ID, customer_id=TEST_USER_ID, wallet_id=TEST_WALLET_ID, sum=500)
    #wallet_test_2 = await api.withdraw_balance(organization_id=ORG_ID, customer_id=TEST_USER_ID, wallet_id=TEST_WALLET_ID, sum=1000)
    #user_info = await api.customer_info(organization_id=ORG_ID, type='id', identifier=TEST_USER_ID)
    #print(int(user_info.wallet_balances[0].balance))
    #print(user_info.wallet_balances[0].id)
    #print(id_customer.id)   
        #print(len(asyncio.all_tasks()))


#asyncio.run(test())