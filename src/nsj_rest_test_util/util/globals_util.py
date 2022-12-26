import os
from uuid import uuid4

from nsj_rest_test_util.util.json_util import JsonUtil


class GlobalUtil:
    __request = None

    @staticmethod
    def profile_query(datetime_inicio, datetime_fim, sql, parametros, retorno):
        request = GlobalUtil.get_request()
        try:
            request.parametros["tenant"]
        except:
            pass
        if os.getenv("USA_PROFILE", "FALSE").lower() == "true":

            if isinstance(request, RequestMock):
                return

            rastro = {
                "id": uuid4(),
                "tenant": request.parametros["tenant"],
                "id_requisicao": request.parametros["id"],
                "datahora_inicio": datetime_inicio,
                "datahora_fim": datetime_fim,
                "string_sql": sql,
                "parametros": JsonUtil().encode(parametros),
                "qnt_linhas_parametros": len(parametros) if isinstance(parametros, list) else 1,
                "qnt_campos_parametros": JsonUtil().encode(parametros).count(':') if parametros is not None else 0,
                "qnt_linhas_retorno": len(retorno) if retorno is not None else 0
            }
            if not "rastros" in request.parametros:
                request.parametros["rastros"] = []
            request.parametros["rastros"].append(rastro)

    @staticmethod
    def get_request() -> any:
        try:
            from flask import request
            x = request.args

            try:
                y = request.parametros
            except:
                request.parametros = {}

            return request
        except:
            if GlobalUtil.__request is None:
                GlobalUtil.__request = RequestMock()
                GlobalUtil.__request
            return GlobalUtil.__request


class RequestMock:
    parametros = {}
