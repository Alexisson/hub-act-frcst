from functools import lru_cache

import pandas as pd
import requests

from data_transform.spikes_remove import remove_spikes
from data_transform.transform_df import transform_df_to_format
from db.pandas_to_db import write_to_db


@lru_cache(maxsize=None)
def get_measures(dataset_id: int = 52):
    url = f"https://cbr.ru/dataservice/measures?datasetId={dataset_id}"
    request = requests.get(url)
    regions = {}
    for i in request.json()['measure']:
        regions[i["id"]] = i["name"]
    return regions


def get_loans_volume_msp_data(start_year: int, end_year: int, measure_id=22):
    url = f"https://cbr.ru/dataservice/data?y1={start_year}&y2={end_year}&publicationId=23&datasetId=53&measureId={measure_id}"
    request = requests.get(url)
    df = pd.DataFrame(
        columns=["date", "msp_loans_volume"])
    i = 0
    for row in request.json()["RawData"]:
        if row["element_id"] == 35:
            values = []
            values.append(pd.to_datetime(row["date"]) - pd.DateOffset(months=1))
            values.append(row["obs_val"])
            df.loc[i] = values
            i += 1

    write_to_db(df, "msp_loans_volume")
    return df


if __name__ == "__main__":
    print(get_measures())
    #print(transform_df_to_format(get_loans_volume_msp_df(2015, 2023, measure_id=85)))
