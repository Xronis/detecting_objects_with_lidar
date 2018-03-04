from data.kitti_raw_manager import load_single_tracklet

tracklets = load_single_tracklet('0002')

for tracklet in tracklets:
    tracklet.__str__()

