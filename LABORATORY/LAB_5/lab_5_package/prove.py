import pandas as pd
"""
import Network

df = pd.DataFrame()
path = ['A->B', 'A->B', 'A->B', 'A->B', 'A-B->C', 'A-B->C', 'A-B->C', 'A-B->C']
df['path'] = path
df['channel'] = 1

df.loc[3, 'channel'] = 0
print(df.at[df['path'] == 'A->B->C', 'channel'])

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
"""
a = 3
if a < 2:
    b = 1
elif a < 3:
    b = 2
elif a < 4:
    b = 3
else:
    b = 4

print(b)

