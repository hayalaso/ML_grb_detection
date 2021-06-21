import pandas as pd
import os, fnmatch
import numpy as np
from gbm.data import TTE
from gbm.binning.unbinned import bin_by_time

path='../grbs'

directories = os.listdir(path)

erange = (8.0, 900.0)
frames=[]
print(directories)
for d in directories:
    files=fnmatch.filter(os.listdir(os.path.join(path,d)),'*tte*')
    print(files)
    for f in files:
        tte = TTE.open(os.path.join(path,d,f))
        tte = tte.slice_time([-50.0, 100.0])
        # bin to 1.024 s resolution, reference time is trigger time
        phaii = tte.to_phaii(bin_by_time, 1.024, time_ref=0.0)

        lc = phaii.to_lightcurve(energy_range=erange)
        tempdf = pd.DataFrame(np.reshape(lc.counts,(1,len(lc.counts))))
        name=f[8:22]
        tempdf['name']=name
        frames.append(tempdf)

df=pd.concat(frames,ignore_index=True)
df.to_csv('../simulation/grbs.csv',index=False)
