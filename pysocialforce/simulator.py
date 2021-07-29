# coding=utf-8

"""Synthetic pedestrian behavior with social groups simulation according to the Extended Social Force model.

See Helbing and Molnár 1998 and Moussaïd et al. 2010
"""
from tkinter.constants import N
from pysocialforce.utils import DefaultConfig
from pysocialforce.scene import PedState, EnvState
from pysocialforce import forces
import numpy as np


class Simulator:
    """Simulate social force model.

    ...

    Attributes
    ----------
    state : np.ndarray [n, 6] or [n, 7]
       Each entry represents a pedestrian state, (x, y, v_x, v_y, d_x, d_y, [tau])
    obstacles : np.ndarray
        Environmental obstacles
    groups : List of Lists
        Group members are denoted by their indices in the state
    config : Dict
        Loaded from a toml config file
    max_speeds : np.ndarray
        Maximum speed of pedestrians
    forces : List
        Forces to factor in during navigation

    Methods
    ---------
    capped_velocity(desired_velcity)
        Scale down a desired velocity to its capped speed
    step()
        Make one step
    """

    def __init__(self, state, entry_ped, goal_transition=None, cameraset=None, groups=None, obstacles=None, config_file=None):
        self.config = DefaultConfig()
        if config_file:
            self.config.load_config(config_file)
        # TODO: load obstacles from config
        self.scene_config = self.config.sub_config("scene")
        # initiate total simulated pedestrian with timestep
        self.in_peds = entry_ped

        # # initiate camera set
        # self.cameraset = cameraset

        # goal transition list
        self.goal_transition_list = goal_transition

        # initiate obstacles
        self.env = EnvState(obstacles, cameraset, self.config("resolution", 10.0))

        # initiate agents
        self.peds = PedState(state, groups, self.config)

        # construct forces
        self.forces = self.make_forces(self.config)

    def make_forces(self, force_configs):
        """Construct forces"""
        force_list = [
            forces.DesiredForce(),
            forces.SocialForce(),
            forces.ObstacleForce(),
            # forces.PedRepulsiveForce(),
            # forces.SpaceRepulsiveForce(),
        ]
        group_forces = [
            forces.GroupCoherenceForceAlt(),
            forces.GroupRepulsiveForce(),
            forces.GroupGazeForceAlt(),
        ]
        if self.scene_config("enable_group"):
            force_list += group_forces

        # initiate forces
        for force in force_list:
            force.init(self, force_configs)

        return force_list

    def compute_forces(self):
        """compute forces"""
        return sum(map(lambda x: x.get_force(), self.forces))

    def get_states(self):
        """Expose whole state"""
        return self.peds.get_states()

    def get_cameraset(self):
        """Expose cameras"""
        return self.env.cameraset
    # def add_states(self, states):
    #     """add new ped state"""
    #     self.peds = self.peds.add_ped_state(states)

    def get_length(self):
        """Get simulation length"""
        return len(self.get_states()[0])

    def get_obstacles(self):
        return self.env.obstacles

    def step_once(self, new_entry=None):
        """step once"""
        self.peds.step(self.compute_forces(), self.get_cameraset(), self.goal_transition_list, new_entry=new_entry)

    def step(self, n=1):
        """Step n time"""
        for t in range(n):
            entry_ped_list = []
            if str(t) in self.in_peds.keys():
                entry_ped_list = self.in_peds[str(t)]                   
            # else:
            self.step_once(entry_ped_list)
            if t == 59:
                print("pause")
        return self
