import os
from calendar import monthrange
from datetime import datetime
from pathlib import Path

import pandas as pd

from db.pandas_to_db import write_to_db
from parser.cfg import FOLDER
from parser.utils import download_xlsx_file


def month_to_number(month_name):
    months = {
        'январь': 1, 'февраль': 2, 'март': 3, 'апрель': 4, 'май': 5,
        'июнь': 6, 'июль': 7, 'август': 8, 'сентябрь': 9, 'октябрь': 10,
        'ноябрь': 11, 'декабрь': 12
    }
    return months[month_name.lower()]


def download_cpi():
    if not Path(os.path.join(FOLDER, "cpi")).is_dir():
        Path(os.path.join(FOLDER, "cpi")).mkdir(parents=True)

    bal_url = "https://rosstat.gov.ru/storage/mediabank/Ipc_mes_05-2024.xlsx"
    download_xlsx_file(bal_url, os.path.join(FOLDER, "cpi"))
    print(f"File downloaded:{bal_url.split('/')[-1]}")


def get_cpi_data():
    if not Path(os.path.join(os.path.join("files", "cpi"), f"Ipc_mes_05-2024.xlsx")).is_file():
        download_cpi()
    df = pd.read_excel(os.path.join(os.path.join("files", "cpi"), f"Ipc_mes_05-2024.xlsx"), sheet_name="01",
                       usecols='B:AI', skiprows=4, nrows=12)
    df.columns = [str(year) for year in range(1991, 1991 + df.shape[1])]
    result = pd.DataFrame(columns=['date', 'value'])
    for index, row in df.iterrows():
        for year in range(1991, 1991 + df.shape[1] - 1):
            # Создаем дату первого дня месяца
            date = datetime(year, index + 1, 1)
            # Добавляем строку в результат
            result = pd.concat([result, pd.DataFrame({'date': [date], 'value': [row[str(year)]]})], ignore_index=True)
    write_to_db(result, "cpi")
    return result


if __name__ == "__main__":
    print(get_cpi_df())
