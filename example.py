import sys
import asyncio
import aiohttp

from pyfplapi import FplApi

async def main():
    username = sys.argv[-2]
    password = sys.argv[-1]
    session = aiohttp.ClientSession()
    api = FplApi(username, password, True, loop, session)
    await api.login()
    await api.async_get_yesterday_usage()
    await api.async_get_mtd_usage()
    await session.close()

    print(api.yesterday_kwh)
    print(api.yesterday_dollars)
    print(api.mtd_kwh)
    print(api.mtd_dollars)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
