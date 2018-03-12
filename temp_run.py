import logging
import os
import math

import tensorflow as tf
import numpy as np

from config.config import base_model_config



cfg = base_model_config()


def main(args=None):

    if tf.gfile.Exists(cfg.log_dir):
        tf.gfile.DeleteRecursively(cfg.log_dir)
    tf.gfile.MakeDirs(cfg.log_dir)

    drives = os.listdir(cfg.basedir)


if __name__ == '__main__':
    tf.app.run()
