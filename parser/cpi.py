import os
from calendar import monthrange
from datetime import datetime

import pandas as pd


def get_cpi_df():
    df = pd.read_excel(os.path.join(os.path.join("files", "cpi"), f"ИПЦ.xlsx"))
    df = df[1:]
    daily_data = []
    for index, row in df.iterrows():
        if len(str(row['T']).split()) == 2:
            year = int(str(row['T']).split()[0])
            month = int(str(row['T']).split()[1])
        else:
            month = int(row['T'])
        last_day = monthrange(year, month)[1]
        for day in range(1, last_day + 1):
            date = datetime(year, month, day)
            daily_data.append({'date': date, 'cpi': row['CPI_M_CHI']})
    return pd.DataFrame(daily_data)


if __name__ == "__main__":
    print(get_cpi_df())
