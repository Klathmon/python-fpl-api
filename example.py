import asyncio
import aiohttp

from pyfplapi import FplApi

async def main():
    premise_number = ''
    account_number = ''
    user_type = 'EXT'
    is_tou = False
    view_type = 'kwh'
    async with aiohttp.ClientSession() as session:
        api = FplApi(
            premise_number, account_number, user_type, is_tou,
            view_type, loop, session)
        await api.async_get_usage()

        print(api.data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
