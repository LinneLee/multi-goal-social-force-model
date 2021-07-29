"""This module tracks the state odf scene and scen elements like pedestrians, groups and obstacles"""
from tkinter.constants import NO
from typing import List

import numpy as np

from pysocialforce.utils import stateutils

import random
"""
calculate and record the states of pedestrians, 
multi-goal?
"""


class PedState:
    """Tracks the state of pedstrains and social groups"""

    def __init__(self, state, groups, config):
        self.default_tau = config("tau", 0.5) # Transition Time
        self.step_width = config("step_width", 0.4)
        self.agent_radius = config("agent_radius", 0.35)
        self.max_speed_multiplier = config("max_speed_multiplier", 6) # 1.3m/s

        self.max_speeds = None
        self.initial_speeds = None
        
        self.ped_states = [] # track the state of pedestrians in each step
        self.group_states = [] # 
        self.entry_state = [] # record entry pedestrian number at each step

        self.update(state, groups, state.shape[0])

    def update(self, state, groups, entry):
        self.state = state
        self.groups = groups
        self.entry_state.append(entry)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        tau = self.default_tau * np.ones(state.shape[0])
        goal_num = np.ones(state.shape[0]) * (-1)
        if state.shape[1] == 6:
            self._state = np.concatenate((state, np.expand_dims(tau, -1), np.expand_dims(goal_num, -1)), axis=-1)
        else:
            self._state = state
        # if self.initial_speeds is None:
        #     self.initial_speeds = self.speeds()
        self.initial_speeds = self.speeds()
 
        self.max_speeds = self.max_speed_multiplier * np.ones(self.initial_speeds.shape[0])
        self.ped_states.append(self._state.copy())

    def get_states(self):
        return self.ped_states, self.group_states, self.entry_state

    # def add_ped_state(self, states):
    #     # new_states = self.ped_states.append(states)
    #     new_states = np.append(self.state, np.array(states), axis=0)
    #     new_groups = self.groups
    #     self.update(new_states, new_groups)
        

    def size(self) -> int:
        return self.state.shape[0]

    def pos(self) -> np.ndarray:
        return self.state[:, 0:2]

    def vel(self) -> np.ndarray:
        return self.state[:, 2:4] # velocities

    def goal(self) -> np.ndarray:
        return self.state[:, 4:6]

    def tau(self):
        return self.state[:, 6:7]

    def speeds(self):
        """Return the speeds corresponding to a given state."""
        return stateutils.speeds(self.state)

    def step(self, force, cameraset=None, goal_transition=None, groups=None, new_entry=None):
        """Move peds according to forces"""
        # desired velocity
        desired_velocity = self.vel() + self.step_width * force
        desired_velocity = self.capped_velocity(desired_velocity, self.max_speeds)
        # # stop when arrived
        goal_transition[0] = [] # special for init ped 0 
        # desired_velocity[stateutils.desired_directions(self.state)[1] < 0.5] = [0, 0]
        
        # update goals or stop when arrived 
        _ , dist = stateutils.desired_directions(self.state)
        for ix in range(self.state.shape[0]):
            if dist[ix] < 0.5: # when ped[ix] arrived at his destination
                next_goal_num = self.state[ix, 7] + 1
                max_goal_num = len(goal_transition[ix])
                if next_goal_num>=max_goal_num:
                    desired_velocity[ix] = [0, 0] 
                else:
                    # compute next goal
                    next_goal_region, _ = goal_transition[ix][int(next_goal_num)]
                    # next_goal = computeGoalFromRegion(cameraset[next_goal_region])
                    region = cameraset[next_goal_region]
                    x = random.random()*(region[2]-region[0]) + region[0]
                    y = random.random()*(region[3]-region[1]) + region[1]
                    next_goal = [x, y]
                    self.state[ix, 4: 6] = next_goal
                    self.state[ix, 7] += 1

        # goal_num = self.state[:, 7]
        # max_goal_num = [len(g) for g in goal_trasition]
        # next_goal_region = goal_trasition[: self.state[0]][goal_num][0]
        # next_goal_region_flag = np.zeros(next_goal_region.shape)
        # next_goal_region[goal_num<max_goal_num] += 1
        # next_goal_region_flag[goal_num<max_goal_num] += 1
        # next_goal_region[next_goal_region_flag==0] = 0
        # next_goal = [[random.random()*(region[2]-region[0]) + region[0], random.random()*(region[3]-region[1]) + region[1]] if region!=0 else self.state[***] for region in next_goal_region]


        # desired_velocity[stateutils.desired_directions(self.state)[1] < 0.5 & goal_num==max_goal_num] = [0, 0]
        # self.state[goal_num<max_goal_num, 7] += 1

        # update state
        next_state = self.state
        next_state[:, 0:2] += desired_velocity * self.step_width
        next_state[:, 2:4] = desired_velocity
        # add new entry pedestrian
        if len(new_entry)!=0:
            tau = self.default_tau * np.ones(new_entry.shape[0])
            goal_num = np.zeros(new_entry.shape[0])
            new_entry = np.concatenate((new_entry, np.expand_dims(tau, -1), np.expand_dims(goal_num, -1)), axis=-1)
            next_state = np.append(next_state, new_entry, axis=0)
        next_groups = self.groups
        if groups is not None:
            next_groups = groups
        self.update(next_state, next_groups, len(new_entry))

    # def initial_speeds(self):
    #     return stateutils.speeds(self.ped_states[0])

    def desired_directions(self):
        return stateutils.desired_directions(self.state)[0]

    @staticmethod
    def capped_velocity(desired_velocity, max_velocity):
        """Scale down a desired velocity to its capped speed."""
        desired_speeds = np.linalg.norm(desired_velocity, axis=-1)
        factor = np.minimum(1.0, max_velocity / (desired_speeds+0.0000000001))
        factor[desired_speeds == 0] = 0.0
        return desired_velocity * np.expand_dims(factor, -1)

    @property
    def groups(self) -> List[List]:
        return self._groups

    @groups.setter
    def groups(self, groups: List[List]):
        if groups is None:
            self._groups = []
        else:
            self._groups = groups
        self.group_states.append(self._groups.copy())

    def has_group(self):
        return self.groups is not None

    # def get_group_by_idx(self, index: int) -> np.ndarray:
    #     return self.state[self.groups[index], :]

    def which_group(self, index: int) -> int:
        """find group index from ped index"""
        for i, group in enumerate(self.groups):
            if index in group:
                return i
        return -1


class EnvState:
    """State of the environment obstacles and cameraset"""

    def __init__(self, obstacles, cameras, resolution=10):
        self.resolution = resolution
        self.obstacles = obstacles
        self.cameraset = cameras

    @property
    def obstacles(self) -> List[np.ndarray]:
        """obstacles is a list of np.ndarray"""
        return self._obstacles

    @obstacles.setter
    def obstacles(self, obstacles):
        """Input an list of (startx, endx, starty, endy) as start and end of a line"""
        if obstacles is None:
            self._obstacles = []
        else:
            self._obstacles = []
            for startx, endx, starty, endy in obstacles:
                samples = int(np.linalg.norm((startx - endx, starty - endy)) * self.resolution)
                line = np.array(
                    list(
                        zip(np.linspace(startx, endx, samples), np.linspace(starty, endy, samples))
                    )
                )
                self._obstacles.append(line)
