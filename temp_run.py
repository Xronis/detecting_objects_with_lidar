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

    bll = np.array([23.08612957107574, 9.547677019518012, -1.7921571450416216])
    blr = np.array([23.013475461893403, 7.843513258291362, -1.7921571450416216])
    bul = np.array([23.08612957107574, 9.547677019518012, 0.37507775495837836])
    bur = np.array([23.013475461893403, 7.843513258291362, 0.37507775495837836])

    fll = np.array([27.41155661301912, 9.363269830657602, -1.7921571450416216])
    flr = np.array([27.33890250383678, 7.659106069430952, -1.7921571450416216])
    ful = np.array([27.41155661301912, 9.363269830657602, 0.37507775495837836])
    fur = np.array([27.33890250383678, 7.659106069430952, 0.37507775495837836])

    point_inside = np.array([23.515, 9.037, -0.602])

    cond = np.array([point_inside[0] >= bll[0], point_inside[1] <= bll[1], point_inside[2] >= bll[2],
                     point_inside[0] >= blr[0], point_inside[1] >= blr[1],
                     point_inside[2] <= bul[2],
                     point_inside[0] <= fll[0], point_inside[1] <= fll[1],
                     point_inside[0] < flr[0], point_inside[1] >= flr[1]])

    if cond.all():
        print('hey')


if __name__ == '__main__':
    tf.app.run()
