import pandas as pd


def get_average_coefficient(df, column_name):
    average_rates = df.groupby('year')[column_name].mean().to_dict()

    # Расчет отношения текущей ставки к средней
    df['Отношение ставки к средней'] = df.apply(
        lambda row: row[column_name] / average_rates[row['year']], axis=1)
    # Расчет среднего отношения текущей ставки к средней для каждого месяца
    monthly_average = df.groupby('month_n')['Отношение ставки к средней'].mean().reset_index()

    # Переименование столбцов для соответствия заданию
    monthly_average.columns = ['month_n', 'avg']
    print(monthly_average.iloc[1])
    return monthly_average


def approximate_df_from_year_to_monthly(df, column_name):
    avg_df = get_average_coefficient(df, column_name)
    print(avg_df)
    merged_df = pd.merge(avg_df, df, on='month_n')

    # Умножение колонки 'value' на 'avg'
    merged_df['adjusted_value'] = merged_df[column_name] * merged_df['avg']
    print(merged_df.iloc[30]["avg"])
    merged_df.loc[merged_df['year'] >= 2024, column_name] = merged_df['adjusted_value']
    # Теперь merged_df содержит обновленные значения 'value' для указанных условий
    merged_df = merged_df.drop(columns=["Отношение ставки к средней", "adjusted_value", "avg"])
    return merged_df
