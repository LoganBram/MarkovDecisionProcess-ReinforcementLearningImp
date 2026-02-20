import numpy as np
from enum import IntEnum
from copy import deepcopy
import matplotlib.pyplot as plt
plt.style.use('seaborn-notebook')
plt.style.use('seaborn-whitegrid')
import matplotlib.colors as mcolors

class Action(IntEnum):
    up = 0
    right = 1
    down = 2
    left = 3

action_to_str = {
    Action.up : "up",
    Action.right : "right",
    Action.down : "down",
    Action.left : "left",
}

action_to_offset = {
    Action.up : (-1, 0),
    Action.right : (0, 1),
    Action.down : (1, 0),
    Action.left : (0, -1),
}

class GridWorld:

    def __init__(self, height, width, goal, goal_value=5.0, danger=[], danger_value=-5.0, blocked=[], noise=0.0):
        """
        Initialize the GridWorld environment.
        Creates a gridworld like MDP
         - height (int): Number of rows
         - width (int): Number of columns
         - goal (int): Index number of goal cell
         - goal_value (float): Reward given for goal cell
         - danger (list of int): Indices of cells marked as danger
         - danger_value (float): Reward given for danger cell
         - blocked (list of int): Indices of cells marked as blocked (can't enter)
         - noise (float): probability of resulting state not being what was expected
        """

        self._width = width
        self._height = height
        self._grid_values = [0 for _ in range(height * width)] # Initialize state values.
        self._goal_value = goal_value
        self._danger_value = danger_value
        self._goal_cell = goal
        self._danger_cells = danger
        self._blocked_cells = blocked
        self._noise = noise # Noise level in the environment.
        assert noise >= 0 and noise < 1 # Ensure valid noise value.
        self.create_next_values() # Initialize the next state values.


    def reset(self):
        """
        Reset the state values to their initial state.
        """
        self._grid_values = [0 for _ in range(self._height * self._width)]
        self.create_next_values()


    def _inbounds(self, state):
        """
        Check if a state index is within the grid boundaries.
        """
        return state >= 0 and state < self._width * self._height

    def _inbounds_rc(self, state_r, state_c):
        """
        Check if row and column indices are within the grid boundaries.
        """
        return state_r >= 0 and state_r < self._height and state_c >= 0 and state_c < self._width

    def _state_to_rc(self, state):
        """
        Convert a state index to row and column indices.
        """
        return state // self._width, state % self._width

    def _state_from_action(self, state, action):
        """
        Gets the state as a result of applying the given action
        """
        #TO DO:

    def is_terminal(self, state):
        """
        Returns true if a state is terminal (goal, or danger)
        """
        #To Do:

    def get_states(self):
        """
        Gets all non-terminal states in the environment
        """
        #TO DO:


    def get_actions(self, state):
        """
        Returns a list of valid actions given the current state
        """
        #TO DO:


    def get_reward(self, state):
        """
        Get the reward for being in the current state
        """
        assert self._inbounds(state)
        # Reward is non-zero for danger or goal
        #TO DO:


    def get_transitions(self, state, action):
        """
        Get a list of transitions as a result of attempting the action in the current state
        Each item in the list is a dictionary, containing the probability of reaching that state and the state itself
        """
        #TO DO:


    def get_value(self, state):
        """
        Get the current value of the state
        """
        assert self._inbounds(state)
        return self._grid_values[state]

    def create_next_values(self):
        """
        Creates a temporary storage for state value updating
        If this is not used, then asynchronous updating may result in unexpected results
        To use properly, run this at the start of each iteration
        """
        #TO DO:

    def set_next_values(self):
        """
        Set the state values from the temporary copied values
        To use properly, run this at the end of each iteration
        """
        # TO DO:

    def set_value(self, state, value):
        """
        Set the value of the state into the temporary copy
        This value will not update into main storage until self.set_next_values() is called.
        """
        assert self._inbounds(state)
        #TO DO:

    def solve_linear_system(self, discount_factor=1.0):
        """
        Solve the gridworld using a system of linear equations.
        :param discount_factor: The discount factor for future rewards.
        """
        #To Do:

    def __str__(self):
        """
        Pretty print the state values
        """
        out_str = ""
        for r in range(self._height):
            for c in range(self._width):
                cell = r * self._width + c
                if cell in self._blocked_cells:
                    out_str += "{:>6}".format("----")
                elif cell == self._goal_cell:
                    out_str += "{:>6}".format("GOAL")
                elif cell in self._danger_cells:
                    out_str += "{:>6.2f}".format(self._danger_value)
                else:
                    out_str += "{:>6.2f}".format(self._grid_values[cell])
                out_str += " "
            out_str += "\n"
        return out_str
    
    # Initialize your GridWorld
simple_gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.0)

# Solve the linear system
values_grid = simple_gw.solve_linear_system(discount_factor=0.95)
print(values_grid)

def value_iteration(gw, discount, tolerance=0.1):
    #TO DO

# Initialize your GridWorld
simple_gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.0)
noisy_gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.2)
discount = 0.95
tolerance = 0.1

value_iteration(simple_gw, discount, 0.1)
print(simple_gw)

value_iteration(noisy_gw, discount, 0.1)
print(noisy_gw)

def policy_iteration(gw, discount, tolerance=0.1):
    #TO DO