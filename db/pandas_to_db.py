
from sqlalchemy import create_engine, exc

# Параметры подключения к базе данных
db_username = 'postgres'
db_password = 'test'  # Лучше бы тут это не хранить а положить в env(ближе к деплою разберемся)
db_host = 'test'
db_port = '5432'
db_name = 'postgres'

# Создаем движок SQLAlchemy для подключения к PostgreSQL
engine = create_engine(f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}',
                       connect_args={'options': '-csearch_path={}'.format("s_pg_hub")})


def write_to_db(df, table_name, engine):
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
