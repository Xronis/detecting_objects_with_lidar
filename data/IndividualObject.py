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

        # front_lower_left_corner = {'x': float(self.tx),
        #                            'y': float(self.ty),
        #                            'z': float(self.tz)}
        #
        # front_lower_right_corner = {'x': float(self.tx) + float(length),
        #                             'y': float(self.ty),
        #                             'z': float(self.tz)}
        #
        # front_upper_left_corner = {'x': float(self.tx),
        #                            'y': float(self.ty) + float(width),
        #                            'z': float(self.tz)}
        #
        # front_upper_right_corner = {'x': float(self.tx) + float(length),
        #                             'y': float(self.ty) + float(width),
        #                             'z': float(self.tz)}
        #
        # back_lower_left_corner = {'x': float(self.tx),
        #                           'y': float(self.ty),
        #                           'z': float(self.tz) + float(height)}
        #
        # back_lower_right_corner = {'x': float(self.tx) + float(length),
        #                            'y': float(self.ty),
        #                            'z': float(self.tz) + float(height)}
        #
        # back_upper_left_corner = {'x': float(self.tx),
        #                           'y': float(self.ty) + float(width),
        #                           'z': float(self.tz) + float(height)}
        #
        # back_upper_right_conrner = {'x': float(self.tx) + float(length),
        #                             'y': float(self.ty) + float(width),
        #                             'z': float(self.tz) + float(height)}

        front_lower_left_corner = {'x': float(self.tx) - (float(length)/2),
                                   'y': float(self.ty) - (float(width)/2),
                                   'z': float(self.tz)}

        front_lower_right_corner = {'x': float(self.tx) - (float(length)/2),
                                    'y': float(self.ty) + (float(width)/2),
                                    'z': float(self.tz)}

        front_upper_left_corner = {'x': float(self.tx) - (float(length)/2),
                                   'y': float(self.ty) - (float(width)/2),
                                   'z': float(self.tz) + float(height)}

        front_upper_right_corner = {'x': float(self.tx) - (float(length)/2),
                                    'y': float(self.ty) + (float(width)/2),
                                    'z': float(self.tz) + float(height)}

        back_lower_left_corner = {'x': float(self.tx) + (float(length)/2),
                                  'y': float(self.ty) - (float(width)/2),
                                  'z': float(self.tz)}

        back_lower_right_corner = {'x': float(self.tx) + (float(length)/2),
                                   'y': float(self.ty) + (float(width)/2),
                                   'z': float(self.tz)}

        back_upper_left_corner = {'x': float(self.tx) + (float(length)/2),
                                  'y': float(self.ty) - (float(width)/2),
                                  'z': float(self.tz) + float(height)}

        back_upper_right_conrner = {'x': float(self.tx) + (float(length)/2),
                                    'y': float(self.ty) + (float(width)/2),
                                    'z': float(self.tz) + float(height)}

        return front_lower_left_corner, front_lower_right_corner, \
               front_upper_left_corner, front_upper_right_corner, \
               back_lower_left_corner, back_lower_right_corner, \
               back_upper_left_corner, back_upper_right_conrner

    def __str__(self):
        print('Frame:\t{}'.format(self.number_of_frame))
        print('Tracklet x:\t{}'.format(self.tx))
        print('Tracklet y:\t{}'.format(self.ty))
        print('Tracklet z:\t{}\n'.format(self.tz))

        print('Rotation x:\t{}'.format(self.rx))
        print('Rotation y:\t{}'.format(self.ry))
        print('Rotation z:\t{}'.format(self.rz))
