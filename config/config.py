from easydict import EasyDict as edict


def base_model_config():

    cfg = edict()

    cfg.log_dir = './log/'
    cfg.basedir = 'E:\Documents\KITTI\Raw\\'
    cfg.date = '2011_09_26'

    cfg.keep_log = True

    return cfg
