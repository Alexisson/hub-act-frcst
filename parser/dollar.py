import datetime
import os.path
from pathlib import Path

import requests
import pandas as pd

from parser.cfg import FOLDER

start_date = datetime.datetime.strptime("01.01.2015", "%d.%m.%Y")
end_date = datetime.datetime.now()


def download_dollar_exchange_rate(start_date, end_date):
    if not Path(os.path.join(FOLDER, "dollar")).is_dir():
        Path(os.path.join(FOLDER, "dollar")).mkdir(parents=True)
    start_date_str = start_date.strftime("%d.%m.%Y")
    start_date_str_2 = start_date.strftime("%m.%d.%Y")
    end_date_str = end_date.strftime("%d.%m.%Y")
    end_date_str_2 = end_date.strftime("%m.%d.%Y")
    dollar_url = f"https://cbr.ru/Queries/UniDbQuery/DownloadExcel/98956?Posted=True&so=1&mode=2&VAL_NM_RQ=R01235&From={start_date_str}&To={end_date_str}&FromDate={start_date_str_2.replace('.', '%2F')}&ToDate={end_date_str_2.replace('.', '%2F')}"

    resp = requests.get(dollar_url)
    if not Path(os.path.join(os.path.join("files", "dollar"), f"{start_date_str}-{end_date_str}.xlsx")).is_file():
        output = open(os.path.join(os.path.join("files", "dollar"), f"{start_date_str}-{end_date_str}.xlsx"), 'wb')
        output.write(resp.content)
        output.close()


def get_dollar_df(start_date: datetime.datetime, end_date: datetime.datetime):
    download_dollar_exchange_rate(start_date, end_date)
    start_date_str = start_date.strftime("%d.%m.%Y")
    end_date_str = end_date.strftime("%d.%m.%Y")
    download_dollar_exchange_rate(start_date, end_date)

    df = pd.read_excel(os.path.join(os.path.join("files", "dollar"), f"{start_date_str}-{end_date_str}.xlsx"),
                       usecols=['data', 'curs'])
    df = df.rename(columns={'data': 'date'})
    return df


if __name__ == "__main__":
    print(get_dollar_df(start_date, end_date))
