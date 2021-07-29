import json
import matplotlib.pyplot as plt


json_path = r"G:\data\Edinburgh Informatics Forum Pedestrian Database\tracks.24Aug.json"
# entry_state = {}
fig, ax = plt.subplots()
with open(json_path) as f:
    json_data = json.load(f)
    for id in range(1, 1+len(json_data)): 
        # (px, py, vx, vy, gx, gy)
        current_track = json_data[str(id)]['Full_Tracklet']
        l = len(current_track)
        x = [current_track[i][0] for i in range(l)]
        y = [current_track[i][1] for i in range(l)]
        ax.plot(x, y, "-o", label=f"ped {id}", markersize=0.5)

save_path = r"G:\SFMProject\images\origin_track_24Aug.png"
plt.savefig(save_path)