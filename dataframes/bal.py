from sqlalchemy import exc

from data_transform.spikes_remove import remove_spikes
from db.db_to_pandas import read_dataframe_from_table
from parser.bal import get_bal_data


def get_bal_df(spikes_remove=True, window_size=3, sigma=2):
    try:
        df = read_dataframe_from_table("bal")
    except exc.SQLAlchemyError as e:
        df = get_bal_data()
    if spikes_remove:
        df = remove_spikes(df, 'bal', window_size, sigma)
    return df
