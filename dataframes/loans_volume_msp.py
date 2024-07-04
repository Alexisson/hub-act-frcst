from sqlalchemy import exc

from data_transform.spikes_remove import remove_spikes
from db.db_to_pandas import read_dataframe_from_table
from parser.loans_volume_msp import get_loans_volume_msp_data


def get_loans_volume_msp_df(start_year: int, end_year: int, measure_id=22, spikes_remove=True, window_size=3,
                                sigma=2):
    try:
        df = read_dataframe_from_table("loans_volume_msp")
    except exc.SQLAlchemyError as e:
        df = get_loans_volume_msp_data(start_year, end_year, measure_id)
    if spikes_remove:
        df = remove_spikes(df, "msp_loans_volume", window_size, sigma)
    return df


if __name__ == "__main__":
    pass
