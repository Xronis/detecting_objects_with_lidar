import logging
import os

import tensorflow as tf

from config.config import base_model_config
from data.kitti_raw_manager import load_raw_tracklets, load_raw_data
from plot.plot import plot_bounding_box, plot_velo

from plotly import graph_objs as go
import plotly.plotly as py

import plotly

plotly.tools.set_credentials_file(username='panagiotidisxronis', api_key='ttur4sQ0tHGT0m7cz5XT')

cfg = base_model_config()


def main(args=None):
    if tf.gfile.Exists(cfg.log_dir):
        tf.gfile.DeleteRecursively(cfg.log_dir)
    tf.gfile.MakeDirs(cfg.log_dir)

    if cfg.keep_log:
        logging.basicConfig(filename=cfg.log_dir+'log', level=logging.DEBUG)


if __name__ == '__main__':
    tf.app.run()
