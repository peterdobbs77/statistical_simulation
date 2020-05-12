import pandas as pd

df = pd.read_csv(f'./data/ultimate/archives/open_college_archive_scraped.csv')
df['Team'] = df['Team'].str.strip()
df.to_csv(f'./data/ultimate/archives/open_college_archive_scraped.csv', index=False)
