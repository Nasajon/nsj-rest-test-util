import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from nsj_rest_test_util.dao.db_pool_config import db_pool
from nsj_rest_test_util.util.cursor_util import CursorUtil
from nsj_rest_test_util.util.globals_util import GlobalUtil
from nsj_rest_test_util.util.json_util import JsonUtil
from nsj_rest_test_util.dao.exception.repetir_exception import RepetirException

from sqlalchemy.engine.base import Connection


class AbstractRepository:
    def __init__(self):
        inicio = datetime.now()

        request = GlobalUtil.get_request()
        if "connection" in request.parametros:
            self.__con = request.parametros["connection"]
        else:

            self.__con: Connection = db_pool.connect()
            self.__transaction = None
            request.parametros["connection"] = self.__con
        GlobalUtil.profile_query(inicio, datetime.now(), "<construtor>", {}, [])

    def set_connection(self, connection: str):
        inicio = datetime.now()
        self.__con = db_pool.connect()
        GlobalUtil.profile_query(inicio, datetime.now(), "<set_connection>", {}, [])

    def begin(self):
        inicio = datetime.now()

        if self.__transaction is None:
            self.__transaction = self.__con.begin()

        GlobalUtil.profile_query(inicio, datetime.now(), "<begin>", {}, [])
        return

    def commit(self):
        inicio = datetime.now()
        if self.__transaction is not None:
            self.__transaction.commit()
            self.__transaction = None

        GlobalUtil.profile_query(inicio, datetime.now(), "<commit>", {}, [])

    def em_transacao(self):
        if self.__transaction is None:
            transacao = False 
            return transacao

        try:
            transacao = self.__transaction.is_active
            return transacao.is_active
        except:
            transacao = False
            return transacao

    def rollback(self):
        inicio = datetime.now()

        if self._transaction is not None:
            self._transaction.rollback()
            self._transaction = None

        GlobalUtil.profile_query(inicio, datetime.now(), "<rollback>", {}, [])

    def execute_many(self, sql, params : List[Dict]):
        from sqlparams import SQLParams

        if len(params) == 0:
            raise Exception("NENHUMA LINHA A INSERIR")

        parametros_execucao = []

        for i in range(len(params)):
            parametro = params[i]

            sql2, params2 = SQLParams(
                'named', 'format').format(sql, parametro)

            parametros_execucao.append(tuple(self.trata_parametros_v2(params2)))

        try:
            for parametro in parametros_execucao:
                cursor = self.__con.execute(sql2, parametro)
        except Exception as e:
            print(e)
            print(sql2)
            print(params2)
            try:
                print(sql % tuple(params2))
            except:
                pass
            raise
        return cursor

    def execute(self, sql: str, params: dict):
        inicio = datetime.now()
        try:
            cursor = None

            cursor = self.__execute_retornando_cursor(sql, params)
            
        finally:
            if cursor != None:
                cursor.close()
        GlobalUtil.profile_query(inicio, datetime.now(), sql, params, [])

    def fetchAll(self, sql: str, params: dict) -> List[dict]:
        inicio = datetime.now()
        try:
            cursor = None
            try:
                cursor = self.__execute_retornando_cursor(sql, params)
                
            except Exception as err:
                raise

            retorno = []
            fetch  = CursorUtil().fetchall(cursor)
            
        finally:
            if cursor != None:
                cursor.close()
        GlobalUtil.profile_query(inicio, datetime.now(), sql, params, retorno)
        return fetch

    def fetchOne(self, sql: str, params: dict) -> Optional[dict]:
        inicio = datetime.now()
        try:
            cursor = None
            try:
                cursor = self.__execute_retornando_cursor(sql, params)
            except Exception as err:
                raise RepetirException(err)
            retorno = CursorUtil().fetchone(cursor)
        finally:
            if cursor != None:
                cursor.close()
        GlobalUtil.profile_query(inicio, datetime.now(), sql, params, retorno)
        return retorno

    def trata_parametro(self, elem):
        if isinstance(elem, Enum):
            return elem.value
        elif isinstance(elem, UUID):
            return str(elem)

        elif isinstance(elem, str):
            try:
                return datetime.strptime(elem, '%Y-%m-%d').date()
            except:
                try:
                    return datetime.strptime(elem, '%Y-%m-%dT%H:%M:%S')
                except:
                    try:
                        return datetime.strptime(elem, '%Y-%m-%dT%H:%M:%S')
                    except:
                        return elem
        elif isinstance(elem, list):
            if len(elem) == 0:
                raise Exception("Lista de parâmetros vazia")
            return tuple([self.trata_parametro(e) for e in elem])
        else:
            return elem

    def trata_parametros_v2(self, params):
        saida = params
        for i in range(len(params)):
            if isinstance(saida[i], Enum):
                saida[i] = saida[i].value
            elif isinstance(saida[i], UUID):
                saida[i] = str(saida[i])
            elif isinstance(saida[i], list):
                if len(saida[i]) == 0:
                    raise Exception("Lista de parâmetros vazia")
                saida[i] = tuple(self.trata_parametro(saida[i]))
        return params

    def __execute_retornando_cursor(self, sql: str, params: dict):
        from sqlparams import SQLParams
        if not isinstance(params, dict):
            params = params.__dict__

        try:
            sql2, params2 = SQLParams('named', 'format').format(sql, params)
            param3 = [self.trata_parametro(elem) for elem in params2]

            cursor = self.__con.execute(sql2, param3)

        except Exception as e:
            print(e)
            print(sql)
            print(params)
            try:
                print(sql % tuple(param3))
            except:
                pass
            raise
        return cursor


if __name__ == '__main__':
    sql = """
    
    """
    repositorio = AbstractRepository()
    repositorio.fetchAll()
