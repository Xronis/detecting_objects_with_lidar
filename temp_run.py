import logging

import tensorflow as tf

from config.config import base_model_config
from demos.loading_tracklets import load_single_tracklet
from demos.loading_velo_data import loading_one_velo_data
from demos.plotting_data import plot_scan
from demos.get_all_objects_in_frame import get_trackelts_in_frame

cfg = base_model_config()


def main(args=None):
    if tf.gfile.Exists(cfg.log_dir):
        tf.gfile.DeleteRecursively(cfg.log_dir)
    tf.gfile.MakeDirs(cfg.log_dir)

    if cfg.keep_log:
        logging.basicConfig(filename=cfg.log_dir+'log', level=logging.DEBUG)

    # # data = loading_one_velo_data('0001')
    # # plot_scan(data[0])
    #
    # tracklets = load_single_tracklet('0002')
    # # print(tracklets)
    #
    # for key in tracklets:
    #     print(tracklets[key])
    # print()
    #
    # objects = get_trackelts_in_frame(0, tracklets)
    #
    # for key in objects:
    #     print(objects[key])

    tracklets = load_single_tracklet('0002')

    for tracklet in tracklets:
        tracklet.__str__()


if __name__ == '__main__':
    tf.app.run()
