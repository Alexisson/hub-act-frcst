from typing import Tuple

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
from dataclasses import dataclass


@dataclass
class PredictResult:
    predict: pd.DataFrame
    mape: float
    start_date: str
    last_predict_date: str


@dataclass
class PredictInput:
    start_date: str = '2023-05'
    last_predict_date: str = '2026-03'
    trend: str = 'ct'
    custom: bool = False
    season_ord: Tuple = (1, 1, 1, 12)
    custom_pdq: Tuple = (1, 1, 1)


class Predictor:
    def __init__(self):
        self.__dataset = None
        self.predict = None

    @property
    def dataset(self):
        return self.__dataset

    @dataset.getter
    def dataset(self):
        return self.__dataset

    @dataset.setter
    def dataset(self, value):
        self.__dataset = value.copy()

    def mape(self, actual, predict):
        actual, predict = np.array(actual), np.array(predict)
        actual_safe = np.where(actual == 0, 1e-10, actual)
        return np.mean(np.abs((actual - predict) / actual_safe)) * 100

    def divide_data(self, date: str):
        split_index = self.dataset.index[self.dataset['date'] == date]
        train_size = split_index[0]
        test_size = len(self.dataset) - train_size
        train = self.dataset[self.dataset['date'] < date]
        test = self.dataset[self.dataset['date'] >= date]
        # Делаем из датафреймов серии
        train_data = train.copy()
        train_data.set_index(keys='date', drop=True, inplace=True)
        train_data = train_data.squeeze(axis=1)
        test_data = test.copy()
        test_data.set_index(keys='date', drop=True, inplace=True)
        test_data = test_data.squeeze(axis=1)
        return train_data, test_data

    # Отрисовка графика данных и их прогноза с указанием названия прогнозируемой величины
    # dataframe - исходные данные
    # predict - спрогнозированные данные
    # name - название прогнозируемой величины
    def show_plot(self, predict, input_params: PredictInput, name, plt_title='Российская Федерация'):
        self.predict = predict
        columns = list(self.dataset)
        plt.figure(figsize=(12, 4))
        plt.plot(self.dataset[columns[0]], self.dataset[columns[1]].values / 1e6)
        plt.plot(self.predict / 1e6)
        plt.xlabel('Дата')
        plt.ylabel(name + ', трлн руб.')
        plt.title(plt_title)
        plt.grid(True)
        plt.show()

    # Получение прогноза с помощью модели SARIMAX
    # dataframe - исходные данные
    # start_date - дата, от которой строится прогноз
    # last_predict_date - дата, до которой строится прогноз
    # ct_trend - необходимо ли искусственно выпрямить тренд (True задает линейный тренд)
    # custom - подбираем автоматически парамеры для настройки SARIMAX или передаем уже подобранные значения season_ord и custom_pdq
    def get_data_predict(self, input_params: PredictInput):
        train_data, test_data = self.divide_data(input_params.start_date)
        # Подбор параметров
        if input_params.custom:
            s_ord = input_params.season_ord
            pdq = input_params.custom_pdq
        else:
            parameter_search = auto_arima(train_data, start_p=1, start_q=1, max_p=3, max_q=3, m=12, start_P=1,
                                          seasonal=True, d=None, D=1, trace=False, error_action='ignore',
                                          suppress_warnings=True, stepwise=True)
            s_ord = parameter_search.seasonal_order
            pdq = parameter_search.order
        # ОБУЧЕНИЕ МОДЕЛИ
        model = SARIMAX(train_data, order=pdq, seasonal_order=s_ord, trend=input_params.trend,
                        measurement_error=True,
                        enforce_stationarity=True, enforce_invertibility=True)
        model_fit = model.fit()
        # Получение предсказания
        pred = model_fit.get_prediction(start=input_params.start_date, end=input_params.last_predict_date,
                                        dynamic=False)
        predict = pred.predicted_mean
        test_pred = predict[0:len(test_data)]
        self.predict = predict
        return PredictResult(
            predict=self.predict,
            mape=self.mape(test_data.values, test_pred.values),
            start_date=input_params.start_date,
            last_predict_date=input_params.last_predict_date
        )
