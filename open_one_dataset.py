import functions.file_read as f
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import functions.fit_scurve as fsc
import sys

# path of the master file (.json or .raw)
fpath = '../raw_data_SinglephotoncountingpixeldetectorforsoftX-rays/data/W0/vthrscan_W0G_E4000_150V_vrpre3400_vrsh1400_exptime1000ms_master_1.json'

# min-max-step can be found in the master file
minV = 0
maxV = 2001
step = 20 
vthreshold = np.arange(minV, maxV, step)

data = f.file_read(fpath)
frames = np.shape(data)[0]
print('Number of frames:', frames)

fig1, sub1 = plt.subplots()
im = sub1.imshow(data[20] , norm=LogNorm(vmin=0.1, vmax=100000), interpolation=None)
fig1.colorbar(im)
sub1.set(title='Single frame', xlabel='Pixel x', ylabel='Pixel y')
fig1.show()

# plot and fit scurve of one pixel
pixy = 115
pixx = 190
one_pix = data[:, pixy, pixx]

fit_results = fsc.fit_scurve_func(vthreshold, one_pix, 1, -1, 1000)
scurve_plot = list(map(lambda th:fsc.scurve(th,*fit_results[:6], -1), vthreshold))
print('Inflection point:', fit_results[2])
print('Noise:', fit_results[3])
print('Amplitude:', fit_results[4])

fig2, sub2 = plt.subplots()
sub2.plot(vthreshold, one_pix, label='data', linestyle='none', marker='.',)
sub2.set(title='Threshold scan - one pixel', xlabel='vthreshold (DACu)', ylabel='Counts')
sub2.plot(vthreshold, scurve_plot, '-', label='Fit')
sub2.legend()
fig2.show(1)