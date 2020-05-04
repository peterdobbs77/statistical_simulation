import pandas as pd


filepath = './data/ultimate/'
extpath = 'collegenationals_men/'
filename = 'all_reorganized.csv'

df = pd.read_csv(filepath+extpath+filename)
df["winner_seed"] = df["winner_team"].str.extract(r'(\d+)')
df["loser_seed"] = df["loser_team"].str.extract(r'(\d+)')
df.to_csv(filepath+extpath+filename, index=False)
