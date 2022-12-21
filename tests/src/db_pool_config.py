from src.settings import DATABASE_HOST
from src.settings import DATABASE_PASS
from src.settings import DATABASE_PORT
from src.settings import DATABASE_NAME
from src.settings import DATABASE_USER

import sqlalchemy


def create_pool(database_conn_url):
    # Creating database connection pool
    db_pool = sqlalchemy.create_engine(
        database_conn_url,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    )
    return db_pool


database_conn_url = f'postgresql+pg8000://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
db_pool = create_pool(database_conn_url)
