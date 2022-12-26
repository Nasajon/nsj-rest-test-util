import json
import os

import requests

from nsj_rest_test_util.util.enum_param_mode import ParamMode

class RequestsUtil():

    @staticmethod
    def get(url, params: dict = None, headers: dict = {},
            param_mode: ParamMode = ParamMode.QUERY) -> requests.Response:

        if param_mode == ParamMode.PATH:
            for field, value in params.items():
                url = url.replace(f"<{field}>", f"{value}")
            params = {}

        return requests.get(url=url, params=params, headers=headers)

    @staticmethod
    def delete(url, params: dict = None, headers: dict = {},
            param_mode: ParamMode = ParamMode.QUERY) -> requests.Response:

        if param_mode == ParamMode.PATH:
            for field, value in params.items():
                url = url.replace(f"<{field}>", f"{value}")
            params = {}

        return requests.delete(url=url, params=params, headers=headers)

    @staticmethod
    def post(url, data: dict = None, params: dict = None, headers: dict = {}) -> requests.Response:

        retorno = requests.post(
            url=url, json=data, headers=headers, params=params)
        return retorno

    @staticmethod
    def postToken(url, data: dict = None, headers: dict = {}) -> requests.Response:

        retorno = requests.post(
            url=url, data=data, headers=headers)
        return retorno


    @staticmethod
    def put(url, data: dict = None, params: dict = None, headers: dict = {}) -> requests.Response:

        retorno = requests.put(
            url=url, json=data, headers=headers, params=params)
        return retorno
