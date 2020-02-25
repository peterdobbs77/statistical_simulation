import pandas as pd
infilename = './data/valid.csv'
outfilename = './data/valid_plus_PIDs.csv'
df = pd.read_csv(infilename)
path = df['Path'].str.split('/', expand=True)
patientIDs = path[2].map(lambda x: x.lstrip('patient'))
df['PID'] = patientIDs
df.to_csv(outfilename, index=False)
