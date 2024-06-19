import pandas as pd
import psycopg2

# Параметры подключения к базе данных
db_username = 'postgres'
db_password = 'test'  # Лучше бы тут это не хранить а положить в env(ближе к деплою разберемся)
db_host = 'test'
db_port = '5432'
db_name = 'test'

conn_string = f"dbname='{db_name}' user='{db_username}' password='{db_password}' host='{db_host}' port='{db_port}'"

conn = psycopg2.connect(conn_string)

query = "SELECT * FROM test_table;"


df = pd.read_sql_query(query, conn)


conn.close()


print(df)