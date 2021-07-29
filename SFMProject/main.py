from pathlib import Path
import numpy as np
import pysocialforce as psf
import pickle


if __name__ == "__main__":
    # initial states, each entry is the position, velocity and goal of a pedestrian in the form of (px, py, vx, vy, gx, gy)
    initial_state = np.array(
        [
            # [0.0, 0, 0, 0, 0.0, 0.0],
            [0.5, 10, -0.5, -0.5, 0.5, 0.0],
            # [0.0, 0.0, 0.0, 0.5, 1.0, 10.0],
            # [1.0, 0.0, 0.0, 0.5, 2.0, 10.0],
            # [2.0, 0.0, 0.0, 0.5, 3.0, 10.0],
            # [3.0, 0.0, 0.0, 0.5, 4.0, 10.0],
        ]
    )
    # 
    # with open(json_path) as f:
    #     json_data = json.load(f)
    # social groups informoation is represented as lists of indices of the state array
    # groups = [[1, 0], [2]]

    # in_ped_list: {timestep: entry pedetrian list[id,state]} 
    # entry_state = {"1": [[12, 34, 1, 0.5, 0.5, 47, 48], [12, 34, 1, 0.5, 0.5, 47, 48]], 2:[[12, 34, 1, 0.5, 0.5, 47, 48]]}
    
    # entry_path = r"G:\SFMProject\entry_states.pickle"
    entry_path = r"G:\SFMProject\entry_states_for_multi-goal.pickle"
    with open(entry_path, 'rb') as f:
        entry_state = pickle.load(f)
    # entry_state = {}
    
    # camera set
    virtual_camera1 = [440, 0, 640, 200]
    virtual_camera2 = [80, 300, 300, 480]
    virtual_camera3 = [0, 0, 175, 175]
    cameras = {
    1:virtual_camera1,
    2:virtual_camera2,
    3:virtual_camera3
    }

    # goal transition list
    goal_transition_path = r"G:\SFMProject\gaol_transitions.pickle"
    with open(goal_transition_path, "rb") as f:
        goal_transition = pickle.load(f)
    
    # list of linear obstacles given in the form of (x_min, x_max, y_min, y_max)
    # obs = [[-1, -1, -1, 11], [3, 3, -1, 11]]
    obs = [[325, 0, 325, 35], [325, 35, 443, 40], [443, 40, 443, 0], [0, 290, 70, 320],
    [70, 320, 100, 375], [100, 375, 100, 455], [160, 445, 250,450], [300, 430, 345, 450], 
    [390, 450, 590, 460]]
    # obs = None
    # initiate the simulator,
    # s = psf.Simulator(
    #     initial_state,
    #     groups=groups,
    #     obstacles=obs,
    #     config_file=Path(__file__).resolve().parent.joinpath("example.toml"),
    # )
    s = psf.Simulator(
        initial_state,
        entry_state,
        goal_transition,
        cameraset=cameras,
        groups=None,
        obstacles=obs,
        config_file=Path(__file__).resolve().parent.joinpath("setup/example.toml"),
    )
    # update 50 steps; maxmum update timestep
    # s.step(100)
    s.step(10000)
    # save_state_path = r"G:\SFMProject\SFM_ped_states.pickle"
    save_state_path = r"G:\SFMProject\multi-goal_SFM_ped_states.pickle"
    with open(save_state_path, 'wb') as f:
        pickle.dump(s.peds.ped_states, f)
    # pic_path = "images/exmaple"
    with psf.plot.SceneVisualizer(s, "G:\SFMProject\images\example", figsize=[640, 480]) as sv:
        sv.animate()
        sv.plot()
1