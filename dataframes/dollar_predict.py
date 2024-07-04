from sqlalchemy import exc

from data_transform.transform_df import transform_df_to_format
from db.db_to_pandas import read_dataframe_from_table
from parser.dollar_predict import get_dollar_predict_data


def get_dollar_predict_df():
    try:
        df = read_dataframe_from_table("dollar_predict")
    except exc.SQLAlchemyError as e:
        df = get_dollar_predict_data()
    return df


if __name__ == "__main__":
    print(transform_df_to_format(get_dollar_predict_df()))
