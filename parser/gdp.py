import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from data_transform.transform_df import transform_df_to_format
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


def get_gdp_dataframe():
    download_gdp()
    df = pd.read_excel(os.path.join(os.path.join("files", "gdp"), f"VVP_na_dushu_s1995-2023.xlsx"),
                       sheet_name="1", usecols='A:Q', skiprows=2, nrows=2)
    df_melted = df.melt(var_name='date', value_name='gdp')
    df2 = pd.read_excel(os.path.join(os.path.join("files", "gdp"), f"VVP_na_dushu_s1995-2023.xlsx"),
                        sheet_name="2", usecols='A:M', skiprows=2, nrows=2)
    df_melted2 = df2.melt(var_name='date', value_name='gdp')
    df_expanded = pd.DataFrame()
    df_melted = pd.concat([df_melted, df_melted2], axis=0)
    for index, row in df_melted.iterrows():
        year = int(str(row['date'])[:4])
        value = row['gdp']
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        date_range = pd.date_range(start_date, end_date, freq='D')
        year_data = pd.DataFrame({'date': date_range, 'gdp': np.repeat(value, len(date_range))})
        df_expanded = pd.concat([df_expanded, year_data], ignore_index=True)

    return df_expanded


# download_gdp()
if __name__ == "__main__":
    df = transform_df_to_format(get_gdp_dataframe())
    print(df)
