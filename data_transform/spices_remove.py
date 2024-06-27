import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose


def remove_spikes(df, column_name, window_size=3, sigma=2):
    # Конвертируем столбец 'date' в формат datetime и сортируем данные
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').set_index('date')

    # Декомпозиция временного ряда
    decomposition = seasonal_decompose(df[column_name], model='additive', period=window_size)

    # Извлекаем сезонную и остаточную компоненты
    seasonal = decomposition.seasonal
    residuals = decomposition.resid

    # Определяем порог для обнаружения выбросов
    threshold = residuals.std() * sigma

    # Удаляем выбросы
    outliers = residuals.abs() > threshold
    df[column_name][outliers] = None

    # Заполняем пропущенные значения сглаженными данными
    df[column_name].interpolate(method='time', inplace=True)

    # Добавляем сезонную компоненту обратно к данным
    df[column_name] += seasonal

    return df.reset_index()