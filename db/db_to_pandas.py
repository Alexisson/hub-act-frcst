import pandas as pd
import psycopg2
from sqlalchemy import create_engine, exc

from settings import settings


def read_dataframe_from_table(table_name):
    try:
        engine = create_engine(
            f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}',
            connect_args={'options': '-csearch_path={}'.format("s_pg_hub")})
        cnx = engine.connect()
    except exc.SQLAlchemyError as e:
        #print(f"Ошибка подключения: {e}")
        return
    df = pd.read_sql_table(table_name, cnx)
    cnx.close()
    return df


if __name__ == "__main__":
    print(read_dataframe_from_table('resident_loans_volume'))
