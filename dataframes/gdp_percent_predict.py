from sqlalchemy import exc

from db.db_to_pandas import read_dataframe_from_table
from parser.gdp import get_gdp_on_2021_prices_data


def get_gdp_percent_predict_df():
    try:
        df = read_dataframe_from_table("gdp_predict")
    except exc.SQLAlchemyError as e:
        df = get_gdp_on_2021_prices_data()
    return df


if __name__ == "__main__":
    pass
