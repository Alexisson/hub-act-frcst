import numpy as np
import pandas as pd

from data_transform.transform_df import transform_df_to_format
from parser.cb_xlsx import get_soup
from parser.prediction import replace_with_average

URL = "https://ru.tradingeconomics.com/russia/forecast"


def get_inflation_predict():
    # Parse the HTML content

    # Find the table with the class 'data levels'
    soup = get_soup(URL)
    tables = soup.find_all('table', {'class': 'table table-hover'})
    table = tables[1]
    # Parse the table rows and headers
    headers = [header.text for header in table.find_all('th')]
    headers.insert(0, "---")
    rows = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        rows.append([column.text for column in columns])
    # Create a DataFrame
    headers = [s.strip().replace('\n', '').replace('\r', '') for s in headers]
    df = pd.DataFrame(rows, columns=headers[1:])
    # Clean the DataFrame
    df = df.replace('\n', '', regex=True).dropna().reset_index(drop=True)
    df = df.replace('\r', '', regex=True)
    df = df.set_index('Обзор').T

    # Функция для преобразования квартала в дату
    def quarter_to_date(quarter):
        year = int(quarter.split('/')[1])
        quarter_num = int(quarter.split('/')[0][1])
        first_month_of_quarter = 3 * quarter_num - 2
        return pd.Timestamp(year=2000 + year, month=first_month_of_quarter, day=1)

    new_index = [quarter_to_date(q) for q in df.index[1:].insert(0, ["Q1/24"])]
    df.index = new_index
    df = df.iloc[:, [2]]
    df = df.reset_index()
    df.columns = ["date", "inflation"]

    # Заполняем пропущенные месяцы данными
    df.set_index('date', inplace=True)
    df = df.asfreq('D').fillna(method='ffill')
    df['inflation'] = df['inflation'].replace(r'\n', '', regex=True).replace(r'\r', '', regex=True)
    df['inflation'] = df['inflation'].astype(float)
    return df.reset_index()


if __name__ == "__main__":
    df = get_inflation_predict()
    print(transform_df_to_format(df))
