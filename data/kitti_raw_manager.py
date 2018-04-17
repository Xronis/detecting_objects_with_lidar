import xml.etree.ElementTree as ET

import pykitti
import plotly
import numpy as np

import data.IndividualObject as IndividualObject
from config.config import base_model_config


cfg = base_model_config()

index = 0


def load_raw_data(drive):

    basedir = cfg.basedir+drive
    date = cfg.date

    dataset = pykitti.raw(basedir, date, drive)

    velo_data = []

    for x in dataset.velo:
        velo_data.append(x)

    return velo_data


def load_raw_forward_data(drive, one_out_of=None, y_threshold=None):
    basedir = cfg.basedir+drive
    date = cfg.date

    dataset = pykitti.raw(basedir, date, drive)

    return [_get_points_with_threshold(frame, y_threshold, one_out_of) for frame in dataset.velo]


def get_spherical_data(frame):
    spherical_frame = []
    spherical_data = []
    # for frame in scan:
    for x, y, z, r in frame:
        radial_distance = np.sqrt(np.power(x, 2) + np.power(y, 2) + np.power(z, 2))

        if z != 0:
            theta = np.arctan(np.sqrt(np.power(x, 2) + np.power(y, 2)) / z)
        else:
            theta = np.arctan(np.sqrt(np.power(x, 2) + np.power(y, 2)))

        if x != 0:
            phi = np.arctan(y / x)
        else:
            phi = np.arctan(y)

        spherical_frame.append([radial_distance, phi, theta, r])
        # spherical_data.append(spherical_frame)

    return np.array(spherical_frame)


def load_single_tracklet(drive):
    return load_raw_tracklets(drive)


def load_raw_tracklets(drive):
    global index

    index = 0

    document = cfg.basedir + drive + '\\' + cfg.date + '\\tracklet_labels.xml'
    tree = ET.parse(document)

    object_types, heights, widths, lengths, first_frames = _get_attributes_of_object_from_file(tree)

    poses = tree.findall('./tracklets/item/poses/')
    tx, ty, tz, rx, ry, rz, count = _get_attributes_of_pose_from_file(poses)

    tracklet_x, tracklet_y, tracklet_z, rotation_x, rotation_y, rotation_z = _get_all_poses_from_file(tx, ty, tz,
                                                                                                      rx, ry, rz,
                                                                                                      count)

    tracklets = []

    for i in range(len(object_types)):
        tracklets.append(IndividualObject.IndividualObject(object_types[i],
                                                           heights[i],
                                                           widths[i],
                                                           lengths[i],
                                                           int(first_frames[i]),
                                                           tracklet_x[i],
                                                           tracklet_y[i],
                                                           tracklet_z[i],
                                                           rotation_x[i],
                                                           rotation_y[i],
                                                           rotation_z[i],
                                                           int(count[i])))

    return tracklets


def _get_attributes_of_pose_from_file(poses):
    count = []

    tx = []
    ty = []
    tz = []

    rx = []
    ry = []
    rz = []

    for child in poses:
        if child.tag == 'item':
            for c in child:
                if c.tag == 'tx':
                    tx.append(c.text)

                elif c.tag == 'ty':
                    ty.append(c.text)

                elif c.tag == 'tz':
                    tz.append(c.text)

                elif c.tag == 'rx':
                    rx.append(c.text)

                elif c.tag == 'ry':
                    ry.append(c.text)

                elif c.tag == 'rz':
                    rz.append(c.text)

        elif child.tag == 'count':
            count.append(child.text)

    return tx, ty, tz, rx, ry, rz, count


def _get_attributes_of_object_from_file(tree):
    object_types = _get_attribute_of_objects_from_file(tree, './tracklets/item/objectType')
    heights = _get_attribute_of_objects_from_file(tree, './tracklets/item/h')
    widths = _get_attribute_of_objects_from_file(tree, './tracklets/item/w')
    lengths = _get_attribute_of_objects_from_file(tree, './tracklets/item/l')
    first_frames = _get_attribute_of_objects_from_file(tree, './tracklets/item/first_frame')

    return object_types, heights, widths, lengths, first_frames


def _get_attribute_of_objects_from_file(tree, path):
    return _iter_through_objects(tree.findall(path))


def _iter_through_objects(elements):
    items = []

    for child in elements:
        items.append(child.text)

    return items


def _get_all_poses_from_file(tx, ty, tz, rx, ry, rz, count):
    global index

    tracklet_x = []
    tracklet_y = []
    tracklet_z = []

    rotation_x = []
    rotation_y = []
    rotation_z = []

    for i in range(len(count)):
        temp_tx, temp_ty, temp_tz, temp_rx, temp_ry, temp_rz = _poses_of_each_object_from_file(tx, ty, tz,
                                                                                               rx, ry, rz,
                                                                                               int(count[i]), index)

        tracklet_x.append(temp_tx)
        tracklet_y.append(temp_ty)
        tracklet_z.append(temp_tz)

        rotation_x.append(temp_rx)
        rotation_y.append(temp_ry)
        rotation_z.append(temp_rz)

    return tracklet_x, tracklet_y, tracklet_z, rotation_x, rotation_y, rotation_z


def _poses_of_each_object_from_file(tx, ty, tz, rx, ry, rz, last_frame, first_frame=0):
    global index

    index = first_frame + last_frame

    tracklet_x = tx[first_frame:index]
    tracklet_y = ty[first_frame:index]
    tracklet_z = tz[first_frame:index]

    rotation_x = rx[first_frame:index]
    rotation_y = ry[first_frame:index]
    rotation_z = rz[first_frame:index]

    return tracklet_x, tracklet_y, tracklet_z, rotation_x, rotation_y, rotation_z


def _downscale_scan(array_to_scale, one_out_of):

    ret = []

    for i in range(len(array_to_scale)):
        if i % one_out_of == 0:
            ret.append(array_to_scale[i])

    return np.asarray(ret)


def _get_points_with_threshold(frame, y_threshold=None, one_out_of=None):
    over_x_0 = frame[frame[:, 0] > 0]

    if y_threshold:
        under_y_threshold = over_x_0[over_x_0[:, 1] < y_threshold]
        over_y_threshold = under_y_threshold[under_y_threshold[:, 1] > -y_threshold]

        if one_out_of:
            return _downscale_scan(over_y_threshold, one_out_of)
        else:
            return over_y_threshold
    else:
        if one_out_of:
            return _downscale_scan(over_x_0, one_out_of)
        else:
            return over_x_0
