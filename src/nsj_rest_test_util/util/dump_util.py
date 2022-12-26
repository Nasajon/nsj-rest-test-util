import csv
from datetime import datetime
import json
import pathlib
from typing import List, Tuple, Union

from nsj_rest_test_util.dao.factory.util_factory import TestesFactory


class DumpUtil():

    @staticmethod
    def dump_from_sqls(files_paths: List[str], params: Union[List[dict], dict]):
        if isinstance(params, dict):
            params = [params for _ in range(len(files_paths))]

        for file_path, file_params in zip(files_paths, params):
            DumpUtil.dump_sql_if_exists(file_path, file_params)

    @staticmethod
    def dump_csvs_from_folder(folder_path: str, params: Union[List[dict], dict], schema: str):

        files = DumpUtil.get_files_from_folder(folder_path)

        if isinstance(params, dict):
            params = [params for _ in range(len(files))]

        for file_path, file_params in zip(files, params):
            file_name = DumpUtil.get_file_name(file_path)
            DumpUtil.dump_csv_if_exists(
                file_path, table=file_name, schema=schema, params=file_params)

    @staticmethod
    def dump_sql_command(sql_command: str, params: dict):
        repository = TestesFactory.getTestesRepository()
        response = repository.execute(sql_command, params)
        return response

    @staticmethod
    def fetchAll(sql_command: str, params: dict):
        repository = TestesFactory.getTestesRepository()
        response = repository.fetchAll(sql_command, params)
        return response

    @staticmethod
    def fetchOne(sql_command: str, params: dict):
        repository = TestesFactory.getTestesRepository()
        response = repository.fetchOne(sql_command, params)
        return response

    @staticmethod
    def select_from(table: str, 
                    where: Union[str, List[str]] = "", 
                    fields: Union[str, List[str]] = "*",
                    group_by: Union[str, List[str]] = "",
                    having: Union[str, List[str]] = "",
                    fetchOne: bool = False) -> List:

        if fields and isinstance(fields, list):
            fields = ", ".join([field for field in fields])
        
        if where:
            if isinstance(where, list):
                where = "WHERE " + " and ".join(where)
            elif isinstance(where, str):
                where = "WHERE " + where
        
        if group_by:
            if isinstance(group_by, list):
                group_by = "GROUP BY " + ", ".join([field for field in group_by])
            elif isinstance(group_by, str):
                group_by = f"GROUP BY {group_by}"

        if having:
            if isinstance(having, list):
                having = "HAVING " + " and ".join(having)
            elif isinstance(having, str):
                having = "HAVING " + having

        sql_command = f"SELECT {fields} FROM {table} {where} {group_by} {having};"

        repository = TestesFactory.getTestesRepository()

        if fetchOne:
            return repository.fetchOne(sql_command, {})
        return repository.fetchAll(sql_command, {})

    @staticmethod
    def count_rows(table: str, field: str = "*", where: Union[str, List[str]] = "") -> int:

        select = f"COUNT({field}) as n_rows"

        res = DumpUtil.select_from(table, where=where, fields=select, fetchOne=True)

        return res["n_rows"]

    @staticmethod
    def dump_from_sql(file_path: str, params: dict = {}):

        with open(file_path, "r", encoding='utf8') as sql_file:
            sql_command = sql_file.read().split(';')
            for command in sql_command:
                if command != '':
                    DumpUtil.dump_sql_command(command, params)

    @staticmethod
    def dump_from_csv(file_path: str, schema: str, table: str, params: dict = {}, delimiter: str = ','):

        with open(file_path, 'r', encoding='utf8') as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter=delimiter)

            columns = csv_reader.fieldnames

            table_columns = (', ').join(columns)
            table_values = (', ').join([f":{col}" for col in columns])

            sql_command = f"INSERT INTO {((schema + '.') if schema else '' ) + table} ({table_columns}) VALUES ({table_values});"

            def return_none_if_empty_string(
                x): return None if x == "" or x == None else x

            values = [{key: params[key] if key in params else return_none_if_empty_string(val) for key, val in row.items()}
                      for row in csv_reader]

            repository = TestesFactory.getTestesRepository()
            repository.execute_many(sql_command, values)

    @staticmethod
    def dump_sql_if_exists(file_path, params: dict = {}):
        file_path = file_path if file_path[-4:
                                           ] == ".sql" else f"{file_path}.sql"

        if pathlib.Path(file_path).is_file():
            DumpUtil.dump_from_sql(file_path, params)

    @staticmethod
    def dump_csv_if_exists(file_path: str, schema: str, table: str, params: dict = {}):
        file_path = file_path if file_path[-4:
                                           ] == ".csv" else f"{file_path}.csv"
        if pathlib.Path(f"{file_path}").is_file():
            DumpUtil.dump_from_csv(file_path, schema, table, params)

    @staticmethod
    def load_json(file_path: str) -> dict:
        try:
            with open(file_path, encoding='utf8') as json_file:
                return json.load(json_file)
        except: # arquivo vazio ou json incorreto
            return ''

    @staticmethod
    def write_json(file_path: str, data: dict):
        folder = DumpUtil.get_folder_path(file_path)
        # pathlib.Path(folder).mkdir(parents=False, exist_ok=True)
        DumpUtil.mkdir(folder, False, True)
        with open(file_path, 'w', encoding='utf8') as json_file:
            json_file.write(json.dumps(data, indent=2))

    @staticmethod
    def read_file_to_list(file_path: str) -> List:
        itens = []
        with open(file_path, "r", encoding='utf8') as file:
            for line in file:
                itens.append(line.strip())
        return itens

    @staticmethod
    def write_list_to_file(file_path: str, content_list: List):
        with open(file_path, "w", encoding='utf8') as file:
            for item in content_list:
                file.write(f"{item}\n")

    @staticmethod
    def mkdir(folder_path: str, parents: bool = False, exist_ok: bool = True):
        pathlib.Path(folder_path).mkdir(parents=parents, exist_ok=exist_ok)

    @staticmethod
    def load_json_data_and_status_code(file_path: str) -> Tuple[dict, int]:
        expected_status = int(DumpUtil.get_file_name(file_path).split("_")[-1])
        data = DumpUtil.load_json(file_path)
        return data, expected_status

    @staticmethod
    def get_status_code_from_file_path(file_path):
        return int(DumpUtil.get_file_name(file_path).split("_")[-1])

    @staticmethod
    def is_file(file_path: str):
        return pathlib.Path(file_path).is_file()

    @staticmethod
    def copy_file(source_file_path: str, dest_file_path: str):
        with open(source_file_path, "r", encoding='utf8') as source_file, open(dest_file_path, "w", encoding='utf8') as dest_file:
            for line in source_file:
                dest_file.write(line)

    @staticmethod
    def get_file_name(file_path: str) -> str:
        return str(pathlib.Path(file_path).stem)

    @staticmethod
    def get_file_name_with_extension(file_path: str) -> str:
        return str(pathlib.Path(file_path).name)

    @staticmethod
    def get_folder_path(file_path: str) -> str:
        return str(pathlib.Path(file_path).parent.resolve())

    @staticmethod
    def get_workspace_path() -> str:
        return str(pathlib.Path().resolve())

    @staticmethod
    def get_tests_folder_path() -> str:
        return str(pathlib.Path(DumpUtil.get_workspace_path(), "tests/api/casos_de_teste"))

    @staticmethod
    def get_dump_sql_folder_path() -> str:
        return str(pathlib.Path(DumpUtil.get_tests_folder_path(), "dump_sql"))

    @staticmethod
    def get_files_from_folder(folder_path: str, return_name: bool = False) -> Union[List, List[Tuple[str, str]]]:

        if pathlib.Path(folder_path).exists():
            files = pathlib.Path(f"{folder_path}").iterdir()

            if not return_name:
                return list(map(str, files))

            return [(DumpUtil.get_file_name(file_path), str(file_path)) for file_path in files]
        else:
            return []