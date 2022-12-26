import os
from pathlib import Path

from write import write

from nsj_rest_test_util.util.json_util import JsonUtil
from nsj_rest_test_util.util import backup_util
from nsj_rest_test_util.util.enum_http_method import HTTPMethod
from nsj_rest_test_util.util.requests_util import RequestsUtil
from nsj_rest_test_util.util.tcase_util import TCaseUtil


def delete_all_files_in_folder(folder: Path):
    for file in folder.iterdir():
        file.unlink()


class TCaseTools:
    @staticmethod
    def criar_caso_teste_padrao(tenant, endpoint: str, mope_code: str, http_method: HTTPMethod,
                                status_http_esperado: int, nome_caso_teste: str, 
                                dict_entrada_ou_parametros_get, executar_e_gerar_saida: bool,
                                sobrescrever_artefatos: bool = False, sobrescrever_script: bool = False,
                                utilizar_sql_global: bool = False):
        os.environ["TESTS_TENANT"] = str(tenant)
        port = os.getenv('SERVER_PORT', 5000)
        nome_arq = f"{nome_caso_teste}_{status_http_esperado}"
        nome_arq_script = f"_{http_method.name.lower()}"
        pasta_atual = __file__
        pasta_atual = Path(pasta_atual)
        pasta_util = pasta_atual.parent
        pasta_testes = pasta_util.parent
        pasta_api = Path(str(pasta_testes) + "/api")
        pasta_casos = Path(str(pasta_api) + "/casos_de_teste")
        _endpoint = endpoint
        if _endpoint[0] == '/':
            _endpoint = _endpoint[1:]
        sub_endpoints = _endpoint.split('/')
        pasta_endpoint = pasta_casos
        for sub in sub_endpoints:
            pasta_endpoint = Path(str(pasta_endpoint) + f"/{sub}")
            pasta_endpoint.mkdir(exist_ok=True)
        pasta_verbo = Path(str(pasta_endpoint) + f"/{http_method.value.lower()}")
        pasta_verbo.mkdir(exist_ok=True)
        pasta_csv_geral = Path(str(pasta_verbo) + "/dump_csv")
        pasta_csv = Path(str(pasta_csv_geral) + f"/{nome_arq}")
        pasta_sql = Path(str(pasta_verbo) + "/dump_sql")
        pasta_entradas = Path(str(pasta_verbo) + "/entradas_json")
        pasta_saidas = Path(str(pasta_verbo) + "/saidas_json")
        pasta_csv_geral.mkdir(exist_ok=True)
        pasta_csv.mkdir(exist_ok=True)
        pasta_sql.mkdir(exist_ok=True)
        pasta_entradas.mkdir(exist_ok=True)
        pasta_saidas.mkdir(exist_ok=True)
        script = Path(str(pasta_verbo) + f"/test_{sub.lower().replace('-', '_')}_{http_method.name.lower()}.py")

        arq_entrada = Path(str(pasta_entradas) + f"/{nome_arq}.json")
        arq_saida = Path(str(pasta_saidas) + f"/{nome_arq}.json")

        if arq_entrada.exists() and not sobrescrever_artefatos:
            return

        print("Criando arquivo de entrada")
        if arq_entrada.exists():
            arq_entrada.unlink()
        if arq_saida.exists():
            arq_saida.unlink()
        write(arq_entrada, JsonUtil().encode(dict_entrada_ou_parametros_get))

        print("Criando Dump em CSV")
        if pasta_csv.exists():
            delete_all_files_in_folder(pasta_csv)

        backup_util.BackupUtil.backup_database_to_csv(str(pasta_csv), tenant)


        print("#Criar script de teste")
        script_template = Path(str(pasta_util) + "/resources/caso_teste_template.py.template")
        with open(script_template, "r") as f:
            template = f.read()
        template = template.replace("<sub_endpoint>", "".join(map(str.capitalize, sub.split("-"))))
        template = template.replace("<endpoint>", endpoint)
        template = template.replace("<http_method>", http_method.value)
        template = template.replace("<method_lower>", http_method.value.lower())
        template = template.replace("<mope_code>", mope_code)
        template = template.replace("<use_global_sql_file>", str(utilizar_sql_global))
        if script.exists():
            if sobrescrever_script:
                script.unlink()
                write(str(script), template)
        else:
            write(str(script), template)
        
        # Gerar SQLs que limpam o banco
        if not utilizar_sql_global:
            texto_sql = ""
            for arquivo in pasta_csv.iterdir():
                nome = arquivo.name.replace(".csv", "")
                texto_sql += f" \r\ndelete from {nome} where tenant=:tenant;";
            arquivo_sql = Path(str(pasta_sql) + f"/{nome_arq}.sql")
            arquivo_sql_after = Path(str(pasta_sql) + f"/{nome_arq}_after.sql")
            write(str(arquivo_sql), texto_sql)
            write(str(arquivo_sql_after), texto_sql)
            

        if executar_e_gerar_saida:
            test_util = TCaseUtil(None, mope_code, endpoint, port)
            if HTTPMethod.POST == http_method:
                saida = RequestsUtil.post(test_util.endpoint, data=dict_entrada_ou_parametros_get)
            elif HTTPMethod.GET == http_method:
                saida = RequestsUtil.get(test_util.endpoint, params=dict_entrada_ou_parametros_get)
            elif HTTPMethod.PUT == http_method:
                saida = RequestsUtil.put(test_util.endpoint, data=dict_entrada_ou_parametros_get)
            elif HTTPMethod.DELETE == http_method:
                saida = RequestsUtil.delete(test_util.endpoint, params=dict_entrada_ou_parametros_get)

            print(saida.content)
            write(str(arq_saida), saida.content)


if __name__ == '__main__':
    TCaseTools.criar_caso_teste_padrao(
        1,
        "recursos/c54cca2c-1468-4eb1-88a0-b16d891985bb",
        "1234",
        HTTPMethod.DELETE,
        204,
        "exemplo1",
        JsonUtil().decode(""""""),
        True,
        True
    )