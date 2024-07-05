from enum import Enum

from dataframes.loans_volume_msp import get_loans_volume_msp_df
from dataframes.new_loans_msp import get_new_loans_msp_df
from dataframes.resident_loans_volume import get_resident_loans_volume_df
from dataframes.resident_new_loans import get_new_loans_resident_data
from parser.loans_volume_msp import get_measures
from predictor import PredictInput, Predictor


class PredictEnum(Enum):
    RESIDENT_LOANS_VOLUME = 0
    RESIDENT_NEW_LOANS = 1
    MSP_LOANS_VOLUME = 2
    MSP_NEW_LOANS = 3


class LoansPredict(Predictor):
    def __init__(self, datasource: PredictEnum):
        self.plot_title = ""
        if datasource == PredictEnum.MSP_NEW_LOANS:
            self.datasource = get_new_loans_msp_df
            self.plot_title = "Объем выданных кредитов МСП"
        elif datasource == PredictEnum.MSP_LOANS_VOLUME:
            self.datasource = get_loans_volume_msp_df
            self.plot_title = "Задолженность по кредитам МСП"
        elif datasource == PredictEnum.RESIDENT_NEW_LOANS:
            self.datasource = get_new_loans_resident_data
            self.plot_title = "Объем выданных кредитов резиденты"
        elif datasource == PredictEnum.RESIDENT_LOANS_VOLUME:
            self.datasource = get_resident_loans_volume_df
            self.plot_title = "Задолженность по кредитам резиденты"
        super().__init__()
        self.regions = get_measures()
        self.regions_df = {}

    def get_region_predict(self, region: int, predict_params: PredictInput = None):
        if predict_params is None:
            predict_params = PredictInput()
        new_loans_volume_reg_df = self.datasource(2019, 2024, spikes_remove=False, measure_id=region)
        # определяем дату, до которой возьмем данные для обучения модели
        # Составляем прогноз
        self.dataset = new_loans_volume_reg_df
        predict_results = self.get_data_predict(predict_params)
        self.regions_df[self.regions[region]] = predict_results
        return predict_results

    def get_regions_predict(self, regions: list[int] = None, predict_params=None):
        if regions is None:
            regions = [22]
        if predict_params is None:
            predict_params = PredictInput()
        results = []
        for key, value in self.regions.items():
            # Берем данные только по федеральным округам
            if key in regions:
                if value not in self.regions_df:
                    self.regions_df[value] = self.get_region_predict(key, predict_params)
                predict, mp = self.regions_df[value].predict, self.regions_df[value].mape
                results.append((value, predict))
        return results

    def show_regions_predict(self, regions: list[int] = None, predict_params=None):
        if regions is None:
            regions = [22]
        if predict_params is None:
            predict_params = PredictInput()
        res = self.get_regions_predict(regions, predict_params)
        for elem in res:
            print(elem[0], "\n")
            print("Спрогнозированные значения:")
            print(elem[1])
            print("MAPE = ", self.regions_df[elem[0]].mape)

    def show_regions_plot(self, regions: list[int] = None, predict_params=None):
        if regions is None:
            regions = [22]
        if predict_params is None:
            predict_params = PredictInput()
        for key, value in self.regions.items():
            # Берем данные только по федеральным округам
            if key in regions:
                if value not in self.regions_df:
                    self.regions_df[value] = self.get_region_predict(key, predict_params)
                self.show_plot(
                    PredictInput(self.regions_df[value].start_date, self.regions_df[value].last_predict_date),
                    self.plot_title, value)


if __name__ == "__main__":
    predictor = LoansPredict(PredictEnum.RESIDENT_LOANS_VOLUME)
    predictor.show_regions_plot()
    predictor.show_regions_predict()
