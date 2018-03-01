from data.kitti_raw_manager import get_objects_of_frame


def get_trackelts_in_frame(frame, tracklets):
    return get_objects_of_frame(frame, tracklets)
