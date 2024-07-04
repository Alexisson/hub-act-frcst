import datetime

from sqlalchemy import exc

from data_transform.spikes_remove import remove_spikes
from db.db_to_pandas import read_dataframe_from_table
from parser.inflation import get_inflation_data


def get_inflation_df(start_date: datetime.datetime, end_date: datetime.datetime, spikes_remove=True, window_size=3,
                       sigma=2):
    try:
        df = read_dataframe_from_table("inflation")
    except exc.SQLAlchemyError as e:
        df = get_inflation_data(start_date, end_date)
    if spikes_remove:
        df = remove_spikes(df, df.columns[1], window_size, sigma)
        df = remove_spikes(df, df.columns[2], window_size, sigma)
    return df


if __name__ == "__main__":
    pass
