import math

import numpy as np
from plotly import graph_objs as go
import plotly.plotly as py

import plotly

from data.kitti_raw_manager import load_raw_tracklets, load_raw_forward_data

plotly.tools.set_credentials_file(username='panagiotidisxronis', api_key='ttur4sQ0tHGT0m7cz5XT')


def plot_scan_with_bbox(drive, frame, y_threshold, one_out_of):
    for d in drive:
        tracklets = load_raw_tracklets(d)

        bbox_traces = []

        if y_threshold and one_out_of:
            data = load_raw_forward_data(d, one_out_of=one_out_of, y_threshold=y_threshold)
        elif y_threshold and not one_out_of:
            data = load_raw_forward_data(d, y_threshold=y_threshold)
        elif not y_threshold and one_out_of:
            data = load_raw_forward_data(d, one_out_of=one_out_of)
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

                    if one_out_of:
                        if _bbox_has_point(data[frame], front_lower_left_corner, front_lower_right_corner,
                                           front_upper_left_corner, back_lower_left_corner, back_lower_right_corner):
                            for b in bbox:
                                bbox_traces.append(b)
                    else:
                        for b in bbox:
                            bbox_traces.append(b)

                    # for b in bbox:
                    #     bbox_traces.append(b)

        scan_traces = _plot_velo(data[frame])

        layout = go.Layout(
            scene=dict(
                xaxis=dict(nticks=4, range=[-100, 100], ),
                yaxis=dict(nticks=4, range=[-50, 100], ),
                zaxis=dict(nticks=4, range=[-100, 100], ),
                aspectratio=dict(x=1, y=1, z=1)),
            width=700,
            margin=dict(r=0, l=0, b=0, t=0)
        )

        data = [scan_traces[0]]

        for bb in bbox_traces:
            data.append(bb)

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='scan_with_tracklet_{}'.format(d))
        # plotly.offline.plot(fig, filename='scan_with_tracklet_{}'.format(d))


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


def _bbox_has_point(scan, front_lower_left_corner, front_lower_right_corner,
                    front_upper_left_corner, back_lower_left_corner, back_lower_right_corner):

    for i in range(len(scan)):
        point = scan[i]

        x = point[0]
        y = point[1]
        z = point[2]

        cond = np.array([x >= front_lower_left_corner['x'], x >= front_lower_right_corner['x'],
 +                        x <= back_lower_left_corner['x'], x <= back_lower_right_corner['x'],
                         y <= front_lower_left_corner['y'], y >= front_lower_right_corner['y'],
                         y <= back_lower_left_corner['y'], y >= back_lower_right_corner['y'],
                         z >= front_lower_left_corner['z'], z <= front_upper_left_corner['z']])

        if cond.all():
            return True

    return False
