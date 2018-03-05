import math

import numpy as np


class IndividualObject:
    def __init__(self, object_type, height, width, length, first_frame, tx, ty, tz, rx, ry, rz, count):

        self.object_type = object_type
        self.height = height
        self.width = width
        self.length = length
        self.first_frame = first_frame
        self.count = count
        self.poses = self._make_poses(tx, ty, tz, rx, ry, rz)

    def _make_poses(self, tx, ty, tz, rx, ry, rz):
        poses = []

        for i in range(len(tx)):
            poses.append(Pose(tx[i], ty[i], tz[i],
                              rx[i], ry[i], rz[i],
                              self.first_frame + i))

        return poses

    def get_pose_of_frame(self, frame):
        for pose in self.poses:
            if pose.number_of_frame == frame:
                return pose
                # return self.object_type, self.height, self.width, self.length,\
                #        pose.tx, pose.ty, pose.tz, pose.rx, pose.ry, pose.rz
        print('No pose of this object in that frame')

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

        # front_lower_left_corner = {'x': float(self.tx) - (float(length)/2),
        #                            'y': float(self.ty) - (float(width)/2),
        #                            'z': float(self.tz)}
        #
        # front_lower_right_corner = {'x': float(self.tx) - (float(length)/2),
        #                             'y': float(self.ty) + (float(width)/2),
        #                             'z': float(self.tz)}
        #
        # front_upper_left_corner = {'x': float(self.tx) - (float(length)/2),
        #                            'y': float(self.ty) - (float(width)/2),
        #                            'z': float(self.tz) + float(height)}
        #
        # front_upper_right_corner = {'x': float(self.tx) - (float(length)/2),
        #                             'y': float(self.ty) + (float(width)/2),
        #                             'z': float(self.tz) + float(height)}
        #
        # back_lower_left_corner = {'x': float(self.tx) + (float(length)/2),
        #                           'y': float(self.ty) - (float(width)/2),
        #                           'z': float(self.tz)}
        #
        # back_lower_right_corner = {'x': float(self.tx) + (float(length)/2),
        #                            'y': float(self.ty) + (float(width)/2),
        #                            'z': float(self.tz)}
        #
        # back_upper_left_corner = {'x': float(self.tx) + (float(length)/2),
        #                           'y': float(self.ty) - (float(width)/2),
        #                           'z': float(self.tz) + float(height)}
        #
        # back_upper_right_conrner = {'x': float(self.tx) + (float(length)/2),
        #                             'y': float(self.ty) + (float(width)/2),
        #                             'z': float(self.tz) + float(height)}

        front_lower_left = [float(self.tx) - (float(length)/2),
                            float(self.ty) - (float(width) / 2),
                            float(self.tz)]

        front_lower_right = [float(self.tx) - (float(length)/2),
                             float(self.ty) + (float(width)/2),
                             float(self.tz)]

        front_upper_left = [float(self.tx) - (float(length)/2),
                            float(self.ty) - (float(width)/2),
                            float(self.tz) + float(height)]

        front_upper_right = [float(self.tx) - (float(length)/2),
                             float(self.ty) + (float(width)/2),
                             float(self.tz) + float(height)]

        back_lower_left = [float(self.tx) + (float(length)/2),
                           float(self.ty) - (float(width)/2),
                           float(self.tz)]

        back_lower_right = [float(self.tx) + (float(length)/2),
                            float(self.ty) + (float(width)/2),
                            float(self.tz)]

        back_upper_left = [float(self.tx) + (float(length)/2),
                           float(self.ty) - (float(width)/2),
                           float(self.tz) + float(height)]

        back_upper_right = [float(self.tx) + (float(length)/2),
                            float(self.ty) + (float(width)/2),
                            float(self.tz) + float(height)]

        r_front_lower_left_corner = self._get_rotated_points(front_lower_left)
        r_front_lower_right_corner = self._get_rotated_points(front_lower_right)
        r_front_upper_left_corner = self._get_rotated_points(front_upper_left)
        r_front_upper_right_corner = self._get_rotated_points(front_upper_right)
        r_back_lower_left_corner = self._get_rotated_points(back_lower_left)
        r_back_lower_right_corner = self._get_rotated_points(back_lower_right)
        r_back_upper_left_corner = self._get_rotated_points(back_upper_left)
        r_back_upper_right_corner = self._get_rotated_points(back_upper_right)

        # print(r_front_lower_left_corner)
        # print(r_front_lower_right_corner)
        # print(r_front_upper_left_corner)
        # print(r_front_upper_right_corner)
        # print(r_back_lower_left_corner)
        # print(r_back_lower_right_corner)
        # print(r_back_upper_left_corner)
        # print(r_back_upper_right_corner)

        front_lower_left_corner = {'x': r_front_lower_left_corner[0],
                                   'y': r_front_lower_left_corner[1],
                                   'z': r_front_lower_left_corner[2]}

        front_lower_right_corner = {'x': r_front_lower_right_corner[0],
                                    'y': r_front_lower_right_corner[1],
                                    'z': r_front_lower_right_corner[2]}

        front_upper_left_corner = {'x': r_front_upper_left_corner[0],
                                   'y': r_front_upper_left_corner[1],
                                   'z': r_front_upper_left_corner[2]}

        front_upper_right_corner = {'x': r_front_upper_right_corner[0],
                                    'y': r_front_upper_right_corner[1],
                                    'z': r_front_upper_right_corner[2]}

        back_lower_left_corner = {'x': r_back_lower_left_corner[0],
                                  'y': r_back_lower_left_corner[1],
                                  'z': r_back_lower_left_corner[2]}

        back_lower_right_corner = {'x': r_back_lower_right_corner[0],
                                   'y': r_back_lower_right_corner[1],
                                   'z': r_back_lower_right_corner[2]}

        back_upper_left_corner = {'x': r_back_upper_left_corner[0],
                                  'y': r_back_upper_left_corner[1],
                                  'z': r_back_upper_left_corner[2]}

        back_upper_right_conrner = {'x': r_back_upper_right_corner[0],
                                    'y': r_back_upper_right_corner[1],
                                    'z': r_back_upper_right_corner[2]}

        return front_lower_left_corner, front_lower_right_corner, \
               front_upper_left_corner, front_upper_right_corner, \
               back_lower_left_corner, back_lower_right_corner, \
               back_upper_left_corner, back_upper_right_conrner

    def _get_rotated_points(self, vector):
        vector = np.asarray(vector)

        axis = [0, 1, 0]
        first_rotation = np.dot(self._rotation_matrix(axis, float(self.ry)), vector)

        axis = [0, 0, 1]
        second_rotation = np.dot(self._rotation_matrix(axis, float(self.rz)), first_rotation)

        axis = [1, 0, 0]
        third_rotation = np.dot(self._rotation_matrix(axis, float(self.rx)), second_rotation)

        return vector

    def _rotation_matrix(self, axis, theta):
        axis = np.asarray(axis)
        axis = axis / math.sqrt(np.dot(axis, axis))
        a = math.cos(theta / 2.0)
        b, c, d = -axis * math.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

    def __str__(self):
        print('Frame:\t{}'.format(self.number_of_frame))
        print('Tracklet x:\t{}'.format(self.tx))
        print('Tracklet y:\t{}'.format(self.ty))
        print('Tracklet z:\t{}\n'.format(self.tz))

        print('Rotation x:\t{}'.format(self.rx))
        print('Rotation y:\t{}'.format(self.ry))
        print('Rotation z:\t{}'.format(self.rz))
