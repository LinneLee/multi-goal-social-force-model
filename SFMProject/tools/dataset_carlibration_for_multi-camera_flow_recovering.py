"""
dateset: Edinburgh Informatics Forum Pedestrian Database
pick some areas as camera surveillanced tracklets, other unknown
area will be simulated with social force model

this python file was used to generate intermidirated goal for social force in the given area
"""

import json
import matplotlib.pyplot as plt
import pickle


def isInCameraNum(cameraset, position):
    for camera in cameraset.keys():
        camera_region = cameraset[camera]
        x, y , _ = position
        if x>camera_region[0] & x<camera_region[2]:
            if y>camera_region[1] & y<camera_region[3]:
                return camera

    return None
# function definition before call

# destination = []
virtual_camera1 = [440, 0, 640, 200]
virtual_camera2 = [80, 300, 300, 480]
virtual_camera3 = [0, 0, 175, 175]
cameras = {
1:virtual_camera1,
2:virtual_camera2,
3:virtual_camera3
}
json_path = r"G:\data\Edinburgh Informatics Forum Pedestrian Database\tracks.24Aug.json"

transition = {}
with open(json_path) as f:
    json_data = json.load(f)
    for id in range(1, 1+len(json_data)): 
        # (px, py, vx, vy, gx, gy)
        camera_list = []
        current_track = json_data[str(id)]['Full_Tracklet']
        for pos in current_track:
            camera_list.append(isInCameraNum(cameras, pos))
            # pos_camera_dic[pos] = isInCameraNum(cameras, pos)
        
        # generate camera transition
        last_camera = None
        goal_set = []
        for ix, camera_id in enumerate(camera_list):
            if last_camera is None:
                if camera_id is not None:
                    last_camera = [camera_id, current_track[ix]] # [1, [468, 8, 60]]
                    goal_set.append([last_camera])
            else:
                if camera_id != last_camera[0]:
                    if camera_id is not None:
                        # transit
                        last_camera = [camera_id, current_track[ix]]
                        goal_set.append(last_camera)

        transition[id] = goal_set

save_path = r"G:\SFMProject\gaol_transitions.pickle"
with open(save_path, "wb") as f:
    pickle.dump(transition, f)

with open(save_path, "rb") as f:
    obj = pickle.load(f)