import os

from tests.src.factory.util_factory import TestesFactory
from tests.util.assert_util import AssertUtil
from tests.util.dump_util import DumpUtil
from tests.util.enum_http_method import HTTPMethod
from tests.util.enum_param_mode import ParamMode
from tests.util.requests_util import RequestsUtil
from tests.util.validate_util import ValidateUtil


class TCaseUtil:
    def __init__(self, current_file, mope_code, endpoint, port = 5000):
        """
        Args:
            current_file_path: caminho do arquivo local de teste. Normalmente passado com __file__
        """
        self.current_file = current_file
        self.dump_sql_folder_path = DumpUtil.get_dump_sql_folder_path()
        if current_file is not None:
            self.folder_path = DumpUtil.get_folder_path(current_file)
            self.argvalues = DumpUtil.get_files_from_folder(

                f"{self.folder_path}/entradas_json", True)
        self.url_base = os.getenv("TESTS_URL_BASE", "http://localhost")
        self.tests_tenant = os.getenv("TESTS_TENANT", "11045")
        self.mope_code = mope_code

        self.global_sql = f"{self.dump_sql_folder_path}/global.sql"
        self.tests_tenant = os.getenv("TESTS_TENANT", "100011045")
        self.endpoint = f"{self.url_base}:{port}/{self.mope_code}/{endpoint}"

    def pre_setup(self, json_entrada_nome, executar_globals=True):
        print(f"\nJSON: {json_entrada_nome}", end="\t")
        entrada_sql = f"{self.folder_path}/dump_sql/{json_entrada_nome}"
        csv_folder = f"{self.folder_path}/dump_csv/{json_entrada_nome}"

        params_tenant = {"tenant": self.tests_tenant}
        if executar_globals:
            DumpUtil.dump_from_sqls([self.global_sql], params_tenant)
        DumpUtil.dump_from_sqls([entrada_sql], params_tenant)
        DumpUtil.dump_csvs_from_folder(

            csv_folder, {"tenant": self.tests_tenant})

    def pos_setup(self, json_entrada_nome=None):
        params_tenant = {"tenant": self.tests_tenant}
        DumpUtil.dump_sql_if_exists(
            f"{self.dump_sql_folder_path}/global_after", params_tenant)
        if json_entrada_nome is not None:
            DumpUtil.dump_sql_if_exists(
                f"{self.folder_path}/dump_sql/{json_entrada_nome}_after", params_tenant)

    def common_request_test(self, json_entrada, json_entrada_nome, http_method, param_mode=ParamMode.QUERY):

        body, status_esperado = DumpUtil.load_json_data_and_status_code(
            json_entrada)
        if HTTPMethod.POST == http_method:
            retorno = RequestsUtil.post(self.endpoint, data=body)
        elif HTTPMethod.GET == http_method:
            retorno = RequestsUtil.get(
                self.endpoint, params=body, param_mode=param_mode)
        elif HTTPMethod.DELETE == http_method:
            retorno = RequestsUtil.delete(
                self.endpoint, params=body, param_mode=param_mode)
        elif HTTPMethod.PUT == http_method:
            retorno = RequestsUtil.put(self.endpoint, data=body)
        else:
            retorno = None
        AssertUtil.assert_status_code(retorno, status_esperado)
        content = ''
        if retorno.text.strip() != '':
            content: str = retorno.json()
        saida = DumpUtil.load_json(
            f"{self.folder_path}/saidas_json/{json_entrada_nome}.json")
        ValidateUtil.assert_content(saida, content)

    def validar_banco(self):
        pass
