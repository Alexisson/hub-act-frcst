import pandas as pd
import requests

from data_transform.transform_df import transform_df_to_format


def get_loans_volume_msp_df(start_year: int, end_year: int):

    url = f"https://cbr.ru/dataservice/data?y1={start_year}&y2={end_year}&publicationId=23&datasetId=52&measureId=22"
    request = requests.get(url)
    df = pd.DataFrame()
    for row in request.json()["RawData"]:
        df = pd.concat([df, pd.DataFrame({"date": [pd.to_datetime(row["date"])], "msp_loans": [row["obs_val"]]})],
                       ignore_index=True)
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_loans_volume_msp_df(2015, 2023)))
