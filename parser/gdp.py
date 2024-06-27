import os
import re
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from data_transform.spikes_remove import remove_spikes
from data_transform.transform_df import transform_df_to_format
from parser.cfg import FOLDER


def download_gdp():
    if not Path(os.path.join(FOLDER, "gdp")).is_dir():
        Path(os.path.join(FOLDER, "gdp")).mkdir(parents=True)

    gdp_url = "https://rosstat.gov.ru/storage/mediabank/VVP_KVartal_s%201995-2024.xlsx"

    resp = requests.get(gdp_url)
    if not Path(os.path.join(os.path.join("files", "gdp"), f"VVP_KVartal_s%201995-2024.xlsx")).is_file():
        output = open(os.path.join(os.path.join("files", "gdp"), f"VVP_KVartal_s%201995-2024.xlsx"), 'wb')
        output.write(resp.content)
        output.close()


def to_date(year, quarter):
    # Словарь для преобразования квартала в месяц
    quarter_to_month = {'I квартал': 1, 'II квартал': 4, 'III квартал': 7, 'IV квартал': 10}
    # Возвращаем дату, соответствующую первому дню квартала
    return datetime(year, quarter_to_month[quarter], 1)


def get_gdp_on_2021_prices_dataframe(spikes_remove=True, window_size=3, sigma=2):
    download_gdp()
    df = pd.read_excel(os.path.join(os.path.join("files", "gdp"), f"VVP_KVartal_s%201995-2024.xlsx"),
                       sheet_name="9", usecols='A:BA', skiprows=2, nrows=3)

    columns = df.columns.tolist()

    # Проходим по списку колонок и заменяем 'Unnamed' на ближайшую слева цифру
    for i in range(len(columns)):
        if "Unnamed" in str(columns[i]):
            # Находим ближайшую слева цифру, используя регулярные выражения
            # Предполагаем, что цифра всегда будет слева от 'Unnamed'
            left_number = re.search(r'\d+', str(columns[i - 1])).group()
            columns[i] = int(str(left_number)[:4])
        columns[i] = int(str(columns[i])[:4])

    # Обновляем имена колонок в DataFrame
    df.columns = columns
    new_df = pd.DataFrame(columns=["date", "gdp"])
    i = 0
    years = list(range(2011, 2025))
    dates = []
    values = df.T[1].tolist()
    quaters = ['I квартал', 'II квартал', 'III квартал', 'IV квартал']
    i = 0

    for year in years:
        for quater in quaters:
            if i < len(values):
                new_df = pd.concat([new_df, pd.DataFrame(
                    {"date": [pd.to_datetime(to_date(year, quater))],
                     "gdp": [values[i]]}
                )], ignore_index=True)
                i += 1
    new_df.set_index('date', inplace=True)

    # Заполняем пропущенные месяцы данными
    df_resampled = new_df.resample('MS').ffill()
    df_resampled = df_resampled.reset_index()
    if spikes_remove:
        df_resampled = remove_spikes(df_resampled, 'gdp', window_size, sigma)
    return df_resampled


def get_gdp_dataframe_wout_seasons():
    download_gdp()
    df = pd.read_excel(os.path.join(os.path.join("files", "gdp"), f"VVP_KVartal_s%201995-2024.xlsx"),
                       sheet_name="10", usecols='A:BA', skiprows=2, nrows=3)

    columns = df.columns.tolist()

    # Проходим по списку колонок и заменяем 'Unnamed' на ближайшую слева цифру
    for i in range(len(columns)):
        if "Unnamed" in str(columns[i]):
            # Находим ближайшую слева цифру, используя регулярные выражения
            # Предполагаем, что цифра всегда будет слева от 'Unnamed'
            left_number = re.search(r'\d+', str(columns[i - 1])).group()
            columns[i] = int(str(left_number)[:4])
        columns[i] = int(str(columns[i])[:4])

    # Обновляем имена колонок в DataFrame
    df.columns = columns
    new_df = pd.DataFrame(columns=["date", "gdp"])
    i = 0
    years = list(range(2011, 2025))
    dates = []
    values = df.T[1].tolist()
    quaters = ['I квартал', 'II квартал', 'III квартал', 'IV квартал']
    i = 0

    for year in years:
        for quater in quaters:
            if i < len(values):
                new_df = pd.concat([new_df, pd.DataFrame(
                    {"date": [pd.to_datetime(to_date(year, quater))],
                     "gdp": [values[i]]}
                )], ignore_index=True)
                i += 1
    new_df.set_index('date', inplace=True)

    # Заполняем пропущенные месяцы данными
    df_resampled = new_df.resample('MS').ffill()
    return df_resampled.reset_index()


def get_gdp_dataframe():
    download_gdp()
    df = pd.read_excel(os.path.join(os.path.join("files", "gdp"), f"VVP_KVartal_s%201995-2024.xlsx"),
                       sheet_name="2", usecols='A:BA', skiprows=2, nrows=3)

    columns = df.columns.tolist()

    # Проходим по списку колонок и заменяем 'Unnamed' на ближайшую слева цифру
    for i in range(len(columns)):
        if "Unnamed" in str(columns[i]):
            # Находим ближайшую слева цифру, используя регулярные выражения
            # Предполагаем, что цифра всегда будет слева от 'Unnamed'
            left_number = re.search(r'\d+', str(columns[i - 1])).group()
            columns[i] = int(str(left_number)[:4])
        columns[i] = int(str(columns[i])[:4])

    # Обновляем имена колонок в DataFrame
    df.columns = columns
    new_df = pd.DataFrame(columns=["date", "gdp"])
    i = 0
    years = list(range(2011, 2025))
    dates = []
    values = df.T[1].tolist()
    quaters = ['I квартал', 'II квартал', 'III квартал', 'IV квартал']
    i = 0

    for year in years:
        for quater in quaters:
            if i < len(values):
                new_df = pd.concat([new_df, pd.DataFrame(
                    {"date": [pd.to_datetime(to_date(year, quater))],
                     "gdp": [values[i]]}
                )], ignore_index=True)
                i += 1
    new_df.set_index('date', inplace=True)

    # Заполняем пропущенные месяцы данными
    df_resampled = new_df.resample('MS').ffill()
    return df_resampled.reset_index()


# download_gdp()
if __name__ == "__main__":
    df = get_gdp_on_2021_prices_dataframe()
    print(transform_df_to_format(df))
