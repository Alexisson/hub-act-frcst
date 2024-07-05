from enum import Enum

from dataframes.loans_volume_msp import get_loans_volume_msp_df
from dataframes.new_loans_msp import get_new_loans_msp_df
from dataframes.resident_loans_volume import get_resident_loans_volume_df
from dataframes.resident_new_loans import get_new_loans_resident_df
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
            self.__datasource = get_new_loans_msp_df
            self.plot_title = "Объем выданных кредитов МСП"
        elif datasource == PredictEnum.MSP_LOANS_VOLUME:
            self.__datasource = get_loans_volume_msp_df
            self.plot_title = "Задолженность по кредитам МСП"
        elif datasource == PredictEnum.RESIDENT_NEW_LOANS:
            self.__datasource = get_new_loans_resident_df
            self.plot_title = "Объем выданных кредитов резиденты"
        elif datasource == PredictEnum.RESIDENT_LOANS_VOLUME:
            self.__datasource = get_resident_loans_volume_df
            self.plot_title = "Задолженность по кредитам резиденты"
        super().__init__()
        self.regions = get_measures()
        self.__regions_df = {}

    def get_region_predict(self, region: int, predict_params: PredictInput = None):
        if predict_params is None:
            predict_params = PredictInput()
        new_loans_volume_reg_df = self.__datasource(2019, 2024, spikes_remove=False, measure_id=region)
        # определяем дату, до которой возьмем данные для обучения модели
        # Составляем прогноз
        self.dataset = new_loans_volume_reg_df
        if region == 106 and self.__datasource == get_new_loans_resident_df:
            c_df = self.dataset.copy()
            c_df.at[23, 'resident_loans_volume'] = c_df.at[23, 'resident_loans_volume'] / 1.5
            self.dataset = c_df.copy()
        if region == 42 and self.__datasource == get_new_loans_msp_df:
            c_df = self.dataset.copy()
            c_df.at[45, 'msp_loans'] = c_df.at[45, 'msp_loans'] / 1.5
            self.dataset = c_df.copy()
        predict_results = self.get_data_predict(predict_params)
        self.__regions_df[self.regions[region]] = predict_results
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
                if value not in self.__regions_df:
                    self.__regions_df[value] = self.get_region_predict(key, predict_params)
                results.append((value, self.__regions_df[value]))
        return results

    def show_regions_predict(self, regions: list[int] = None, predict_params=None):
        if regions is None:
            regions = [22]
        if predict_params is None:
            predict_params = PredictInput()
        res = self.get_regions_predict(regions, predict_params)
        result = []
        for elem in res:
            print(elem[0], "\n")
            result.append(elem[0])
            print("Спрогнозированные значения:")
            print(elem[1])
            print("MAPE = ", self.__regions_df[elem[0]].mape)
        return result

    def show_regions_plot(self, regions: list[int] = None, predict_params=None):
        if regions is None:
            regions = [22]
        if predict_params is None:
            predict_params = PredictInput()
        res = self.get_regions_predict(regions, predict_params)
        for elem in res:
            self.dataset = self.__datasource(2019, 2024, spikes_remove=False, measure_id=list(self.regions.keys())[list(self.regions.values()).index(elem[0])])
            self.show_plot(elem[1].predict, predict_params, name=elem[0], plt_title=self.plot_title)


if __name__ == "__main__":
    predictor = LoansPredict(PredictEnum.MSP_LOANS_VOLUME)
    predictor.get_regions_predict([23, 24, 29], PredictInput(start_date='2023-06', custom=True, season_ord=(1, 1, 0, 12),
                                                     custom_pdq=(1, 0, 2), trend='ct'))
    predictor.show_regions_plot([23, 24, 29], PredictInput(start_date='2023-06', custom=True, season_ord=(1, 1, 0, 12),
                                                   custom_pdq=(1, 0, 2), trend='ct'))
