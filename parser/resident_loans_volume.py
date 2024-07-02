import os
import re
from pathlib import Path

import pandas as pd

from data_transform.spikes_remove import remove_spikes
from data_transform.transform_df import transform_df_to_format
from parser.cb_xlsx import download_files_from_href, get_soup, url_for_parse
from parser.cfg import BASE_URL, FOLDER
from parser.loans_volume_msp import get_measures
import warnings

warnings.simplefilter("ignore")

def get_loans_volume_resident(measure_id=22, spike_remove=True, window_size=3, sigma=2):
    soup = get_soup(url_for_parse)
    if not Path(os.path.join(FOLDER, "A_Debt_corp")).is_dir():
        Path(os.path.join(FOLDER, "A_Debt_corp")).mkdir(parents=True)
        download_files_from_href(soup, BASE_URL, ["A_Debt_corp"])
    # Путь к директории
    directory = os.path.join('files', 'A_Debt_corp')

    # Регулярное выражение для поиска даты в имени файла
    date_pattern = re.compile(r'_(\d{8})\.xlsx$')
    df = pd.DataFrame(columns=["date", "resident_new_loans"])
    # Проходим по всем файлам в директории
    for ind, filename in enumerate(os.listdir(directory)):

        # Ищем соответствие с регулярным выражением
        match = date_pattern.search(filename)
        if match:
            date = match.group(1)
            measure_name = get_measures()[measure_id]
            row = pd.read_excel(os.path.join(directory, filename), sheet_name="итого", skiprows=2, index_col=0, engine="openpyxl")
            row.index = row.index.str.lower()
            filtered_df = row.loc[row.index == measure_name.lower()]
            filtered_df = filtered_df[['ВСЕГО']]
            df.loc[ind] = {
                "date": pd.Timestamp(year=int(date[:2] + date[2:4]), month=int(date[4:6]), day=int(date[6:])),
                "resident_new_loans": float(filtered_df.iloc[0])}

    if spike_remove:
        df = remove_spikes(df, "resident_new_loans", window_size, sigma)
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_loans_volume_resident()).to_string())
