from datetime import datetime

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

from data_transform.transform_df import transform_df_to_format

# Исторические данные по инфляции
data = {
    "date": [
        "01.2021", "02.2021", "03.2021", "04.2021", "05.2021", "06.2021", "07.2021", "08.2021", "09.2021", "10.2021",
        "11.2021", "12.2021",
        "01.2022", "02.2022", "03.2022", "04.2022", "05.2022", "06.2022", "07.2022", "08.2022", "09.2022", "10.2022",
        "11.2022", "12.2022",
        "01.2023", "02.2023", "03.2023", "04.2023", "05.2023", "06.2023", "07.2023", "08.2023", "09.2023", "10.2023",
        "11.2023", "12.2023",
        "01.2024", "02.2024", "03.2024", "04.2024", "05.2024"
    ],
    "inflation": [
        5.2, 5.7, 5.8, 5.5, 6.0, 6.5, 6.5, 6.7, 7.4, 8.13, 8.4, 8.39,
        8.73, 9.15, 16.69, 17.83, 17.1, 15.9, 15.1, 14.3, 13.68, 12.63, 11.98, 11.94,
        11.77, 10.99, 3.51, 2.31, 2.51, 3.25, 4.3, 5.15, 6.0, 6.69, 7.48, 7.42,
        7.44, 7.69, 7.72, 7.84, 8.3
    ]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'], format='%m.%Y')
df.set_index('date', inplace=True)

# Декомпозиция временного ряда
result = seasonal_decompose(df['inflation'], model='additive', period=12)
seasonal = result.seasonal

# Рассчитаем средние сезонные коэффициенты для каждого месяца
seasonal_factors = seasonal.groupby(seasonal.index.month).mean()
seasonal_factors.index = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
    'December'
]

# Прогноз инфляции на конец года
end_year_inflation = {
    '2024': 5.5,
    '2025': 4.2,
    '2026': 4.0
}

# Прогноз на оставшиеся месяцы 2024 года
inflation_june_2024 = 7.9
inflation_december_2024 = end_year_inflation['2024']
months_remaining_2024 = 6  # июль - декабрь

inflation_2024 = np.linspace(inflation_june_2024, inflation_december_2024, months_remaining_2024 + 1)
months_2024 = pd.date_range(start='2024-07-01', end='2024-12-01', freq='MS').month_name()
seasonal_adjusted_2024 = inflation_2024[1:] + seasonal_factors.loc[months_2024].values

# Прогноз на 2025 год
inflation_january_2025 = end_year_inflation['2024']
inflation_december_2025 = end_year_inflation['2025']
months_2025 = 12

inflation_2025 = np.linspace(inflation_january_2025, inflation_december_2025, months_2025 + 1)
months_2025_names = pd.date_range(start='2025-01-01', end='2025-12-01', freq='MS').month_name()
seasonal_adjusted_2025 = inflation_2025[1:] + seasonal_factors.loc[months_2025_names].values

# Прогноз на 2026 год
inflation_january_2026 = end_year_inflation['2025']
inflation_december_2026 = end_year_inflation['2026']
months_2026 = 12

inflation_2026 = np.linspace(inflation_january_2026, inflation_december_2026, months_2026 + 1)
months_2026_names = pd.date_range(start='2026-01-01', end='2026-12-01', freq='MS').month_name()
seasonal_adjusted_2026 = inflation_2026[1:] + seasonal_factors.loc[months_2026_names].values


# Вывод результатов


def month_to_number(month_name):
    months = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    return months[month_name.lower()]


# Функция для преобразования исходного DataFrame
def transform_df(original_df, year):
    # Преобразование имени месяца в номер месяца
    original_df['month_number'] = original_df['month'].apply(month_to_number)

    # Создание столбца 'date' с первым днем каждого месяца
    original_df['date'] = original_df['month_number'].apply(lambda x: datetime(year, x, 1))

    # Удаление ненужных столбцов
    final_df = original_df.drop(['month', 'month_number'], axis=1)

    # Переупорядочивание столбцов
    final_df = final_df[['date', 'inflation']]

    return final_df


def get_predicted_inflation():
    forecast_2024 = pd.DataFrame({
        'month': months_2024,
        'inflation': seasonal_adjusted_2024
    })

    forecast_2025 = pd.DataFrame({
        'month': months_2025_names,
        'inflation': seasonal_adjusted_2025
    })

    forecast_2026 = pd.DataFrame({
        'month': months_2026_names,
        'inflation': seasonal_adjusted_2026
    })
    return pd.concat([transform_df(forecast_2024, 2024), transform_df(forecast_2025, 2025), transform_df(forecast_2026, 2026)])


if __name__ == "__main__":
    print(transform_df_to_format(get_predicted_inflation()))