import os
import time

import numpy as np

from data.kitti_raw_manager import load_raw_data
from config.config import base_model_config

cfg = base_model_config()


start_time = time.time()

drives = os.listdir(cfg.basedir)
total_frames = 0

for drive in drives:

    data = load_raw_data(drive)
    print(data)

    total_frames += np.shape(data)[0]
    # DO STUFF FOR EACH FILE HERE

print('Total {} frames'.format(total_frames))

duration = time.time() - start_time

if duration > 60:
    duration = duration/60
    print('Ends in {} minutes'.format(duration))
else:
    print('Ends in {} seconds'.format(duration))






