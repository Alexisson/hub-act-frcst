from sqlalchemy import exc

from data_transform.spikes_remove import remove_spikes
from data_transform.transform_df import transform_df_to_format
from db.db_to_pandas import read_dataframe_from_table
from parser.broad_money_supply import get_broad_money_supply_data


def get_broad_money_supply_df(start_year: int, end_year: int, spikes_remove=True, window_size=3, sigma=2):
    try:
        df = read_dataframe_from_table("broad_money_supply")
    except exc.SQLAlchemyError as e:
        df = get_broad_money_supply_data(start_year, end_year)
    if spikes_remove:
        df = remove_spikes(df, 'broad_money_supply', window_size, sigma)
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_broad_money_supply_df(2015, 2023)))
