from data.kitti_raw_manager import load_raw_tracklets, load_raw_data
from plot.plot import plot_bounding_box, plot_velo

from plotly import graph_objs as go
import plotly.plotly as py

import plotly

plotly.tools.set_credentials_file(username='panagiotidisxronis', api_key='ttur4sQ0tHGT0m7cz5XT')

drive = ['0001', '0002', '0005', '0009']
frame = 0

for d in drive:
    tracklets = load_raw_tracklets(d)

    bbox_traces = []

    for tracklet in tracklets:
        if tracklet.first_frame == frame:

            pose = tracklet.get_pose_of_frame(frame)

            front_lower_left_corner, front_lower_right_corner, \
            front_upper_left_corner, front_upper_right_corner, \
            back_lower_left_corner, back_lower_right_corner, \
            back_upper_left_corner, back_upper_right_corner = pose.get_corners_of_bounding_box(tracklet.height,
                                                                                               tracklet.width,
                                                                                               tracklet.length)

            bbox = plot_bounding_box(front_lower_left_corner, front_lower_right_corner,
                                     front_upper_left_corner, front_upper_right_corner,
                                     back_lower_left_corner, back_lower_right_corner,
                                     back_upper_left_corner, back_upper_right_corner)

            for b in bbox:
                bbox_traces.append(b)

    data = load_raw_data(d)
    scan_traces = plot_velo(data[frame])

    layout = go.Layout(
        scene=dict(
            xaxis=dict(nticks=4, range=[-100, 100], ),
            yaxis=dict(nticks=4, range=[-50, 100], ),
            zaxis=dict(nticks=4, range=[-100, 100], ), ),
        width=700,
        margin=dict(r=20, l=10, b=10, t=10)
    )

    data = [scan_traces[frame]]

    for bb in bbox_traces:
        data.append(bb)

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='scan_with_tracklet')
