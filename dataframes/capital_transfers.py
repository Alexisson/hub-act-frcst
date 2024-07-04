from sqlalchemy import exc

from data_transform.spikes_remove import remove_spikes
from data_transform.transform_df import transform_df_to_format
from db.db_to_pandas import read_dataframe_from_table
from parser.capital_transfers import get_capital_transfers_data


def get_capital_transfers_df(start_year: int, end_year: int, spikes_remove=True, window_size=3, sigma=2):
    try:
        df = read_dataframe_from_table("capital_transfers")
    except exc.SQLAlchemyError as e:
        df = get_capital_transfers_data(start_year, end_year)
    if spikes_remove:
        df = remove_spikes(df, 'balance', window_size, sigma)
        df = remove_spikes(df, 'input', window_size, sigma)
        df = remove_spikes(df, 'output', window_size, sigma)
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_capital_transfers_df(2019, 2023)).to_string())
