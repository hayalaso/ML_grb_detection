import numpy as np
import pandas as pd
import os

path = "../simulation/individual"
dfs = []
for i in range(1,3001):
    dfs.append(pd.read_csv(os.path.join(path,"{}.csv".format(i))))

df = pd.concat(dfs)
df.to_csv('../simulation/bkg.csv',index=False)
