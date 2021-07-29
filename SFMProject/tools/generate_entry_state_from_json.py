import json
import numpy as np
import pickle


"""generate entry state array for social force model from proccessed json data. """
# class Track_data:
#     def __init__(self) -> None:
#         pass


json_path = r"G:\data\Edinburgh Informatics Forum Pedestrian Database\tracks.24Aug.json"
entry_state = {}
with open(json_path) as f:
    json_data = json.load(f)
    for id in range(1, 1+len(json_data)):
        # (px, py, vx, vy, gx, gy)
        et = json_data[str(id)]["Entry_Time"]
        initial_pos = json_data[str(id)]["Entry_Position"]
        goal = json_data[str(id)]["Leave_Position"]
        initial_vel = [json_data[str(id)]['Full_Tracklet'][1][:-1][x]
        -json_data[str(id)]['Full_Tracklet'][0][:-1][x] for x in range(2)]
        if int(et) not in entry_state.keys():
            # entry_state[str(et)] = np.array([initial_pos+initial_vel+goal])
            entry_state[str(et)] = np.array([initial_pos+initial_vel+initial_pos])

        else:
            entry_state[str(et)] = np.append(entry_state[str(et)], 
            # np.array(initial_pos+initial_vel+goal), axis=0)
            np.array(initial_pos+initial_vel+initial_pos), axis=0)

# save_path = r"G:\SFMProject\entry_states.pickle"
# with open(save_path, 'wb') as f:
#     pickle.dump(entry_state, f, pickle.HIGHEST_PROTOCOL)
    
# entry_path = r"G:\SFMProject\entry_states.pickle"
# with open(entry_path, 'rb') as f:
#     load_entry_state = pickle.load(f)
#     print('sdfa')

save_path = r"G:\SFMProject\entry_states_for_multi-goal.pickle"
with open(save_path, 'wb') as f:
    pickle.dump(entry_state, f, pickle.HIGHEST_PROTOCOL)