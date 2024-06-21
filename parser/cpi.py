import os
from calendar import monthrange
from datetime import datetime

import pandas as pd


def get_cpi_df():
    df = pd.read_excel(os.path.join(os.path.join("files", "cpi"), f"ИПЦ.xlsx"))
    df = df[1:]
    daily_data = []
    for index, row in df.iterrows():
        year, month = int(row['T']), int(row['CPI_M_CHI'])
        last_day = monthrange(year, month)[1]
        for day in range(1, last_day + 1):
            date = datetime(year, month, day)
            daily_data.append({'date': date, 'cpi': row['CPI_M_CHI']})
    return pd.DataFrame(daily_data)


if __name__ == "__main__":
    print(get_cpi_df())
