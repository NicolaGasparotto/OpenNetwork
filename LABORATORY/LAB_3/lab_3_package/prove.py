import pandas as pd

import Network

df = pd.DataFrame()
path = ['A->B', 'A->B', 'A->B', 'A->B', 'A-B->C', 'A-B->C', 'A-B->C', 'A-B->C']
df['path'] = path
df['channel'] = 1

df.loc[3,'channel'] = 0

df1 = df.copy()

for k in range(4):
    UPDATED = 0
    indexes = []
    start = path[0]
    for i in df.index:
        if df.at[i, 'path'] == start:
            if not UPDATED:
                UPDATED = 1
                indexes.append(i)
        else:
            start = df.at[i, 'path']
            indexes.append(i)
    #print(indexes)
    df1.loc[indexes, 'channel'] = 0
    df = df.drop(indexes)
    print(df1)
