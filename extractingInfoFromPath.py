import pandas as pd
infilename = './data/train.csv'
outfilename = './data/train_plusMeta.csv'
df = pd.read_csv(infilename)
path = df['Path'].str.split('/', expand=True)
df['PID'] = path[2].map(lambda x: x.lstrip('patient'))
df['StudyID'] = path[3].map(lambda x: x.lstrip('study'))
df.to_csv(outfilename, index=False)
