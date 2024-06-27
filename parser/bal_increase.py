import os
from pathlib import Path

import pandas as pd

from data_transform.spices_remove import remove_spikes
from data_transform.transform_df import transform_df_to_format
from parser.cfg import FOLDER
from parser.utils import download_xlsx_file


def download_bal_increase():
    if not Path(os.path.join(FOLDER, "bal_increase")).is_dir():
        Path(os.path.join(FOLDER, "bal_increase")).mkdir(parents=True)

    bal_url = "https://cbr.ru/content/document/file/108632/indicators_cpd.xlsx"
    download_xlsx_file(bal_url, os.path.join(FOLDER, "bal_increase"))
    print(f"File downloaded:{bal_url.split('/')[-1]}")


def get_bal_increase_df(spikes_remove=True):
    if not Path(os.path.join(os.path.join("files", "bal_increase"), f"indicators_cpd.xlsx")).is_file():
        download_bal_increase()
    df = pd.read_excel(os.path.join(os.path.join("files", "bal_increase"), "indicators_cpd.xlsx"),
                       sheet_name="Лист1", usecols='B:JJ', nrows=1)
    df_melted = df.melt(var_name='date', value_name='bal_increase')
    if spikes_remove:
        df_melted = remove_spikes(df_melted, 'bal')
    return df_melted


if __name__ == "__main__":
    print(transform_df_to_format(get_bal_increase_df()))
