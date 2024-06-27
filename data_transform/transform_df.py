import pandas as pd


# df - date(datetime), value(любой тип) преобразует в df
# df_new
# Отчетный период - строка в формате Январь 2022г.
# month_n - порядковый номер месяца
# year - год числом
# value - старая колонка из df
def transform_df_to_format(df):
    df_new = df.copy()
    df_new['month_n'] = df['date'].dt.month

    # Add 'year' column representing the year
    df_new['year'] = df['date'].dt.year

    # Add 'Отчетный период' column formatted as 'Month Year', e.g., 'Январь 2022'
    df_new['Отчетный период'] = df['date'].dt.strftime('%B %Y г.')

    # Ensure the 'Отчетный период' column is in Russian
    df_new['Отчетный период'] = df_new['Отчетный период'].apply(
        lambda x: x.replace('January', 'Январь').replace('February', 'Февраль').replace('March', 'Март').replace(
            'April', 'Апрель').replace('May', 'Май').replace('June', 'Июнь').replace('July', 'Июль').replace('August',
                                                                                                             'Август').replace(
            'September', 'Сентябрь').replace('October', 'Октябрь').replace('November', 'Ноябрь').replace('December',
                                                                                                         'Декабрь'))

    col_name = df.columns[1]
    # Группируем данные по месяцу и году, вычисляем среднее
    monthly_mean = df_new.groupby(df_new['date'].dt.to_period('M'))[col_name].mean().reset_index()

    # Преобразуем обратно в datetime
    monthly_mean['date'] = monthly_mean['date'].dt.to_timestamp()

    monthly_mean = pd.merge(df_new, monthly_mean, on=['date'])
    monthly_mean = monthly_mean.drop(columns=["date"], axis=1)
    return monthly_mean.drop_duplicates()
