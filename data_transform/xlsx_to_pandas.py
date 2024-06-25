import pandas as pd

df = pd.read_excel('parser/files/A_Debt_corp_by_activity/01_02_A_Debt_corp_by_activity.xlsx-01_45.xlsx',
                   sheet_name='Таблица 1', skiprows=2)
df.to_csv("Test.csv")
replace_text = ' '
for i in range(1, len(df.columns)):
    if df.columns[i] == 'Unnamed: ' + str(i):
        if count == 0:
            replace_text = df.columns.values[i - 1]
            df.columns.values[i - 1] = df.columns.values[i - 1] + '<>' + df.iloc[0][i - 1]
        df.columns.values[i] = replace_text + '<>' + df.iloc[0][i]
        count += 1
    else:
        count = 0

df = df.drop(0, axis=0)
