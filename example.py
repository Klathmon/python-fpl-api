import asyncio
import aiohttp

from pyfplapi import FplApi

async def main():
    username = ''
    password = ''
    async with aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(username, password)) as session:
        api = FplApi(True, loop, session)
        await api.login()
        await api.async_get_yesterday_usage()
        await api.async_get_mtd_usage()

        print(api.yesterday_kwh)
        print(api.yesterday_dollars)
        print(api.mtd_kwh)
        print(api.mtd_dollars)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
