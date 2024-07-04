from sqlalchemy import exc

from db.db_to_pandas import read_dataframe_from_table
from parser.prediction import get_inflation_predict_data


def get_inflation_predict_df():
    try:
        df = read_dataframe_from_table("prediction")
    except exc.SQLAlchemyError as e:
        df = get_inflation_predict_data()
    return df


if __name__ == "__main__":
    pass
