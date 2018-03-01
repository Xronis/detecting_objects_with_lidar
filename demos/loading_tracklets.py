import time
import os
import logging

from config.config import base_model_config
from data.kitti_raw_manager import load_raw_tracklets, load_raw_tracklets_v2

cfg = base_model_config()


def loading_tracklets():
    start_time = time.time()

    drives = os.listdir(cfg.basedir)

    for drive in drives:
        logging.info(msg=load_raw_tracklets(drive))

    duration = time.time() - start_time

    if duration > 60:
        duration = duration / 60
        print('Ends in {} minutes'.format(duration))
    else:
        print('Ends in {} seconds'.format(duration))


def load_single_tracklet(drive):
    start_time = time.time()

    # tracklets = load_raw_tracklets(drive)
    tracklets = load_raw_tracklets_v2(drive)

    duration = time.time() - start_time

    if duration > 60:
        duration = duration / 60
        print('Ends in {} minutes'.format(duration))
    else:
        print('Ends in {} seconds'.format(duration))

    return tracklets