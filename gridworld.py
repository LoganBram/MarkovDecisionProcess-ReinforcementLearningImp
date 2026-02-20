from enum import IntEnum
import numpy as np

class Action(IntEnum):
    up = 0
    right = 1
    down = 2
    left = 3


action_to_str = {
    Action.up: "up",
    Action.right: "right",
    Action.down: "down",
    Action.left: "left",
}

action_to_offset = {
    Action.up: (-1, 0),
    Action.right: (0, 1),
    Action.down: (1, 0),
    Action.left: (0, -1),
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
        self._grid_values = [0 for _ in range(height * width)]  # Initialize state values.
        self._goal_value = goal_value
        self._danger_value = danger_value
        self._goal_cell = goal
        self._danger_cells = danger
        self._blocked_cells = blocked
        self._noise = noise  # Noise level in the environment.
        assert noise >= 0 and noise < 1  # Ensure valid noise value.
        self.create_next_values()  # Initialize the next state values.

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
        # make sure state is a valid number like 0..24
        assert self._inbounds(state)

        # convert 1D state number into row/col
        r, c = self._state_to_rc(state)

        # get the movement offset for that action
        dr, dc = action_to_offset[action]

        # compute the attempted new row/col
        nr, nc = r + dr, c + dc

        # if it goes off the grid, stay where you are
        if not self._inbounds_rc(nr, nc):
            return state

        # convert attempted row/col back to 1D state number
        next_state = nr * self._width + nc

        # if the attempted cell is blocked, stay where you are
        if next_state in self._blocked_cells:
            return state

        # otherwise, the move succeeds
        return next_state

    def is_terminal(self, state):
        """
        Returns true if a state is terminal (goal, or danger)
        """
        # TO DO:
        if state == self._goal_cell:
            return True
        elif state in self._danger_cells:
            return True
        return False

    def get_states(self):
        """
        Gets all non-terminal states in the environment
        """
        # TO DO:
        #loop through every possible state
        #if value in is_terminal == false
            #add to array

        #also check if cell is blocked

        nonterm_states = []
        for i in range(self._height * self._width):
            if (not self.is_terminal(i)) and (i not in self._blocked_cells):
                nonterm_states.append(i)
        return nonterm_states

    def get_actions(self, state):
        """
        Returns a list of valid actions given the current state
        """
        # TO DO:
        return [Action.up, Action.down, Action.left, Action.right]

    def get_reward(self, state):
        """
        Get the reward for being in the current state
        """
        assert self._inbounds(state)
        # Reward is non-zero for danger or goal
        # TO DO:
        if state == self._goal_cell:
            return self._goal_value
        elif state in self._danger_cells:
            return self._danger_value
        else:
            return 0
        

    def get_transitions(self, state, action):
        """
        Get a list of transitions as a result of attempting the action in the current state
        Each item in the list is a dictionary, containing the probability of reaching that state and the state itself
        """
        transitions = []
        
        if self._noise == 0.0:
            # Deterministic case - just one transition
            next_state = self._state_from_action(state, action)
            transitions.append({'probability': 1.0, 'state': next_state})
        else:
            # Stochastic case - consider all possible actions due to noise
            # The agent goes in the intended direction with probability (1 - noise)
            # With probability noise, it could go in any of the 4 directions equally
            
            intended_next_state = self._state_from_action(state, action)
            
            # Probability of each random direction due to noise
            noise_prob_per_action = self._noise / 4.0
            
            # Start with intended action having base probability of (1 - noise)
            # But we need to account for the case where noise also leads to the same state
            state_probs = {}
            
            # Add probability for intended action
            state_probs[intended_next_state] = 1.0 - self._noise
            
            # Add probabilities for all 4 actions due to noise
            for a in [Action.up, Action.right, Action.down, Action.left]:
                next_state = self._state_from_action(state, a)
                if next_state in state_probs:
                    state_probs[next_state] += noise_prob_per_action
                else:
                    state_probs[next_state] = noise_prob_per_action
            
            # Convert to list of transition dictionaries
            for next_state, prob in state_probs.items():
                transitions.append({'probability': prob, 'state': next_state})
        
        return transitions

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
        # TO DO:
        self._next_grid_values = self._grid_values.copy()

    def set_next_values(self):
        """
        Set the state values from the temporary copied values
        To use properly, run this at the end of each iteration
        """
        # TO DO:
        self._grid_values = self._next_grid_values.copy()


    def set_value(self, state, value):
        """
        Set the value of the state into the temporary copy
        This value will not update into main storage until self.set_next_values() is called.
        """
        assert self._inbounds(state)
        self._next_grid_values[state] = value

    def solve_linear_system(self, discount_factor=1.0):
        """
        Solve the gridworld using a system of linear equations.
        Only works for deterministic case (noise=0)
        """
        
        # Step 1: Get all non-terminal states
        states = self.get_states()
        num_states = len(states)
        
        # Step 2: Create a mapping from state number to equation index
        state_to_index = {}
        for i, state in enumerate(states):
            state_to_index[state] = i
        
        # Step 3: Create empty matrix A and vector b
        A = np.zeros((num_states, num_states))
        b = np.zeros(num_states)
        
        # Step 4: Build the equations - one for each state
        for i, state in enumerate(states):
            
            # Start with coefficient 1.0 for V(state) itself
            A[i, i] = 1.0
            
            # Set the reward (right side of equation)
            b[i] = self.get_reward(state)
            
            # Look at all 4 possible actions
            for action in self.get_actions(state):
                
                # Find out where this action takes us
                next_state = self._state_from_action(state, action)
                
                # If terminal, add its reward to b (right side)
                # If non-terminal, add its coefficient to A (left side)
                if self.is_terminal(next_state):
                    # Terminal states contribute their reward directly
                    # With uniform random policy: each action has 25% probability
                    b[i] += discount_factor * 0.25 * self.get_reward(next_state)
                elif next_state in state_to_index:
                    # Non-terminal states contribute through their value
                    j = state_to_index[next_state]
                    A[i, j] -= discount_factor * 0.25
        
        # Step 5: Solve the system Ax = b
        values = np.linalg.solve(A, b)
        
        # Step 6: Update the gridworld with the solved values
        for i, state in enumerate(states):
            self._grid_values[state] = values[i]
        
        # Set values for terminal states
        self._grid_values[self._goal_cell] = self._goal_value
        for danger in self._danger_cells:
            self._grid_values[danger] = self._danger_value
        
        # Return self for convenience
        return self
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


def value_iteration(gw, discount, tolerance=0.1):
    iteration = 0
    
    while True:
        iteration += 1
        gw.create_next_values()  # Create temporary storage
        max_change = 0  # Track biggest value change this iteration
        
        # Loop through all non-terminal states
        for state in gw.get_states():
            action_values = []  # Store expected value for each action
            
            # Try each possible action from this state
            for action in gw.get_actions(state):
                expected_value = 0
                
                # Get all possible outcomes of this action
                transitions = gw.get_transitions(state, action)
                
                # Calculate expected value using Bellman equation
                for trans in transitions:
                    next_state = trans['state']
                    prob = trans['probability']
                    
                    # Get reward for entering next state
                    reward = gw.get_reward(next_state)
                    
                    # Get value of next state (0 if terminal)
                    if gw.is_terminal(next_state):
                        next_value = 0
                    else:
                        next_value = gw.get_value(next_state)
                    
                    # Bellman equation: sum of prob * (reward + discount * future_value)
                    expected_value += prob * (reward + discount * next_value)
                
                action_values.append(expected_value)
            
            # Take the MAXIMUM value across all actions (optimal policy)
            new_value = max(action_values)
            
            # Track how much this value changed
            old_value = gw.get_value(state)
            change = abs(new_value - old_value)
            max_change = max(max_change, change)
            
            # Store new value in temporary storage
            gw.set_value(state, new_value)
        
        # Commit all new values at once (synchronous update)
        gw.set_next_values()
        
        print(f"Iteration {iteration}: max change = {max_change:.6f}")
        
        # Check for convergence
        if max_change < tolerance:
            print(f"Converged after {iteration} iterations!")
            break
    
    # Set terminal state values
    gw._grid_values[gw._goal_cell] = gw._goal_value
    for danger in gw._danger_cells:
        gw._grid_values[danger] = gw._danger_value


def policy_iteration(gw, discount, tolerance=0.1):
    # TO DO
    pass


if __name__ == "__main__":
    # Initialize your GridWorld
    simple_gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.0)

    # Solve the linear system (will work after you implement solve_linear_system)
    # values_grid = simple_gw.solve_linear_system(discount_factor=0.95)
    # print(values_grid)

    # Initialize your GridWorlds for value iteration
    simple_gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.0)
    noisy_gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.2)

    discount = 0.95
    tolerance = 0.1
    value_iteration(simple_gw, discount, tolerance)
    # Run value iteration (will work after you implement value_iteration + env TODOs)
    # value_iteration(simple_gw, discount, tolerance)
    # print(simple_gw)

    # value_iteration(noisy_gw, discount, tolerance)
    # print(noisy_gw)

    print("=" * 60)
    print("LINEAR SYSTEM SOLVER (deterministic, discount=0.95)")
    print("=" * 60)
    gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.0)
    gw.solve_linear_system(discount_factor=0.95)
    print(gw)

    print("=" * 60)
    print("LINEAR SYSTEM SOLVER (deterministic, discount=0.75)")
    print("=" * 60)
    gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.0)
    gw.solve_linear_system(discount_factor=0.75)
    print(gw)

    print("=" * 60)
    print("VALUE ITERATION (deterministic, discount=0.95)")
    print("=" * 60)
    gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.0)
    value_iteration(gw, discount=0.95, tolerance=0.01)
    print(gw)

    print("=" * 60)
    print("VALUE ITERATION (deterministic, discount=0.75)")
    print("=" * 60)
    gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.0)
    value_iteration(gw, discount=0.75, tolerance=0.01)
    print(gw)

    print("=" * 60)
    print("VALUE ITERATION (noisy=0.2, discount=0.95)")
    print("=" * 60)
    gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], blocked=[6, 7, 11, 12], noise=0.2)
    value_iteration(gw, discount=0.95, tolerance=0.01)
    print(gw)
    
