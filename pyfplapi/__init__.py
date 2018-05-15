import asyncio
import logging
from datetime import timedelta, date

import aiohttp
import async_timeout
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)
BASE_URL = "https://app.fpl.com/wps/PA_ESFPortalWeb/getDailyConsumption.do"

class FplApi(object):
    """A class for getting daily kwh usage information from Florida Power & Light."""

    def __init__(
            self, premise_number, account_number, user_type, is_tou, view_type,
            loop, session):
        """Initialize the data retrieval."""
        self._loop = loop
        self._session = session
        self.premise_number = premise_number
        self.account_number = account_number
        self.user_type = user_type
        self.is_tou = is_tou
        self.view_type = view_type
        self.search_series_name = "$" if view_type == 'dollar' else " kWh"
        self.data = None

    async def async_get_usage(self):
        async with async_timeout.timeout(10, loop=self._loop):
            response = await self._session.get(self._get_url())

        _LOGGER.debug("Response from API: %s", response.status)

        if response.status != 200:
            self.data = None
            return

        malformedXML = await response.read()

        cleanerXML = str(malformedXML).replace(
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '', 1
            ).split("<ARG>@@", 1)[0]

        soup = BeautifulSoup(cleanerXML, 'html.parser')

        self.data = soup.find("dataset", seriesname=self.search_series_name) \
            .find("set")['value']


    def _get_url (self):
        end_date = date.today()
        start_date = end_date - timedelta(days=1)

        return ("{base_url}"
               "?premiseNumber={premise_number}"
               "&accountNumber={account_number}"
               "&userType={user_type}"
               "&isTouUser={is_tou}"
               "&viewType={view_type}"
               "&startDate={start_date}"
               "&endDate={end_date}"
               "&isResidential=true"
               "&certifiedDate=2000/01/01"
               "&tempType=max"
               "&ecDayHumType=NoHum"
              ).format(
                base_url=BASE_URL,
                premise_number=self.premise_number,
                account_number=self.account_number,
                user_type=self.user_type,
                is_tou=str(self.is_tou),
                view_type=self.view_type,
                start_date=start_date.strftime("%Y%m%d"),
                end_date=end_date.strftime("%Y%m%d"),
              )
