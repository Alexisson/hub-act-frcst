import pandas as pd
import requests

from data_transform.transform_df import transform_df_to_format


def get_loans_volume_msp_df(start_year: int, end_year: int):

    url = f"https://cbr.ru/dataservice/data?y1={start_year}&y2={end_year}&publicationId=23&datasetId=52&measureId=22"
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
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_loans_volume_msp_df(2015, 2023)))