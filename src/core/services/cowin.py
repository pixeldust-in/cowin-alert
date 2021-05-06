import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class CowinApi:
    api_endpoint = settings.COWIN_API_URL

    @classmethod
    def search_by_pincode(cls, pincode, date=None):
        "date: DD-MM-YYYY"
        try:
            payload = {}
            headers = {}
            url = f"{cls.api_endpoint}?pincode={pincode}&date={date}"
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code != 200:
                logger.exception(
                    f"""
                    COWIN API Status code {response.status_code} recieved!
                    response: {response.text}
                    pincode: {pincode}
                """
                )
            return response
        except requests.exceptions.Timeout as e:
            logger.exception("COWIN API Timeout error, %s", e)
        except requests.exceptions.RequestException as e:
            logger.exception("COWIN API error, %s", e)
