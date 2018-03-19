import math

import numpy as np


class IndividualObject:
    def __init__(self, object_type, height, width, length, first_frame, tx, ty, tz, rx, ry, rz, count):

        self.object_type = object_type
        self.height = float(height)
        self.width = float(width)
        self.length = float(length)
        self.first_frame = int(first_frame)
        self.count = int(count)
        self.frames = list(range(self.first_frame, self.count))
        self.poses = self._make_poses(tx, ty, tz, rx, ry, rz)

    def _make_poses(self, tx, ty, tz, rx, ry, rz):
        poses = []

        for i in range(len(tx)):
            poses.append(Pose(float(tx[i]), float(ty[i]), float(tz[i]),
                              float(rx[i]), float(ry[i]), float(rz[i]),
                              self.first_frame + i))

        return poses

    def get_pose_of_frame(self, frame):
        for pose in self.poses:
            if pose.number_of_frame == frame:
                return pose

    def __str__(self):
        print('--------------------------------------------- NEW OBJECT ---------------------------------------------')
        print('Type:\t{}\n'.format(self.object_type))

        print('Height:\t{}'.format(self.height))
        print('Width:\t{}'.format(self.width))
        print('Length:\t{}\n'.format(self.length))

        print('First Frame:\t{}'.format(self.first_frame))
        print('Last Frame:\t{}\n'.format(self.first_frame + self.count))

        for pose in self.poses:
            print('=================== NEW POSE ===================')
            pose.__str__()
            print('================================================\n')

        print('-----------------------------------------------------------------------------------------------------\n')


class Pose:
    def __init__(self, tx, ty, tz, rx, ry, rz, number_of_frame):
        self.tx = tx
        self.ty = ty
        self.tz = tz
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.number_of_frame = number_of_frame

    def get_corners_of_bounding_box(self, height, width, length):

        origin = 0

        o_back_lower_right = [origin - (length / 2),
                              origin - (width / 2),
                              origin]

        o_back_lower_left = [origin - (length / 2),
                             origin + (width / 2),
                             origin]

        o_back_upper_right = [origin - (length / 2),
                              origin - (width / 2),
                              origin + height]

        o_back_upper_left = [origin - (length / 2),
                             origin + (width / 2),
                             origin + height]

        o_front_lower_right = [origin + (length / 2),
                               origin - (width / 2),
                               origin]

        o_front_lower_left = [origin + (length / 2),
                              origin + (width / 2),
                              origin]

        o_front_upper_right = [origin + (length / 2),
                               origin - (width / 2),
                               origin + height]

        o_front_upper_left = [origin + (length / 2),
                              origin + (width / 2),
                              origin + height]

        r_front_lower_left_corner = self._get_rotated_points(o_front_lower_left)
        r_front_lower_right_corner = self._get_rotated_points(o_front_lower_right)
        r_front_upper_left_corner = self._get_rotated_points(o_front_upper_left)
        r_front_upper_right_corner = self._get_rotated_points(o_front_upper_right)
        r_back_lower_left_corner = self._get_rotated_points(o_back_lower_left)
        r_back_lower_right_corner = self._get_rotated_points(o_back_lower_right)
        r_back_upper_left_corner = self._get_rotated_points(o_back_upper_left)
        r_back_upper_right_corner = self._get_rotated_points(o_back_upper_right)

        front_lower_left_corner = {'x': self.tx + r_front_lower_left_corner[0],
                                   'y': self.ty + r_front_lower_left_corner[1],
                                   'z': self.tz + r_front_lower_left_corner[2]}

        front_lower_right_corner = {'x': self.tx + r_front_lower_right_corner[0],
                                    'y': self.ty + r_front_lower_right_corner[1],
                                    'z': self.tz + r_front_lower_right_corner[2]}

        front_upper_left_corner = {'x': self.tx + r_front_upper_left_corner[0],
                                   'y': self.ty + r_front_upper_left_corner[1],
                                   'z': self.tz + r_front_upper_left_corner[2]}

        front_upper_right_corner = {'x': self.tx + r_front_upper_right_corner[0],
                                    'y': self.ty + r_front_upper_right_corner[1],
                                    'z': self.tz + r_front_upper_right_corner[2]}

        back_lower_left_corner = {'x': self.tx + r_back_lower_left_corner[0],
                                  'y': self.ty + r_back_lower_left_corner[1],
                                  'z': self.tz + r_back_lower_left_corner[2]}

        back_lower_right_corner = {'x': self.tx + r_back_lower_right_corner[0],
                                   'y': self.ty + r_back_lower_right_corner[1],
                                   'z': self.tz + r_back_lower_right_corner[2]}

        back_upper_left_corner = {'x': self.tx + r_back_upper_left_corner[0],
                                  'y': self.ty + r_back_upper_left_corner[1],
                                  'z': self.tz + r_back_upper_left_corner[2]}

        back_upper_right_conrner = {'x': self.tx + r_back_upper_right_corner[0],
                                    'y': self.ty + r_back_upper_right_corner[1],
                                    'z': self.tz + r_back_upper_right_corner[2]}

        return front_lower_left_corner, front_lower_right_corner, \
               front_upper_left_corner, front_upper_right_corner, \
               back_lower_left_corner, back_lower_right_corner, \
               back_upper_left_corner, back_upper_right_conrner

    def _get_rotated_points(self, vector):
        vector = np.asarray(vector)

        first_rotation = np.dot(self._rotation_matrix('y', float(self.ry)), vector)
        second_rotation = np.dot(self._rotation_matrix('z', float(self.rz)), first_rotation)
        third_rotation = np.dot(self._rotation_matrix('x', float(self.rx)), second_rotation)

        return third_rotation

    def _rotation_matrix(self, axis, theta):

        if axis == 'x':
            rotation_matrix = [[1, 0, 0],
                               [0, math.cos(theta), -math.sin(theta)],
                               [0, math.sin(theta), math.cos(theta)]]

        elif axis == 'y':
            rotation_matrix = [[math.cos(theta), 0, math.sin(theta)],
                               [0, 1, 0],
                               [-math.sin(theta), 0, math.cos(theta)]]

        else:
            rotation_matrix = [[math.cos(theta), -math.sin(theta), 0],
                               [math.sin(theta), math.cos(theta), 0],
                               [0, 0, 1]]

        return rotation_matrix

    def __str__(self):
        print('Frame:\t{}'.format(self.number_of_frame))
        print('Tracklet x:\t{}'.format(self.tx))
        print('Tracklet y:\t{}'.format(self.ty))
        print('Tracklet z:\t{}\n'.format(self.tz))

        print('Rotation x:\t{}'.format(self.rx))
        print('Rotation y:\t{}'.format(self.ry))
        print('Rotation z:\t{}'.format(self.rz))
