import pandas as pd
import requests

from data_transform.spikes_remove import remove_spikes
from data_transform.transform_df import transform_df_to_format
from db.pandas_to_db import write_to_db


def get_direct_investments_data(start_year: int, end_year: int):
    url = f"https://cbr.ru/dataservice/data?y1={start_year}&y2={end_year}&publicationId=11&datasetId=19&measureId="
    request = requests.get(url)
    df = pd.DataFrame(
        columns=["date", "balance", "pure_assumption_of_liability", "net_acquisition_of_financial_assets"])
    i = 0
    values = {}
    for row in request.json()["RawData"]:
        if row["element_id"] == 28:
            values["date"] = pd.to_datetime(row["date"]) - pd.DateOffset(months=3)
            values["balance"] = row["obs_val"]
        elif row["element_id"] == 33:
            values["pure_assumption_of_liability"] = row["obs_val"]
        else:
            values["net_acquisition_of_financial_assets"] = row["obs_val"]
        if i % 3 == 2 and i > 0:
            df.loc[i // 3] = values
            values = {}
        i += 1
    df.set_index('date', inplace=True)

    # Заполняем пропущенные месяцы данными
    df_resampled = df.resample('MS').ffill()
    df_resampled = df_resampled.reset_index()
    write_to_db(df_resampled, "direct_investments")
    return df_resampled


if __name__ == "__main__":
    print(get_direct_investments_data(2015, 2023).to_string())
