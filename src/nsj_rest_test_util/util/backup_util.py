import csv
import json
import os
import pathlib
from typing import List

import requests

from nsj_rest_test_util.dao.repository.testes_repository import TestesRepository
from nsj_rest_test_util.dao.factory.util_factory import TestesFactory
from nsj_rest_test_util.util.dump_util import DumpUtil

url_base = os.getenv("TESTS_URL_BASE", "http://localhost")
tests_tenant = os.getenv("TESTS_TENANT", "11045")

folder_path = DumpUtil.get_folder_path(__file__)


class BackupUtil:

    @staticmethod
    def backup_table_to_csv(dest_file_path: str, table: str, tenant: int,
                            repository: TestesRepository = TestesFactory.getTestesRepository()):

        sql = f"SELECT * FROM {table} where tenant={tenant}"

        rows = repository.fetchAll(sql, {})
        for row in rows:
            if "tenant" in row.keys():
                row["tenant"] = ":tenant"
        if not rows:
            return

        fieldnames = rows[0].keys()

        with open(dest_file_path, "w", newline="", encoding='utf8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    @staticmethod
    def backup_tables_to_csv(dest_folder_path: str, tenant: int, tables: List = []):

        DumpUtil.mkdir(dest_folder_path, parents=True)

        if not tables:
            return

        repository = TestesFactory.getTestesRepository()

        for table in tables:
            if table not in ['django_migrations', 'usuarios', 'registros_requisicoes', 'rastros']:
                BackupUtil.backup_table_to_csv(
                    f"{dest_folder_path}/{table}.csv", table, tenant, repository)

    # TODO Aplicar recurso para qualquer
    @staticmethod
    def backup_database_to_csv(dest_folder_path: str, tenant: int):
        repository = TestesFactory.getTestesRepository() 
        response = repository.fetchAll("select tablename from pg_catalog.pg_tables where schemaname = 'public';", {})


        ignore_tables = ["vw_timeserver", "registros_requisicoes"]

        tables = [val['tablename']for val in response  if val["tablename"] not in ignore_tables]

        BackupUtil.backup_tables_to_csv(dest_folder_path, tenant, tables)

    @staticmethod
    def get_csvs_changes(csv_a_path: str, csv_b_path: str, csv_c_path: str):

        csv_a_rows = DumpUtil.read_file_to_list(csv_a_path)
        csv_b_rows = DumpUtil.read_file_to_list(csv_b_path)

        fieldnames = csv_a_rows[0]

        csv_a_rows = csv_a_rows[1:]
        csv_b_rows = csv_b_rows[1:]

        csv_c_rows = [row for row in csv_a_rows if row not in csv_b_rows]
        csv_c_rows.insert(0, fieldnames)

        if len(csv_c_rows) > 1:
            DumpUtil.write_list_to_file(csv_c_path, csv_c_rows)

    @staticmethod
    def get_csvs_changes_from_folder(folder_a_path: str, folder_b_path: str, folder_c_path: str):

        DumpUtil.mkdir(folder_c_path, parents=True)

        files_a_paths = DumpUtil.get_files_from_folder(folder_a_path)

        for csv_a_path in files_a_paths:
            csv_a_name = DumpUtil.get_file_name_with_extension(csv_a_path)

            csv_b_path = f"{folder_b_path}/{csv_a_name}"
            csv_c_path = f"{folder_c_path}/{csv_a_name}"

            if not DumpUtil.is_file(csv_b_path):
                DumpUtil.copy_file(csv_a_path, csv_c_path)

            else:
                BackupUtil.get_csvs_changes(csv_a_path, csv_b_path, csv_c_path)

    @staticmethod
    def delete_backup(backup_folder: str):
        files = DumpUtil.get_files_from_folder(backup_folder)

        for file_path in files:
            pathlib.Path(file_path).unlink()

        pathlib.Path(backup_folder).rmdir()

if __name__ == "__main__":
    # BackupUtil.backup_database_to_csv("/backup/antes")
    BackupUtil.backup_database_to_csv("/backup/depois", 1011045)
    BackupUtil.get_csvs_changes_from_folder(
        "/backup/depois",
        "/backup/antes",
        "/backup/alteracoes")