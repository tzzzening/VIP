import pandas as pd

data = pd.DataFrame({'data': ['hello', 'bye'], 'haha': [1, 2]})
data_to_excel = pd.ExcelWriter('for_fun.xlsx', engine='xlsxwriter')
data.to_excel(data_to_excel, sheet_name='Sheet1')
data_to_excel.save()