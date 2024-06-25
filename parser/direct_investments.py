import pandas as pd
import requests

from data_transform.transform_df import transform_df_to_format


def get_direct_investments(start_year: int, end_year: int):
    url = f"https://cbr.ru/dataservice/data?y1={start_year}&y2={end_year}&publicationId=11&datasetId=19&measureId="
    request = requests.get(url)
    df = pd.DataFrame(
        columns=["date", "balance", "pure_assumption_of_liability", "net_acquisition_of_financial_assets"])
    i = 0
    for row in request.json()["RawData"]:
        if i % 3 == 0:
            values = []
            values.append(pd.to_datetime(row["date"]))
            values.append(row["obs_val"])
        elif i % 3 == 1:
            values.append(row["obs_val"])
        else:
            values.append(row["obs_val"])
            df.loc[i // 3] = values
        i += 1
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_direct_investments(2015, 2023)))
