from sqlalchemy import exc

from data_transform.spikes_remove import remove_spikes
from data_transform.transform_df import transform_df_to_format
from db.db_to_pandas import read_dataframe_from_table
from parser.direct_investments import get_direct_investments_data


def get_direct_investments_df(start_year: int, end_year: int, spikes_remove=True, window_size=3, sigma=2):
    try:
        df = read_dataframe_from_table("direct_investments")
    except exc.SQLAlchemyError as e:
        df = get_direct_investments_data(start_year, end_year)
    if spikes_remove:
        df = remove_spikes(df, 'balance', window_size, sigma)
        df = remove_spikes(df, 'pure_assumption_of_liability', window_size, sigma)
        df = remove_spikes(df, 'net_acquisition_of_financial_assets', window_size, sigma)
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_direct_investments_df(2019, 2023)).to_string())
