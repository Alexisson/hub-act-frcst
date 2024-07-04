from sqlalchemy import exc

from db.db_to_pandas import read_dataframe_from_table
from parser.salary_regions import get_salary_regions_data


def get_salary_regions_df(measure_id=22):
    try:
        df = read_dataframe_from_table("salary_regions")
    except exc.SQLAlchemyError as e:
        df = get_salary_regions_data(measure_id)
    return df


if __name__ == "__main__":
    pass
