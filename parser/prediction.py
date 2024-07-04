import os
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

from data_transform.calculate_avg import get_average_coefficient, approximate_df_from_year_to_monthly
from data_transform.transform_df import transform_df_to_format
from db.pandas_to_db import write_to_db
from parser.cb_xlsx import get_soup
from parser.cfg import FOLDER

if not Path(FOLDER).is_dir():
    Path(FOLDER).mkdir(parents=True)
if not Path(os.path.join(FOLDER, "prediction")).is_dir():
    Path(os.path.join(FOLDER, "prediction")).mkdir(parents=True)

url_for_parse = "https://cbr.ru/about_br/publ/ondkp/on_2024_2026/"


def replace_with_average(value):
    if isinstance(value, str):
        # Замена тире на дефис и запятых на точки
        value = value.replace('—', '-').replace(',', '.')
        if '-' in value:
            numbers = value.split('-')
            try:
                # Преобразование строк в числа с плавающей точкой
                numbers = [float(num) for num in numbers]
                # Возвращаем среднее значение
                return float(sum(numbers) / len(numbers))
            except ValueError:
                # В случае ошибки преобразования возвращаем исходное значение
                return value
        else:
            return value
    else:
        return value


# Применение функции ко всем ячейкам DataFrame


def get_inflation_predict_data():
    # Parse the HTML content

    # Find the table with the class 'data levels'
    soup = get_soup(url_for_parse)
    table = soup.find('table', {'class': 'data levels'})

    # Parse the table rows and headers
    headers = [header.text for header in table.find_all('th')]
    headers.insert(0, "---")
    rows = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        rows.append([column.text for column in columns])
    # Create a DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Clean the DataFrame
    df = df.replace('\n', '', regex=True).dropna().reset_index(drop=True)
    df_melted = df.melt(id_vars=['---'], var_name='Год', value_name='Значение')
    df_cleaned = df_melted.loc[df_melted['Год'] != '2022(факт)']
    df_pivot = df_cleaned.pivot(index='Год', columns='---', values='Значение')

    # Сбросим индекс, чтобы 'Год' стал одной из колонок
    df_pivot.reset_index(inplace=True)
    df_pivot['Год'] = pd.to_datetime(df_pivot['Год'], format='%Y')
    new_df = pd.DataFrame(
        pd.date_range(df_pivot['Год'].min(), df_pivot['Год'].max() + pd.DateOffset(day=31) + pd.DateOffset(months=11),
                      freq='D'), columns=['Год'])

    new_df = new_df.merge(df_pivot, on='Год', how='left')
    # Заполнение пропущенных значений методом forward fill
    new_df.ffill(inplace=True)
    new_df = new_df.rename(columns={'Год': 'date'})
    new_df = new_df.applymap(replace_with_average)
    df.columns = df.columns.str.replace('\xa0', ' ', regex=True)
    new_df[new_df.columns[3]] = new_df[new_df.columns[3]].astype(float)
    new_df[new_df.columns[3]] = new_df[new_df.columns[3]].astype(float)
    write_to_db(new_df, "prediction")
    return new_df


if __name__ == "__main__":
    df = transform_df_to_format(get_inflation_predict())
    df = approximate_df_from_year_to_monthly(df, df.columns[3])
    print(df)
