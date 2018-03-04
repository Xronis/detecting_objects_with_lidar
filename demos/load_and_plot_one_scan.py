import time

import numpy as np

from data.kitti_raw_manager import load_raw_data
from plot.plot import plot_velo

drive = '0002'
frame = 0
plot = True

start_time = time.time()

data = load_raw_data(drive)
print('Number of frames: {}'.format(np.shape(data)[0]))

if plot:
    plot_velo(data[frame])

duration = time.time() - start_time

if duration > 60:
    duration = duration / 60
    print('Ends in {} minutes'.format(duration))
else:
    print('Ends in {} seconds'.format(duration))

