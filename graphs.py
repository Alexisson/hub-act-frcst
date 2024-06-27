import matplotlib.pyplot as plt

from parser.loans_volume_msp import get_loans_volume_msp_df

# Данные для графика

# Преобразование данных в DataFrame
df = get_loans_volume_msp_df(2015, 2023, spikes_remove=False)
df_spike_remove = get_loans_volume_msp_df(2015, 2023, spikes_remove=True)
# Вычисление минимума, максимума и медианы
min_value = df['msp_loans_volume'].min()
max_value = df['msp_loans_volume'].max()
median_value = df['msp_loans_volume'].median()

# Создание графика
plt.figure(figsize=(15, 8))
plt.plot(df['date'], df['msp_loans_volume'], marker='o', linestyle='-', color='b', label='С пиками')
plt.plot(df_spike_remove['date'], df_spike_remove['msp_loans_volume'], marker='o', linestyle='-', color='r', label='Убраны пики')

# Добавление линий минимума, максимума и медианы
plt.axhline(y=min_value, color='r', linestyle='--', label=f'Минимум: {min_value}')
plt.axhline(y=max_value, color='g', linestyle='--', label=f'Максимум: {max_value}')
plt.axhline(y=median_value, color='orange', linestyle='--', label=f'Медиана: {median_value}')

# Настройка осей и заголовка
plt.xlabel('date')
plt.ylabel('msp_loans_volume')
plt.title('Объем задолженностей')
plt.xticks(rotation=90)
plt.grid(True)
plt.legend()

# Отображение графика
plt.tight_layout()
plt.show()
