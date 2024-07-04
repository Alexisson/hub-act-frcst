import pandas as pd
import requests

from data_transform.spikes_remove import remove_spikes
from data_transform.transform_df import transform_df_to_format
from db.pandas_to_db import write_to_db


def get_broad_money_supply_data(start_year: int, end_year: int):
    url = f"https://cbr.ru/dataservice/data?y1={start_year}&y2={end_year}&publicationId=5&datasetId=8&measureId="
    request = requests.get(url)
    df = pd.DataFrame(
        columns=["date", "broad_money"])
    i = 0
    for row in request.json()["RawData"]:
        if row["element_id"] == 12:
            df.loc[i] = [pd.to_datetime(row["date"]) - pd.DateOffset(months=1), row["obs_val"]]
            i += 1
    write_to_db(df, "broad_money_supply")
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_broad_money_supply_data(2015, 2023)))
