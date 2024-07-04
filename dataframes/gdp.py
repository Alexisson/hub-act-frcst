from sqlalchemy import exc
from db.db_to_pandas import read_dataframe_from_table


from data_transform.spikes_remove import remove_spikes
from parser.gdp import get_gdp_on_2021_prices_data, get_gdp_dataframe_wout_seasons_data, get_gdp_data


def get_gdp_on_2021_prices_df(spikes_remove=True, window_size=3, sigma=2):
    try:
        df = read_dataframe_from_table("gdp_on_2021_prices")
    except exc.SQLAlchemyError as e:
        df = get_gdp_on_2021_prices_data()
    if spikes_remove:
        df = remove_spikes(df, 'gdp', window_size, sigma)
    return df


def get_gdp_dataframe_wout_seasons_df(spikes_remove=True, window_size=3, sigma=2):
    try:
        df = read_dataframe_from_table("gdp_on_2021_prices")
    except exc.SQLAlchemyError as e:
        df = get_gdp_dataframe_wout_seasons_data()
    if spikes_remove:
        df = remove_spikes(df, 'gdp', window_size, sigma)
    return df


def get_gdp_df(spikes_remove=True, window_size=3, sigma=2):
    try:
        df = read_dataframe_from_table("gdp")
    except exc.SQLAlchemyError as e:
        df = get_gdp_data()
    if spikes_remove:
        df = remove_spikes(df, 'gdp', window_size, sigma)
    return df


# download_gdp()
if __name__ == "__main__":
    pass
