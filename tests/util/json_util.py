import decimal
import enum
import json
from datetime import date, datetime
from uuid import UUID

import jsonpickle

from pydantic import BaseModel


class JsonUtil:
    def encode(self, dados: object, __profundidade_permitida=20):
        if isinstance(dados, str):
            return dados
        if dados is None:
            return None
        if not isinstance(dados, dict):
            dados = self.toDict(dados, __profundidade_permitida)
        return json.dumps(dados, indent=True, sort_keys=True, default=self.toDict)

    def decode(self, dados: object):
        if dados is None:
            return None
        if dados == '':
            return None
        return jsonpickle.decode(dados)

    def toDict(self, dados: object, __profundidade_permitida=10):
        """
        Converte um Objeto em um dicionario. Caso seja um tipo primitivo, retorna o proprio argumento recebido
        """
        if __profundidade_permitida <= 0:
            return str(dados)
        if (isinstance(dados, BaseModel)):
            return self.toDict(dados.dict(), __profundidade_permitida)
        if (isinstance(dados, dict)):  # A entrada já foi um dict
            saida = dict()
            for key in dados.keys():
                saida[key] = self.toDict(dados[key], __profundidade_permitida - 1)
            return saida
        if (isinstance(dados, UUID)):
            return str(dados)
        if (isinstance(dados, list)):
            saida = list()
            for elem in dados:
                saida.append(self.toDict(elem, __profundidade_permitida - 1))
            return saida
        if isinstance(dados, enum.Enum):
            return dados.value
        if (isinstance(dados, datetime)):  # Tratamento de datas
            return dados.strftime('%Y-%m-%d %H:%M:%S')
        if (isinstance(dados, date)):  # Tratamento de datas
            return dados.strftime('%Y-%m-%d')
        if isinstance(dados, decimal.Decimal):  # Tratamento de decimal
            return float(dados)
        if (not hasattr(dados, "__dict__")):  # A entrada nao pode ser convertida para dict
            return dados
        else:
            saida = dict()  # A entrada foi um objeto, que deverá ser convertido para dict
            # Para cada atributo...
            dir_dados = dir(dados)
            for atributo in dir_dados:
                if atributo.startswith('__'):
                    continue
                try:
                    if callable(getattr(dados, atributo)):
                        continue
                except:
                    continue
                if atributo.startswith('_'):
                    continue
                atr = getattr(dados, atributo)
                saida[atributo] = self.toDict(atr, __profundidade_permitida - 1)
            return saida

    def encode_soft(self, dados, __profundidade_permitida=10):
        if isinstance(dados, str):
            return dados
        if dados is None:
            return None
        dic = self.toDict(dados, __profundidade_permitida)
        for key in dic.keys():
            dic[key] = str(dic[key])
        return json.dumps(dic)
