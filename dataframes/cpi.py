from sqlalchemy import exc

from data_transform.transform_df import transform_df_to_format
from db.db_to_pandas import read_dataframe_from_table
from parser.cpi import get_cpi_data


def get_cpi_df():
    try:
        df = read_dataframe_from_table("cpi")
    except exc.SQLAlchemyError as e:
        df = get_cpi_data()
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_cpi_df()).to_string())
