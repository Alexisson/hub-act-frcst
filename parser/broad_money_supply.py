import pandas as pd
import requests

from data_transform.transform_df import transform_df_to_format


def get_broad_money_supply(start_year: int, end_year: int):
    url = f"https://cbr.ru/dataservice/data?y1={start_year}&y2={end_year}&publicationId=5&datasetId=8&measureId="
    request = requests.get(url)
    df = pd.DataFrame(
        columns=["date", "broad_money"])
    i = 0
    for row in request.json()["RawData"]:
        if i % 6 == 0:
            values = []
            values.append(pd.to_datetime(row["date"]))
            values.append(row["obs_val"])
            df.loc[i // 6] = values
        i += 1
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_broad_money_supply(2015, 2023)))
