from gbm.finder import BurstCatalog
from gbm.finder import ContinuousFtp
from gbm.finder import TriggerFtp
from gbm.data import Trigdat

import os

burstcat = BurstCatalog()
burstcat.get_table(columns=('trigger_name', 'trigger_time'))
sliced_burstcat2 = burstcat.slices([('t90',2.0,10000),('trigger_time', '2020-01-01 00:00:00', None)])
grbs=sliced_burstcat2.get_table(columns=('trigger_name','trigger_time','t90'))

trig_finder = TriggerFtp()

for g in range(20,51):

    trigname = grbs.trigger_name[g][2:]
    trigdir = os.path.join("../grbs",grbs.trigger_name[g])
    if not os.path.isdir(trigdir):
        os.mkdir(trigdir)

    trig_finder.set_trigger(trigname)

    trig_finder.get_trigdat(download_dir=trigdir)
    trig_finder.get_tte(download_dir=trigdir)#,dets=trig_dets)
    trig_finder.get_rsp2(download_dir=trigdir,ctime=False,)#dets=trig_dets)

    directory_size = 0    

    fsizedicr = {'Bytes': 1, 'Kilobytes': float(1)/1024, 'Megabytes': float(1)/(1024*1024), 'Gigabytes': float(1)/(1024*1024*1024)}

    for (path, dirs, files) in os.walk(trigdir):
        for file in files:
            try:
                filename = os.path.join(path, file.decode())
            except:
                filename = os.path.join(path,file)
            directory_size += os.path.getsize(filename)

    for key in fsizedicr:       
        print ("Folder Size: " + str(round(fsizedicr[key]*directory_size, 2)) + " " + key)

