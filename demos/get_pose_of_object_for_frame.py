from data.kitti_raw_manager import load_single_tracklet

tracklets = load_single_tracklet('0002')

pose_0 = tracklets[1].get_pose_of_frame(0)
pose_0.__str__()

