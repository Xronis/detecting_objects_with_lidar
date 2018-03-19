import math

import numpy as np
from plotly import graph_objs as go
import plotly.plotly as py

import plotly

from data.kitti_raw_manager import load_raw_tracklets, load_raw_forward_data

plotly.tools.set_credentials_file(username='panagiotidisxronis', api_key='ttur4sQ0tHGT0m7cz5XT')


def plot_scan_with_bbox(drive, frame, y_threshold, one_out_of):
    bounding_boxes = {}
    bb_index = 0

    for d in drive:
        tracklets = load_raw_tracklets(d)

        bbox_traces = []

        if y_threshold and one_out_of:
            data = load_raw_forward_data(d, y_threshold=y_threshold)
        else:
            data = load_raw_forward_data(d)

        for tracklet in tracklets:
            if frame in tracklet.frames:

                pose = tracklet.get_pose_of_frame(frame)

                front_lower_left_corner, front_lower_right_corner, \
                front_upper_left_corner, front_upper_right_corner, \
                back_lower_left_corner, back_lower_right_corner, \
                back_upper_left_corner, back_upper_right_corner = pose.get_corners_of_bounding_box(tracklet.height,
                                                                                                   tracklet.width,
                                                                                                   tracklet.length)

                if not y_threshold:
                    threshold = np.inf
                else:
                    threshold = y_threshold

                inside_y_bounds = np.array([front_lower_left_corner['y'] > -threshold,
                                            front_lower_left_corner['y'] < threshold,
                                            front_lower_right_corner['y'] > -threshold,
                                            front_lower_right_corner['y'] < threshold,
                                            front_upper_left_corner['y'] > -threshold,
                                            front_upper_left_corner['y'] < threshold,
                                            front_upper_right_corner['y'] > -threshold,
                                            front_upper_right_corner['y'] < threshold,
                                            back_lower_left_corner['y'] > -threshold,
                                            back_lower_left_corner['y'] < threshold,
                                            back_lower_right_corner['y'] > -threshold,
                                            back_lower_right_corner['y'] < threshold,
                                            back_upper_left_corner['y'] > -threshold,
                                            back_upper_left_corner['y'] < threshold,
                                            back_upper_right_corner['y'] > -threshold,
                                            back_upper_right_corner['y'] < threshold
                                            ])

                if inside_y_bounds.all():
                    bbox = _plot_bounding_box(front_lower_left_corner, front_lower_right_corner,
                                              front_upper_left_corner, front_upper_right_corner,
                                              back_lower_left_corner, back_lower_right_corner,
                                              back_upper_left_corner, back_upper_right_corner)

                    bounding_box = {'fll': front_lower_left_corner,
                                    'flr': front_lower_right_corner,
                                    'ful': front_upper_left_corner,
                                    'fur': front_upper_right_corner,
                                    'bll': back_lower_left_corner,
                                    'blr': back_lower_right_corner,
                                    'bul': back_upper_left_corner,
                                    'bur': back_upper_right_corner}

                    bounding_boxes['bb'+str(bb_index)] = bounding_box
                    bb_index += 1

                    # if one_out_of:
                    #     if _bbox_has_point(data[frame], front_lower_left_corner, front_lower_right_corner, back_lower_left_corner,
                    #                        back_lower_right_corner, back_upper_left_corner):
                    #         for b in bbox:
                    #             bbox_traces.append(b)
                    # else:
                    #     for b in bbox:
                    #         bbox_traces.append(b)

                    for b in bbox:
                        bbox_traces.append(b)

        if one_out_of:
            scan = _get_sparse_scan(data[frame], bounding_boxes, one_out_of)
        else:
            scan = data[frame]

        scan_traces = _plot_velo(scan)

        layout = go.Layout(
            scene=dict(
                xaxis=dict(nticks=4, range=[-100, 100], ),
                yaxis=dict(nticks=4, range=[-50, 100], ),
                zaxis=dict(nticks=4, range=[-100, 100], ),
                aspectratio=dict(x=1, y=1, z=1)),
            margin=dict(r=0, l=0, b=0, t=0)
        )

        fig_data = [scan_traces[0]]

        for bb in bbox_traces:
            fig_data.append(bb)

        fig = go.Figure(data=fig_data, layout=layout)
        # py.plot(fig, filename='scan_with_tracklet_{}'.format(d))
        plotly.offline.plot(fig, filename='scan_with_tracklet_{}'.format(d))


def plot_points(points):
    trace = go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode='markers',
        marker=dict(size=3,
                    line=dict(color='rgba(217, 217, 217, 0.14)',
                              width=0.2),
                    opacity=0.0)
    )

    data = [trace]
    layout = go.Layout(
            scene=dict(
                xaxis=dict(nticks=4, range=[-100, 100], ),
                yaxis=dict(nticks=4, range=[-50, 100], ),
                zaxis=dict(nticks=4, range=[-100, 100], ),
                aspectratio=dict(x=1, y=1, z=1)),
            margin=dict(r=0, l=0, b=0, t=0)
        )
    fig = go.Figure(data=data, layout=layout)
    # py.iplot(fig, filename='simple-3d-scatter')
    plotly.offline.plot(fig, filename='scan_with_tracklet')


def _plot_velo(velo_data):
    trace = go.Scatter3d(x=velo_data[:, 0],
                         y=velo_data[:, 1],
                         z=velo_data[:, 2],
                         mode='markers',
                         marker=dict(size=3,
                                     line=dict(color='rgba(217, 217, 217, 0.14)',
                                               width=0.2),
                                     opacity=0.0))

    return [trace]


def _plot_bounding_box(front_lower_left_corner, front_lower_right_corner,
                       front_upper_left_corner, front_upper_right_corner,
                       back_lower_left_corner, back_lower_right_corner,
                       back_upper_left_corner, back_upper_right_corner):

    x = [front_lower_left_corner['x'], front_lower_right_corner['x'],
         back_lower_left_corner['x'], back_lower_right_corner['x'],
         front_upper_left_corner['x'], front_upper_right_corner['x'],
         back_upper_left_corner['x'], back_upper_right_corner['x']]

    y = [front_lower_left_corner['y'], front_lower_right_corner['y'],
         back_lower_left_corner['y'], back_lower_right_corner['y'],
         front_upper_left_corner['y'], front_upper_right_corner['y'],
         back_upper_left_corner['y'], back_upper_right_corner['y']]

    z = [front_lower_left_corner['z'], front_lower_right_corner['z'],
         back_lower_left_corner['z'], back_lower_right_corner['z'],
         front_upper_left_corner['z'], front_upper_right_corner['z'],
         back_upper_left_corner['z'], back_upper_right_corner['z']]

    pairs = [(0, 1), (1, 3), (3, 2), (2, 0), (4, 5), (5, 7), (7, 6), (6, 4), (2, 6), (4, 0), (3, 7), (5, 1)]

    trace1 = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(size=3,
                    line=dict(color='rgba(255, 152, 0, 1)',
                              width=0.2),
                    opacity=0.0)
    )

    x_lines = list()
    y_lines = list()
    z_lines = list()

    # create the coordinate list for the lines
    for p in pairs:
        for i in range(2):
            x_lines.append(x[p[i]])
            y_lines.append(y[p[i]])
            z_lines.append(z[p[i]])
        x_lines.append(None)
        y_lines.append(None)
        z_lines.append(None)

    trace2 = go.Scatter3d(
        x=x_lines,
        y=y_lines,
        z=z_lines,
        mode='lines'
    )

    return [trace1, trace2]


def _bbox_has_point(scan, front_lower_left_corner, front_lower_right_corner, back_lower_left_corner,
                    back_lower_right_corner, back_upper_left_corner):

    for i in range(len(scan)):
        point = scan[i]

        cond = np.array([point[0] >= back_lower_left_corner['x'], point[1] <= back_lower_left_corner['y'], point[2] >= back_lower_left_corner['z'],
                         point[0] >= back_lower_right_corner['x'], point[1] >= back_lower_right_corner['y'],
                         point[2] <= back_upper_left_corner['z'],
                         point[0] <= front_lower_left_corner['x'], point[1] <= front_lower_left_corner['y'],
                         point[0] < front_lower_right_corner['x'], point[1] >= front_lower_right_corner['y']])

        if cond.all():
            return True

    return False


def _get_sparse_scan(scan, bboxes, one_out_of):
    sparse_scan = []

    count_in = 0
    count_out = 0

    for i in range(len(scan)):
        cond_for_each_bb = []
        point = scan[i]

        temp_point = [13.189, 4.211, -0.412]

        for _, value in bboxes.items():
            # print('bll x: {}'.format(value['bll']['x']))
            # print('bll y: {}'.format(value['bll']['y']))
            # print('bll z: {}'.format(value['bll']['z']))
            #
            # print('blr x: {}'.format(value['blr']['x']))
            # print('blr y: {}'.format(value['blr']['y']))
            # print('blr z: {}'.format(value['blr']['z']))
            #
            # print('bul x: {}'.format(value['bul']['x']))
            # print('bul y: {}'.format(value['bul']['y']))
            # print('bul z: {}'.format(value['bul']['z']))
            #
            # print('bur x: {}'.format(value['bur']['x']))
            # print('bur y: {}'.format(value['bur']['y']))
            # print('bur z: {}'.format(value['bur']['z']))
            #
            # print('fll x: {}'.format(value['fll']['x']))
            # print('fll y: {}'.format(value['fll']['y']))
            # print('fll z: {}'.format(value['fll']['z']))
            #
            # print('flr x: {}'.format(value['flr']['x']))
            # print('flr y: {}'.format(value['flr']['y']))
            # print('flr z: {}'.format(value['flr']['z']))
            #
            # print('ful x: {}'.format(value['ful']['x']))
            # print('ful y: {}'.format(value['ful']['y']))
            # print('ful z: {}'.format(value['ful']['z']))
            #
            # print('fur x: {}'.format(value['fur']['x']))
            # print('fur y: {}'.format(value['fur']['y']))
            # print('fur z: {}'.format(value['fur']['z']))
            #
            # print()

            #
            # print('point x: {}'.format(point[0]))
            # print('point y: {}'.format(point[1]))
            # print('point z: {}'.format(point[2]))
            # print()

            # error_margin = 2.5

            # cond = np.array([point[0] >= value['bll']['x'], point[1] <= value['bll']['y'], point[2] >= value['bll']['z'],
            #                  point[0] >= value['blr']['x'], point[1] >= value['blr']['y'],
            #                  point[2] <= value['bul']['z'],
            #                  point[0] <= value['fll']['x'], point[1] <= value['fll']['y'],
            #                  point[0] <= value['flr']['x'], point[1] >= value['flr']['y']])

            # cond = (point[0] >= value['bll']['x'] and point[1] >= value['bll']['y'] and point[2] >= value['bll']['z']) or \
            #        (point[0] >= value['bul']['x'] and point[1] >= value['bul']['y'] and point[2] <= value['bul']['z']) or \
            #        (point[0] >= value['blr']['x'] and point[1] <= value['blr']['y'] and point[2] >= value['blr']['z']) or \
            #        (point[0] >= value['bur']['x'] and point[1] <= value['bur']['y'] and point[2] <= value['bur']['z']) or \
            #        (point[0] <= value['fll']['x'] and point[1] >= value['fll']['y'] and point[2] >= value['fll']['z']) or \
            #        (point[0] <= value['ful']['x'] and point[1] >= value['ful']['y'] and point[2] <= value['ful']['z']) or \
            #        (point[0] <= value['flr']['x'] and point[1] <= value['flr']['y'] and point[2] >= value['flr']['z']) or \
            #        (point[0] <= value['fur']['x'] and point[1] <= value['fur']['y'] and point[2] <= value['fur']['z'])
            #
            # cond = (point[0] >= value['bll']['x'] or point[0] >= value['blr']['x']) and \
            #        (point[0] <= value['fll']['x'] or point[0] <= value['flr']['x']) and \
            #        (point[1] >= value['bll']['y'] or point[1] >= value['fll']['y']) and \
            #        (point[1] <= value['blr']['y'] or point[1] <= value['flr']['y']) and \
            #        value['bll']['z'] <= point[2] <= value['bul']['y']

            cond = ((value['fll']['x'] >= point[0] >= value['bll']['x']) or
                    (value['flr']['x'] >= point[0] >= value['blr']['x'])) and \
                   ((value['blr']['y'] >= point[1] >= value['bll']['y']) or
                    (value['flr']['y'] >= point[1] >= value['fll']['y'])) and \
                   (value['bul']['z'] >= point[2] >= value['bll']['z'])

            cond_for_each_bb.append(cond)

            if cond:
                break

        cond_for_each_bb = np.array(cond_for_each_bb)

        if cond_for_each_bb.any():
            sparse_scan.append(point)
            count_in += 1
        elif i % one_out_of == 0:
            sparse_scan.append(point)
            count_out += 1

    print('Points inside bboxes: {}'.format(count_in))
    print('Points outside bboxes: {}'.format(count_out))

    # plot_points(np.array(sparse_scan))
    return np.array(sparse_scan)


