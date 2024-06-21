import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from parser.cfg import FOLDER


def download_gdp():
    if not Path(os.path.join(FOLDER, "gdp")).is_dir():
        Path(os.path.join(FOLDER, "gdp")).mkdir(parents=True)

    gdp_url = "https://rosstat.gov.ru/storage/mediabank/VVP_na_dushu_s1995-2023.xls"

    resp = requests.get(gdp_url)
    if not Path(os.path.join(os.path.join("files", "gdp"), f"VVP_na_dushu_s1995-2023.xlsx")).is_file():
        output = open(os.path.join(os.path.join("files", "gdp"), f"VVP_na_dushu_s1995-2023.xlsx"), 'wb')
        output.write(resp.content)
        output.close()


def get_dfg_dataframe():
    df = pd.read_excel(os.path.join(os.path.join("files", "gdp"), f"VVP_na_dushu_s1995-2023.xlsx"),
                       sheet_name="1", usecols='A:Q', skiprows=2, nrows=2)
    df_melted = df.melt(var_name='date', value_name='gdp')
    df_expanded = pd.DataFrame()

    for index, row in df_melted.iterrows():
        year = int(row['date'])
        value = row['gdp']
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        date_range = pd.date_range(start_date, end_date, freq='D')
        year_data = pd.DataFrame({'date': date_range, 'gdp': np.repeat(value, len(date_range))})
        df_expanded = pd.concat([df_expanded, year_data], ignore_index=True)

    return df_expanded


# download_gdp()
if __name__ == "__main__":
    print(get_dfg_dataframe())
