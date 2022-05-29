import pandas as pd


data = {'path': ['A->B', 'A->B->C', 'B->C', 'B->C->D', 'C->D']}
df = pd.DataFrame(data)
df = df.loc[df.index.repeat(3)].reset_index(
            drop=True)  # without the drop=Ture it will maintain also the old indexes
df['channel state'] = 1  # setting all the channel as free -> value 1

df.loc[0, 'channel state'] = 0  # ab.1
df.loc[3, 'channel state'] = 0  # ab.1
df.loc[4, 'channel state'] = 0  # abc.1 -abc
df.loc[7, 'channel state'] = 0  # abc.1 -bc
df.loc[1, 'channel state'] = 0  # abc.1 -ab
df.loc[10, 'channel state'] = 0 # abc.1 -bc
print(df)

print((df.loc[(df['path'] == 'A->B->C') & (df['channel state'] == 1)].index[0]) % 3)
# facendone il modulo ottengo il numero del canale -> i channel si contano da 0

indexes = [i for i in df.index if (i % 3) == 2]
df = df.drop(indexes)
print(df)
"""
given_path = 'A->B->C'
paths = [given_path[i*3:i*3+4] for i in range(int(len(given_path)/3))]  ################################################
# print(int(len(given_path)/3))
print([path.replace('->', '') for path in paths])
# selected_path = df.loc[(df['path'].str.contains('AB')) | (df['path'].str.contains('BC'))]
selected_path = df.loc[df['path'].apply(lambda x: True if any(i in x for i in paths) else False)]  #####################
print(selected_path)
"""

