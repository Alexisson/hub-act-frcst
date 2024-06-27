import datetime
import matplotlib.pyplot as plt

from parser.bal import get_bal_df
from parser.bal_increase import get_bal_increase_df
from parser.broad_money_supply import get_broad_money_supply
from parser.capital_transfers import get_capital_transfers
from parser.direct_investments import get_direct_investments
from parser.dollar import get_dollar_df
from parser.gdp import get_gdp_on_2021_prices_dataframe
from parser.inflation import get_inflation_df
from parser.loans_volume_msp import get_loans_volume_msp_df


# Данные для графика
def make_graphs(df, df_spike_remove):
    # Преобразование данных в DataFrame

    # Вычисление минимума, максимума и медианы
    min_value = df[df.columns[1]].min()
    max_value = df[df.columns[1]].max()
    median_value = df[df.columns[1]].median()

    # Создание графика
    plt.figure(figsize=(15, 8))
    plt.plot(df['date'], df[df.columns[1]], marker='o', linestyle='-', color='b', label='С пиками', markersize=3)
    plt.plot(df_spike_remove['date'], df_spike_remove[df.columns[1]], marker='o', linestyle='-', color='r',
             label='Убраны пики', markersize=3)

    # Добавление линий минимума, максимума и медианы
    plt.axhline(y=min_value, color='r', linestyle='--', label=f'Минимум: {min_value}')
    plt.axhline(y=max_value, color='g', linestyle='--', label=f'Максимум: {max_value}')
    plt.axhline(y=median_value, color='orange', linestyle='--', label=f'Медиана: {median_value}')

    # Настройка осей и заголовка
    plt.xlabel('date')
    plt.ylabel(df.columns[1])
    plt.title('Объем задолженностей')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.legend()

    # Отображение графика
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Влияет неплохо, параметры 3 и 2 норм
    # df = get_loans_volume_msp_df(2015, 2023, spikes_remove=False)
    # df_spike_remove = get_loans_volume_msp_df(2015, 2023, spikes_remove=True)

    # Не влияет никак, пики не убирает, все параметры пробовал
    # df = get_bal_df(spikes_remove=False)
    # df_spike_remove = get_bal_df(window_size=3, sigma=2)

    # Пики убирает, параметры стандартные
    # df = get_bal_increase_df(spikes_remove=False)
    # df_spike_remove = get_bal_increase_df()

    # get_broad_money_supply
    # Пики небольшие, убираются
    # df = get_broad_money_supply(2019, 2024, spikes_remove=False)
    # df_spike_remove = get_broad_money_supply(2019, 2024)

    # get_capital_transfers
    # Пики странно убираются, но вроде норм. Там просто какой-то провал лютый
    # df = get_capital_transfers(2019, 2024, spikes_remove=False)
    # df_spike_remove = get_capital_transfers(2019, 2024, window_size=5, sigma=0.6)

    # get_direct_investments
    # Пики убрались, возможно сильно, тогда стоит увеличить sigma
    # df = get_direct_investments(2019, 2024, spikes_remove=False)
    # df_spike_remove = get_direct_investments(2019, 2024,  window_size=5, sigma=0.35)

    # get_dollar_df
    # Пик 2022.02 убран
    # start_date = datetime.datetime.strptime("01.01.2015", "%d.%m.%Y")
    # end_date = datetime.datetime.now()
    # df = get_dollar_df(start_date, end_date, spikes_remove=False)
    # df_spike_remove = get_dollar_df(start_date, end_date)

    # get_gdp_on_2021_prices_dataframe
    # Все в сезонных пиках, убирать смысла нет
    # df = get_gdp_on_2021_prices_dataframe()
    # df_spike_remove = get_gdp_on_2021_prices_dataframe(window_size=15, sigma=0.5, spikes_remove=False)

    # get_inflation_df
    # Пик 2022.02 сгладился, если надо сгладить сильнее, то sigma уменьшить
    start_date = datetime.datetime.strptime("01.01.2015", "%d.%m.%Y")
    end_date = datetime.datetime.now()
    df = get_inflation_df(start_date, end_date, spikes_remove=False)
    df_spike_remove = get_inflation_df(start_date, end_date, window_size=70, sigma=0.1)

    make_graphs(df, df_spike_remove)
