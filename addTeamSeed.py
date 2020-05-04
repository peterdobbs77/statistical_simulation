import pandas as pd


filepath = './data/ultimate/'
extpath = 'CollegeSeries/'
filename = 'open_nc_region_allgames.csv'

df = pd.read_csv(filepath+extpath+filename)
df["home_seed"] = df["home_team"].str.extract(r'(\d+)')
df["away_seed"] = df["away_team"].str.extract(r'(\d+)')
df.to_csv(filepath+extpath+filename, index=False)
