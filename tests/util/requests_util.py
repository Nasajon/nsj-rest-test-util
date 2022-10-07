import os

import requests

from tests.util.enum_param_mode import ParamMode

api_key = os.getenv("TESTS_API_KEY", "")
content_type = 'application/json'


class RequestsUtil():

    @staticmethod
    def get_headers_with_api_key(headers):
        if headers:
            headers["X-API-Key"] = headers["X-API-Key"] if headers["X-API-Key"] else api_key
        else:
            headers = {"X-API-Key": api_key}
        return headers

    @staticmethod
    def get(url, data=None, params: dict = None, headers: dict = None,
            param_mode: ParamMode = ParamMode.QUERY) -> requests.Response:

        headers = RequestsUtil.get_headers_with_api_key(headers)
        headers['content-type'] = 'application/json'

        if param_mode == ParamMode.PATH:
            for field, value in params.items():
                url = url.replace(f"<{field}>", f"{value}")
            params = {}

        return requests.get(url=url, json=data,
                            params=params, headers=headers)

    @staticmethod
    def delete(url, data=None, params: dict = None, headers: dict = None,
            param_mode: ParamMode = ParamMode.QUERY) -> requests.Response:

        headers = RequestsUtil.get_headers_with_api_key(headers)
        headers['content-type'] = 'application/json'

        if param_mode == ParamMode.PATH:
            for field, value in params.items():
                url = url.replace(f"<{field}>", f"{value}")
            params = {}

        return requests.delete(url=url, json=data,
                            params=params, headers=headers)

    @staticmethod
    def post(url, data: dict = None, params: dict = None, headers: dict = None) -> requests.Response:

        headers = RequestsUtil.get_headers_with_api_key(headers)
        headers['content-type'] = 'application/json'

        retorno = requests.post(
            url=url, json=data, headers=headers, params=params)
        return retorno


    @staticmethod
    def put(url, data: dict = None, params: dict = None, headers: dict = None) -> requests.Response:

        headers = RequestsUtil.get_headers_with_api_key(headers)
        headers['content-type'] = 'application/json'

        retorno = requests.put(
            url=url, json=data, headers=headers, params=params)
        return retorno
