from data.kitti_raw_manager import load_raw_tracklets
from plot.plot import plot_bounding_box

tracklets = load_raw_tracklets('0001')

pose = tracklets[0].get_pose_of_frame(0)


front_lower_left_corner, front_lower_right_corner,\
front_upper_left_corner, front_upper_right_corner, \
back_lower_left_corner, back_lower_right_corner,\
back_upper_left_corner, back_upper_right_corner = pose.get_corners_of_bounding_box(tracklets[0].height,
                                                                                   tracklets[0].width,
                                                                                   tracklets[0].length)

# print(front_lower_left_corner)
# print(front_lower_right_corner)
# print(front_upper_left_corner)
# print(front_upper_right_corner)
#
# print(back_lower_left_corner)
# print(back_lower_right_corner)
# print(back_upper_left_corner)
# print(back_upper_right_corner)

plot_bounding_box(front_lower_left_corner, front_lower_right_corner,
                  front_upper_left_corner, front_upper_right_corner,
                  back_lower_left_corner, back_lower_right_corner,
                  back_upper_left_corner, back_upper_right_corner)
