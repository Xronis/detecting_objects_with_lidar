from data.kitti_raw_manager import load_raw_tracklets, load_raw_data, load_single_tracklet
from plot.plot import plot_bounding_box, plot_velo

from plotly import graph_objs as go
import plotly.plotly as py

import plotly

plotly.tools.set_credentials_file(username='panagiotidisxronis', api_key='ttur4sQ0tHGT0m7cz5XT')

drive = '0001'
frame = 0
obj = 2

tracklets = load_single_tracklet(drive)

pose = tracklets[obj].get_pose_of_frame(frame)

# tracklets[obj].__str__()

front_lower_left_corner, front_lower_right_corner, \
front_upper_left_corner, front_upper_right_corner, \
back_lower_left_corner, back_lower_right_corner, \
back_upper_left_corner, back_upper_right_corner = pose.get_corners_of_bounding_box(tracklets[obj].height,
                                                                                   tracklets[obj].width,
                                                                                   tracklets[obj].length)

# print(front_lower_left_corner)
# print(front_lower_right_corner)
# print(front_upper_left_corner)
# print(front_upper_right_corner)
#
# print(back_lower_left_corner)
# print(back_lower_right_corner)
# print(back_upper_left_corner)
# print(back_upper_right_corner)

bbox_traces = plot_bounding_box(front_lower_left_corner, front_lower_right_corner,
                                front_upper_left_corner, front_upper_right_corner,
                                back_lower_left_corner, back_lower_right_corner,
                                back_upper_left_corner, back_upper_right_corner)

data = load_raw_data(drive)
scan_traces = plot_velo(data[frame])

layout = go.Layout(
    scene=dict(
        xaxis=dict(nticks=4, range=[-100, 100], ),
        yaxis=dict(nticks=4, range=[-50, 100], ),
        zaxis=dict(nticks=4, range=[-100, 100], ), ),
    width=700,
    margin=dict(r=20, l=10, b=10, t=10)
)

fig_data = [scan_traces[0], bbox_traces[0], bbox_traces[1]]

fig = go.Figure(data=fig_data, layout=layout)
py.plot(fig, filename='scan_with_tracklet')