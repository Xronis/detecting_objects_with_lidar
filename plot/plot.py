from plotly import graph_objs as go
import plotly.plotly as py

import plotly

plotly.tools.set_credentials_file(username='panagiotidisxronis', api_key='ttur4sQ0tHGT0m7cz5XT')


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

    # fig = go.Figure(data=data, layout=layout)
    # py.plot(fig, filename='scan')

    return data


def plot_bounding_box(front_lower_left_corner, front_lower_right_corner,
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

    # fig = go.Figure(data=[trace1, trace2])
    # py.plot(fig, filename='simple-3d-scatter')

    return [trace1, trace2]
