from sqlalchemy import exc

from data_transform.spikes_remove import remove_spikes
from db.db_to_pandas import read_dataframe_from_table
import parser.prediction
from parser.resident_loans_volume import get_loans_volume_resident_data


def get_new_loans_resident_data(measure_id=22, spikes_remove=True, window_size=3, sigma=2):
    try:
        df = read_dataframe_from_table("new_loans_resident")
    except exc.SQLAlchemyError as e:
        df = get_loans_volume_resident_data(measure_id)
    if spikes_remove:
        df = remove_spikes(df, "resident_loans_volume", window_size, sigma)
    return df


if __name__ == "__main__":
    pass
