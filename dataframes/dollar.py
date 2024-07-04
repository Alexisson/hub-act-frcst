from datetime import datetime

from sqlalchemy import exc

from data_transform.spikes_remove import remove_spikes
from data_transform.transform_df import transform_df_to_format
from db.db_to_pandas import read_dataframe_from_table
from parser.dollar import get_dollar_data


def get_dollar_df(start_date: datetime, end_date: datetime, spikes_remove=True, window_size=3, sigma=2):
    try:
        df = read_dataframe_from_table("dollar")
    except exc.SQLAlchemyError as e:
        df = get_dollar_data(start_date, end_date)
    if spikes_remove:
        df = remove_spikes(df, 'curs', window_size, sigma)
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_dollar_df(2019, 2023)).to_string())
