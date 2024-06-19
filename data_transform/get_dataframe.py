import pandas as pd

df = pd.read_excel('obs_tabl20c_do_20240101.xlsx', sheet_name='Активы - всего', skiprows=1)
df.to_csv("Test.csv")
df = df.transpose()
column_names = df.columns.tolist()
for i in range(len(column_names)):
    if pd.isna(df.iloc[1][i]):
        column_names[i] = df.iloc[0][i]
    else:
        column_names[i] = df.iloc[1][i]
df.columns = column_names
df = df.reset_index()
df = df.drop(0, axis=0)
df = df.drop(1, axis=0)
df = df.reset_index()
df = df.drop('level_0', axis=1)
df.rename(columns={'index': 'Отчетный период'}, inplace=True)
df = df.dropna(axis=1, how='all')