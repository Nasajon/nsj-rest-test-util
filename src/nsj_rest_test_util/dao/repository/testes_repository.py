import os
from nsj_rest_test_util.dao.repository.abstract_repository import AbstractRepository


class TestesRepository(AbstractRepository):

    def __init__(self):
        database_host = os.getenv('DATABASE_HOST')
        database_port = os.getenv('DATABASE_PORT')
        database_user = os.getenv('DATABASE_USER')
        database_name = os.getenv('DATABASE_NAME')
        database_pass = os.getenv('DATABASE_PASS') 
        super().__init__(database_host, database_port, database_name, database_user, database_pass)

