import pandas as pd

df = pd.read_json('product4.json')

df.to_csv('product4.csv', index=False)