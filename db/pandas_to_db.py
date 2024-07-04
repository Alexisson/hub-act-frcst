from sqlalchemy import create_engine, exc
from settings import settings


# Создаем движок SQLAlchemy для подключения к PostgreSQL


def write_to_db(df, table_name):
    try:
        engine = create_engine(
            f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}',
            connect_args={'options': '-csearch_path={}'.format("s_pg_hub")})
    except exc.SQLAlchemyError as e:
        print(f"Ошибка подключения: {e}")
        return
    try:

        # Попытка записать данные в существующую таблицу
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f'Данные добавлены в существующую таблицу {table_name}.')
    except exc.SQLAlchemyError as e:
        if 'does not exist' in str(e):
            # Если таблицы не существует, создаем ее и записываем данные
            df.to_sql(table_name, engine, if_exists='fail', index=False)
            print(f'Таблица {table_name} создана и данные добавлены.')
        else:
            # Другие ошибки SQL
            print(f'Ошибка SQL: {e}')
