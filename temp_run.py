import os

import tensorflow as tf
import numpy as np

from config.config import base_model_config
from data.kitti_raw_manager import load_raw_forward_data, get_spherical_data

import matplotlib.pyplot as plt

from PIL import Image

cfg = base_model_config()


def main(args=None):

    if tf.gfile.Exists(cfg.log_dir):
        tf.gfile.DeleteRecursively(cfg.log_dir)
    tf.gfile.MakeDirs(cfg.log_dir)

    drives = os.listdir(cfg.basedir)
    frame = load_raw_forward_data('0001')[0]

    spherical = get_spherical_data(frame)

    img = Image.fromarray(spherical, 'L')
    img.save('my.png')
    img.show()


if __name__ == '__main__':
    tf.app.run()
