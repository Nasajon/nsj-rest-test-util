

import sqlalchemy
        
class Pool:
    def _create_pool(self,database_conn_url):
        # Creating database connection pool
        return sqlalchemy.create_engine(
            database_conn_url,
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,
            pool_recycle=1800
        )
        
    
    def __init__(self, database_user, database_pass, database_host, database_port, database_name ):
        database_conn_url = f'postgresql+pg8000://{database_user}:{database_pass}@{database_host}:{database_port}/{database_name}'
        self.db_pool = self._create_pool(database_conn_url)
        

   
