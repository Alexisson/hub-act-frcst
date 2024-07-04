import datetime
import os.path
from pathlib import Path

import requests
import pandas as pd

from data_transform.calculate_avg import get_average_coefficient, approximate_df_from_year_to_monthly
from data_transform.spikes_remove import remove_spikes
from db.pandas_to_db import write_to_db
from parser.cfg import FOLDER
from data_transform.transform_df import transform_df_to_format

start_date = datetime.datetime.strptime("01.01.2015", "%d.%m.%Y")
end_date = datetime.datetime.now()


def download_inflation(start_date, end_date):
    if not Path(os.path.join(FOLDER, "inflation")).is_dir():
        Path(os.path.join(FOLDER, "inflation")).mkdir(parents=True)
    start_date_str = start_date.strftime("%d.%m.%Y")
    start_date_str_2 = start_date.strftime("%m.%d.%Y")
    end_date_str = end_date.strftime("%d.%m.%Y")
    end_date_str_2 = end_date.strftime("%m.%d.%Y")

    inflation_url = f"https://www.cbr.ru/Queries/UniDbQuery/DownloadExcel/132934?FromDate={start_date_str_2.replace('.', '%2F')}&ToDate={end_date_str_2.replace('.', '%2F')}&posted=False"

    resp = requests.get(inflation_url)
    if not Path(os.path.join(os.path.join("files", "inflation"), f"{start_date_str}-{end_date_str}.xlsx")).is_file():
        output = open(os.path.join(os.path.join("files", "inflation"), f"{start_date_str}-{end_date_str}.xlsx"), 'wb')
        output.write(resp.content)
        output.close()


def get_inflation_data(start_date: datetime.datetime, end_date: datetime.datetime, spikes_remove=True, window_size=3, sigma=2):
    download_inflation(start_date, end_date)
    start_date_str = start_date.strftime("%d.%m.%Y")
    end_date_str = end_date.strftime("%d.%m.%Y")
    download_inflation(start_date, end_date)

    df = pd.read_excel(os.path.join(os.path.join("files", "inflation"), f"{start_date_str}-{end_date_str}.xlsx"),
                       converters={'Дата': str}).iloc[:, : 3]
    df['Дата'] = pd.to_datetime(df['Дата'], format='%m.%Y')

    # Создание нового DataFrame с датами каждый день
    new_df = pd.DataFrame(pd.date_range(df['Дата'].min(), df['Дата'].max(), freq='D'), columns=['Дата'])

    # Объединение нового DataFrame с исходным по датам
    new_df = new_df.merge(df, on='Дата', how='left')

    # Заполнение пропущенных значений методом forward fill
    new_df.ffill(inplace=True)
    new_df = new_df.rename(columns={'Дата': 'date'})
    write_to_db(new_df, "inflation")
    return new_df


if __name__ == "__main__":
    df = transform_df_to_format(get_inflation_df(start_date, end_date))
    print(df)
