import os

from nsj_rest_test_util.util.assert_util import AssertUtil
from nsj_rest_test_util.util.dump_util import DumpUtil
from nsj_rest_test_util.util.enum_http_method import HTTPMethod
from nsj_rest_test_util.util.enum_param_mode import ParamMode
from nsj_rest_test_util.util.requests_util import RequestsUtil
from nsj_rest_test_util.util.validate_util import ValidateUtil


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
        self.token_url = os.getenv('TOKEN_URL','https://auth.dev.nasajonsistemas.com.br/auth/realms/DEV/protocol/openid-connect/token')
        self.token_user = os.getenv('TOKEN_USER')
        self.token_password = os.getenv('TOKEN_PASSWORD')
        self.token_client = os.getenv('TOKEN_CLIENT')
        self.api_key = os.getenv("TESTS_API_KEY")
        self.app_name = os.getenv('APP_NAME')

        self.global_sql = f"{self.dump_sql_folder_path}/global.sql"
        self.endpoint = f"{self.url_base}:{port}/{(self.app_name + '/') if self.app_name else ''}{(mope_code + '/') if mope_code else ''}{endpoint}"

    def pre_setup(self, json_entrada_nome, schema=None, executar_globals=True):
        print(f"\nJSON: {json_entrada_nome}", end="\t")
        entrada_sql = f"{self.folder_path}/dump_sql/{json_entrada_nome}"
        csv_folder = f"{self.folder_path}/dump_csv/{json_entrada_nome}"

        params_tenant = {"tenant": self.tests_tenant}
        if executar_globals:
            DumpUtil.dump_from_sqls([self.global_sql], params_tenant)
        DumpUtil.dump_from_sqls([entrada_sql], params_tenant)
        DumpUtil.dump_csvs_from_folder(

            csv_folder, {"tenant": self.tests_tenant}, schema)

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

        headers = {}
        if self.token_client:
            token_body = {"client_id":self.token_client,"scope":"offline_access","grant_type":"password","username":self.token_user,"password":self.token_password}
            token_retorno = RequestsUtil.postToken(
                self.token_url, data=token_body, headers={'content-type':'application/x-www-form-urlencoded'})
            headers['Authorization'] = token_retorno.json()['access_token']

        if self.api_key:
            headers = {"X-API-Key": self.api_key}

        if HTTPMethod.POST == http_method:
            retorno = RequestsUtil.post(self.endpoint, data=body, headers=headers)
        elif HTTPMethod.GET == http_method:
            retorno = RequestsUtil.get(
                self.endpoint, params=body, param_mode=param_mode, headers=headers)
        elif HTTPMethod.DELETE == http_method:
            retorno = RequestsUtil.delete(
                self.endpoint, params=body, param_mode=param_mode, headers=headers)
        elif HTTPMethod.PUT == http_method:
            retorno = RequestsUtil.put(self.endpoint, data=body, headers=headers)
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
