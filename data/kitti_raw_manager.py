import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom

import pykitti
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import data.IndividualObject as IndividualObject
from config.config import base_model_config

plotly.tools.set_credentials_file(username='panagiotidisxronis', api_key='ttur4sQ0tHGT0m7cz5XT')

cfg = base_model_config()


def load_raw_data(drive):

    basedir = cfg.basedir+drive
    date = cfg.date

    dataset = pykitti.raw(basedir, date, drive)

    velo_data = []

    for x in dataset.velo:
        velo_data.append(x)

    print('Done with {}'.format(drive))

    return velo_data


# def load_raw_tracklets(drive):
#
#     car_idx = 0
#     van_idx = 0
#     truck_idx = 0
#     pedestrian_idx = 0
#     person_idx = 0
#     cyclist_idx = 0
#     tram_idx = 0
#     misc_idx = 0
#
#     tracklets = {}
#
#     document = cfg.basedir+drive+'\\'+cfg.date+'\\tracklet_labels.xml'
#     mydoc = minidom.parse(document)
#
#     object_type = mydoc.getElementsByTagName('objectType')
#     height = mydoc.getElementsByTagName('h')
#     width = mydoc.getElementsByTagName('w')
#     length = mydoc.getElementsByTagName('l')
#     first_frame = mydoc.getElementsByTagName('first_frame')
#
#     tracklet_x = mydoc.getElementsByTagName('tx')
#     tracklet_y = mydoc.getElementsByTagName('ty')
#     tracklet_z = mydoc.getElementsByTagName('tz')
#
#     rotation_x = mydoc.getElementsByTagName('rx')
#     rotation_y = mydoc.getElementsByTagName('ry')
#     rotation_z = mydoc.getElementsByTagName('rz')
#
#     counts = mydoc.getElementsByTagName('count')
#
#     poses = mydoc.getElementsByTagName('poses')
#
#     number_of_objects_in_drive = int(counts[0].firstChild.data)
#
#     if cfg.keep_log:
#         logging.info(msg='Number of Objects in Drive {}:\t{}\n'.format(drive, number_of_objects_in_drive))
#
#     for i in range(number_of_objects_in_drive):
#
#         obj_type = object_type[i].firstChild.data
#         h = height[i].firstChild.data
#         w = width[i].firstChild.data
#         l = length[i].firstChild.data
#         first_f = int(first_frame[i].firstChild.data)
#
#         obj_poses = len(poses[i].childNodes[3].childNodes)
#
#         if cfg.keep_log:
#             logging.info(msg='Object Type:\t{}'.format(obj_type))
#             logging.info(msg='Height:\t\t\t{}'.format(h))
#             logging.info(msg='Width:\t\t\t{}'.format(w))
#             logging.info(msg='Length:\t\t\t{}'.format(l))
#             logging.info(msg='First Frame:\t{}\n'.format(first_f))
#
#         number_of_poses = int(counts[i+1].firstChild.data)
#
#         if cfg.keep_log:
#             logging.info(msg='Number of frames object appears:\t{}\n'.format(number_of_poses))
#
#         poses_dict = {}
#
#         for p in range(number_of_poses):
#
#             frame = first_f + p
#
#             tx = tracklet_x[p].childNodes[i].data
#             ty = tracklet_y[p].childNodes[i].data
#             tz = tracklet_z[p].childNodes[i].data
#
#             rx = rotation_x[p].childNodes[i].data
#             ry = rotation_y[p].childNodes[i].data
#             rz = rotation_z[p].childNodes[i].data
#
#             if cfg.keep_log:
#                 logging.info('Frame:\t{}\n'.format(frame))
#
#                 logging.info(msg='\tTracklet X:\t\t{}'.format(tx))
#                 logging.info(msg='\tTracklet Y:\t\t{}'.format(ty))
#                 logging.info(msg='\tTracklet Z:\t\t{}\n'.format(tz))
#
#                 logging.info(msg='\tRotation X:\t\t{}'.format(rx))
#                 logging.info(msg='\tRotation Y:\t\t{}'.format(ry))
#                 logging.info(msg='\tRotation Z:\t\t{}\n'.format(rz))
#
#             obj = {'height': h,
#                    'width': w,
#                    'length': l,
#                    'tracklet_x': tx,
#                    'tracklet_y': ty,
#                    'tracklet_z': tz,
#                    'rotation_x': rx,
#                    'rotation_y': ry,
#                    'rotation_z': rz}
#
#             poses_dict[frame] = obj
#
#         if obj_type.lower() == 'car':
#             obj_type = obj_type + '_' + str(car_idx)
#             car_idx += 1
#
#         elif obj_type.lower() == 'van':
#             obj_type = obj_type + '_' + str(van_idx)
#             van_idx += 1
#
#         elif obj_type.lower() == 'truck':
#             obj_type = obj_type + '_' + str(truck_idx)
#             truck_idx += 1
#
#         elif obj_type.lower() == 'pedestrian':
#             obj_type = obj_type + '_' + str(pedestrian_idx)
#             pedestrian_idx += 1
#
#         elif obj_type.lower() == 'person':
#             obj_type = obj_type + '_' + str(person_idx)
#             person_idx += 1
#
#         elif obj_type.lower() == 'cyclist':
#             obj_type = obj_type + '_' + str(cyclist_idx)
#             cyclist_idx += 1
#
#         elif obj_type.lower() == 'tram':
#             obj_type = obj_type + '_' + str(tram_idx)
#             tram_idx += 1
#
#         elif obj_type.lower() == 'misc':
#             obj_type = obj_type + '_' + str(misc_idx)
#             misc_idx += 1
#
#         tracklets[obj_type] = poses_dict
#     print('Done with {}'.format(drive))
#
#     return tracklets


def plot_velo(velo_data):
    trace = go.Scatter3d(x=velo_data[:, 0],
                         y=velo_data[:, 1],
                         z=velo_data[:, 2],
                         mode='markers',
                         marker=dict(size=3,
                                     line=dict(color='rgba(217, 217, 217, 0.14)',
                                               width=0.2),
                                     opacity=0.0))

    data = [trace]

    layout = go.Layout(
        scene=dict(
            xaxis=dict(nticks=4, range=[-100, 100], ),
            yaxis=dict(nticks=4, range=[-50, 100], ),
            zaxis=dict(nticks=4, range=[-100, 100], ), ),
        width=700,
        margin=dict(r=20, l=10, b=10, t=10)
    )
    fig = go.Figure(data=data, layout=layout)

    py.plot(fig, filename='scan')


def load_raw_tracklets(drive):

    document = cfg.basedir + drive + '\\' + cfg.date + '\\tracklet_labels.xml'
    tree = ET.parse(document)

    object_types, heights, widths, lengths, first_frames = _get_attributes_of_object(tree)

    poses = tree.findall('./tracklets/item/poses/')
    tx, ty, tz, rx, ry, rz, count = _get_attributes_of_pose(poses)

    tracklet_x, tracklet_y, tracklet_z, rotation_x, rotation_y, rotation_z = _get_all_poses(tx, ty, tz,
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


def get_objects_of_frame(frame, tracklets):

    objects_in_frame = {}

    for key in tracklets:
        if frame in tracklets[key].keys():
            objects_in_frame[key] = tracklets[key][frame]

    return objects_in_frame


def _get_attributes_of_pose(poses):
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


def _get_attributes_of_object(tree):
    object_types = _get_attribute_of_objects(tree, './tracklets/item/objectType')
    heights = _get_attribute_of_objects(tree, './tracklets/item/h')
    widths = _get_attribute_of_objects(tree, './tracklets/item/w')
    lengths = _get_attribute_of_objects(tree, './tracklets/item/l')
    first_frames = _get_attribute_of_objects(tree, './tracklets/item/first_frame')

    return object_types, heights, widths, lengths, first_frames


def _get_attribute_of_objects(tree, path):
    return _iter_through_objects(tree.findall(path))


def _iter_through_objects(elements):
    items = []

    for child in elements:
        items.append(child.text)

    return items


def _get_all_poses(tx, ty, tz, rx, ry, rz, count):
    tracklet_x = []
    tracklet_y = []
    tracklet_z = []

    rotation_x = []
    rotation_y = []
    rotation_z = []

    for i in range(len(count)):
        if i == 0:
            temp_tx, temp_ty, temp_tz, temp_rx, temp_ry, temp_rz = _poses_of_each_object(tx, ty, tz,
                                                                                         rx, ry, rz,
                                                                                         int(count[i]))
            tracklet_x.append(temp_tx)
            tracklet_y.append(temp_ty)
            tracklet_z.append(temp_tz)

            rotation_x.append(temp_rx)
            rotation_y.append(temp_ry)
            rotation_z.append(temp_rz)
        else:
            temp_tx, temp_ty, temp_tz, temp_rx, temp_ry, temp_rz = _poses_of_each_object(tx, ty, tz,
                                                                                         rx, ry, rz,
                                                                                         int(count[i]), int(count[i-1]))
            tracklet_x.append(temp_tx)
            tracklet_y.append(temp_ty)
            tracklet_z.append(temp_tz)

            rotation_x.append(temp_rx)
            rotation_y.append(temp_ry)
            rotation_z.append(temp_rz)

    return tracklet_x, tracklet_y, tracklet_z, rotation_x, rotation_y, rotation_z


def _poses_of_each_object(tx, ty, tz, rx, ry, rz, last_frame, first_frame=0):
    tracklet_x = tx[first_frame:first_frame + last_frame]
    tracklet_y = ty[first_frame:first_frame + last_frame]
    tracklet_z = tz[first_frame:first_frame + last_frame]

    rotation_x = rx[first_frame:first_frame + last_frame]
    rotation_y = ry[first_frame:first_frame + last_frame]
    rotation_z = rz[first_frame:first_frame + last_frame]

    return tracklet_x, tracklet_y, tracklet_z, rotation_x, rotation_y, rotation_z
