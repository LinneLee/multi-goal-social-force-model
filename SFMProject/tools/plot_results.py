import pickle
import matplotlib.pyplot as plt


state_path = r"G:\SFMProject\multi-goal_SFM_ped_states.pickle"
with open(state_path, 'rb') as f:
    ped_states = pickle.load(f)

l = len(ped_states)
fig, ax = plt.subplots()

latest_entry_id = 0
show_time = 60
for t in range(len(ped_states)):
    current_entry_ids = []
    if t == 0:
        current_entry_num = len(ped_states[t])
    else:
        current_entry_num = len(ped_states[t]) - len(ped_states[t-1])
    
    current_entry_ids = [i+latest_entry_id for i in range(current_entry_num)]
    for ped in current_entry_ids:
        x = [ped_states[i][ped][0] for i in range(t, l)]
        y = [ped_states[i][ped][1] for i in range(t, l)]
        ax.plot(x, y, "-o", label=f"ped {ped}", markersize=0.5)
        # plt.show()
        # if t == show_time:
        #     plt.show()
        #     show_time += 100
    latest_entry_id += current_entry_num
save_path = r"G:\SFMProject\images\result2(Multi-goal-social-force).png"
# plt.show()
plt.savefig(save_path)