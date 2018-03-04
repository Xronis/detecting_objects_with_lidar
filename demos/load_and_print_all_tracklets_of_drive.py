from data.kitti_raw_manager import load_single_tracklet

tracklets = load_single_tracklet('0002')

for i in range(len(tracklets)):
    tracklets[i].__str__()
