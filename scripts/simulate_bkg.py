from gbm.data import TTE,RSP
from gbm.binning.unbinned import bin_by_time
from gbm.background import BackgroundFitter
from gbm.background.binned import Polynomial

#simulators
from gbm.simulate import TteSourceSimulator, TteBackgroundSimulator
from gbm.simulate.profiles import constant, norris, quadratic
from gbm.spectra.functions import Band

import pandas as pd
import numpy as np
import argparse

p = argparse.ArgumentParser(description='Simple Bkg simulator for GBM')
p.add_argument("-o","--outputname",dest='outname',
                help="Output name",required=True)
args = p.parse_args()




## open a TTE file and response
tte = TTE.open('../grbs/bn170817908/glg_tte_n0_bn170817908_v00.fit')
rsp = RSP.open('../grbs/bn170817908/glg_cspec_n0_bn170817908_v01.rsp2')

tte = tte.slice_time([-50.0, 100.0])

# bin to 1.024 s resolution, reference time is trigger time
phaii = tte.to_phaii(bin_by_time, 1.024, time_ref=0.0)

bkgd_times = [(-20.0, -5.0), (20.0, 100.0)]
backfitter = BackgroundFitter.from_phaii(phaii, Polynomial, time_ranges=bkgd_times)

backfitter.fit(order=2)
bkgd = backfitter.interpolate_bins(phaii.data.tstart, phaii.data.tstop)

select_time = (20.0, 100.0)
spec_bkgd = bkgd.integrate_time(*select_time)

constant_params = (1.1,)
tte_sim = TteBackgroundSimulator(spec_bkgd, 'Gaussian', constant, constant_params)
tte_bkgd = tte_sim.to_tte(-50.0,100.0)

phaii = tte_bkgd.to_phaii(bin_by_time, 1.024)
lc=phaii.to_lightcurve(energy_range=(8.0, 900.0))
df = pd.DataFrame(np.reshape(lc.counts,(1,len(lc.counts))))


print(args.outname)
df.to_csv(args.outname,index=False)

