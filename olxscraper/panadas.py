import pandas as pd

obj=pd.read_json('output.json',orient='values')
obj.to_csv('output.csv')