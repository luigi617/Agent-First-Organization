

import requests


class StackOverflow():
    @staticmethod
    def api_call(api_url, params):
        api_url = api_url
        params = params
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        api_called = response.request.url
        api_call_output = response.json()
        return api_called, api_call_output