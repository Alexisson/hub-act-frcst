import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import requests

from parser.cb_xlsx import get_soup
from parser.cfg import FOLDER, BASE_URL
from parser.utils import download_xlsx_file


def download_bal():
    if not Path(os.path.join(FOLDER, "bal")).is_dir():
        Path(os.path.join(FOLDER, "bal")).mkdir(parents=True)

    bal_url = "https://www.cbr.ru/statistics/macro_itm/svs/p_balance/"
    soup = get_soup(bal_url)
    file_urls = []
    a_tags = soup.find_all('a', href=lambda href: href and "bal_of_payments" in href and ".xlsx" in href)
    for a in a_tags:
        file_urls.append(a['href'])
    for url in file_urls:
        download_xlsx_file(BASE_URL + url, os.path.join(FOLDER, "bal"))
        print(f"File downloaded:{url.split('/')[-1]}")


def generate_dates(quarter_str, value):
    # Определение начальной и конечной даты квартала
    year = int(quarter_str.split(' ')[2])
    quarter = int(quarter_str[0])
    start_month = 3 * quarter - 2
    end_month = 3 * quarter
    start_date = datetime(year, start_month, 1)
    if quarter == 4:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)

    # Генерация списка дат для каждого дня в квартале
    date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    # Создание DataFrame с этими датами и значением
    df_quarter = pd.DataFrame({'data': date_list, 'значение': value})

    return df_quarter


# Счет текущих операций
def get_bal_df():
    if not Path(os.path.join(os.path.join("files", "bal"), f"bal_of_payments_standart.xlsx")).is_file():
        download_bal()
    df = pd.read_excel(os.path.join(os.path.join("files", "bal"), f"bal_of_payments_standart.xlsx"),
                       sheet_name="Кварталы", skiprows=4, usecols=lambda x: 'Unnamed' not in x, nrows=1)
    df_melted = df.melt(var_name='data', value_name='bal')
    df_daily = pd.DataFrame(columns=['data', 'значение'])
    for index, row in df_melted.iterrows():
        df_quarter = generate_dates(row['data'], row['bal'])
        df_daily = pd.concat([df_daily, df_quarter], ignore_index=True)
    return df_daily


print(get_bal_df().info())
