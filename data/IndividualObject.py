class IndividualObject:
    def __init__(self, object_type, height, width, length, first_frame, tx, ty, tz, rx, ry, rz, count):

        self.object_type = object_type
        self.height = height
        self.width = width
        self.length = length
        self.first_frame = first_frame
        self.tx = tx
        self.ty = ty
        self.tz = tz
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.count = count
        self.poses = self._make_poses()

    def _make_poses(self):
        poses = []

        for i in range(len(self.tx)):
            poses.append(Pose(self.tx[i], self.ty[i], self.tz[i],
                              self.rx[i], self.ry[i], self.rz[i],
                              self.first_frame + i))

        return poses

    def __str__(self):
        print('Type:\t{}\n'.format(self.object_type))

        print('Height:\t{}'.format(self.height))
        print('Width:\t{}'.format(self.width))
        print('Length:\t{}\n'.format(self.length))

        print('First Frame:\t{}'.format(self.first_frame))
        print('Last Frame:\t{}\n'.format(self.first_frame + self.count))

        for pose in self.poses:
            pose.__str__()


class Pose:
    def __init__(self, tx, ty, tz, rx, ry, rz, number_of_frame):
        self.tx = tx
        self.ty = ty
        self.tz = tz
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.number_of_frame = number_of_frame

    def __str__(self):
        print('Tracklet x:\t{}'.format(self.tx))
        print('Tracklet y:\t{}'.format(self.ty))
        print('Tracklet z:\t{}\n'.format(self.tz))

        print('Rotation x:\t{}'.format(self.rx))
        print('Rotation y:\t{}'.format(self.ry))
        print('Rotation z:\t{}\n'.format(self.rz))
