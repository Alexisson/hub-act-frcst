import os
from pathlib import Path

import pandas as pd

from data_transform.transform_df import transform_df_to_format
from parser.cb_xlsx import download_files_from_href, get_soup
from parser.cfg import FOLDER
from parser.loans_volume_msp import get_measures
from parser.utils import download_xlsx_file

url = "https://rosstat.gov.ru/labor_market_employment_salaries"
base_url = "https://rosstat.gov.ru/"
if not Path(FOLDER).is_dir():
    Path(FOLDER).mkdir(parents=True)
if not Path(os.path.join(FOLDER, "salary")).is_dir():
    Path(os.path.join(FOLDER, "salary")).mkdir(parents=True)


def download_salary(soup):
    file_urls = []
    a_tags = soup.find_all('a', href=lambda href: href and "tab4_zpl_2023" in href)
    for a in a_tags:
        file_urls.append(a['href'])
    for url in file_urls:
        download_xlsx_file(base_url + url, os.path.join(FOLDER, "salary"))
        print(f"File downloaded:{url.split('/')[-1]}")


def get_salary_df(measure_id=22):
    measure_name = get_measures()[measure_id]
    if not Path(os.path.join(os.path.join(FOLDER, "salary"), "tab4_zpl_2023.xlsx")).is_file():
        stats_soup = get_soup(url)
        download_salary(stats_soup)
    df1 = pd.read_excel(os.path.join(os.path.join(FOLDER, "salary"), "tab4_zpl_2023.xlsx"), sheet_name="2000-2017",index_col=0, skiprows=3)
    filtered_df = df1.loc[df1.index == measure_name]
    df2 = pd.read_excel(os.path.join(os.path.join(FOLDER, "salary"), "tab4_zpl_2023.xlsx"), sheet_name="с 2018",
                        index_col=0, skiprows=1)
    filtered_df2 = df2.loc[df2.index == measure_name]
    # Преобразование DataFrame в требуемый формат [date, value]
    result_df1 = filtered_df.melt(var_name='date', value_name='salary').reset_index(drop=True)
    result_df2 = filtered_df2.melt(var_name='date', value_name='salary').reset_index(drop=True)
    df_res = pd.concat([result_df1, result_df2], ignore_index=True)
    df_res['date'] = df_res['date'].apply(lambda x: str(x)[:4] if len(str(x)) >= 4 else str(x))
    df_res['date'] = pd.to_datetime(df_res['date'], format='%Y')
    df_res.loc[df_res.index[-1], 'date'] += pd.DateOffset(months=11)
    df_res.set_index('date', inplace=True)

    # Заполняем пропущенные месяцы данным
    df_res = df_res.asfreq('D').fillna(method='ffill')
    return df_res


if __name__ == "__main__":
    print(transform_df_to_format(get_salary_df()))
