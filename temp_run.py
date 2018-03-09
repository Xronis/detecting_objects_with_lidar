import logging
import os
import math

import tensorflow as tf
import numpy as np
import vpython as vpy

from config.config import base_model_config
from data.kitti_raw_manager import load_raw_tracklets, load_raw_data
from plot.plot import plot_bounding_box, plot_velo


cfg = base_model_config()


def main(args=None):
    if tf.gfile.Exists(cfg.log_dir):
        tf.gfile.DeleteRecursively(cfg.log_dir)
    tf.gfile.MakeDirs(cfg.log_dir)

    if cfg.keep_log:
        logging.basicConfig(filename=cfg.log_dir+'log', level=logging.DEBUG)


if __name__ == '__main__':
    tf.app.run()
