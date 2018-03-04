import os
import time
import threading
import multiprocessing

from config.config import base_model_config
from data.kitti_raw_manager import load_raw_tracklets


cfg = base_model_config()
drives = os.listdir(cfg.basedir)

total_duration = 0


for drive in drives:
    start_time = time.time()
    tracklets = load_raw_tracklets(drive)

    print('----------------------------------------- DRIVE {} --------------------------------------'.format(drive))

    for tracklet in tracklets:
        pose = tracklet.get_pose_of_frame(0)

        if pose is not None:
            pose.__str__()

    total_duration += time.time() - start_time
    print()


print('{} sec'.format(total_duration))

