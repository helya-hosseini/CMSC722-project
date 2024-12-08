import gtpyhop
import time
import random

# define domain name
domain_name = "Cliff Walking"
the_domain = gtpyhop.Domain(domain_name)

# Define the grid layout and dangerous positions (cliff)
grid_layout = {
    'start': (0, 0),
    'goal': (7, 7),
    'cliff': [(2, 2), (3, 2), (2, 3)]
}

# Function to check if a location is safe
def is_safe(x, y):
    return (x, y) not in grid_layout['cliff']

# Helper function to calculate distance between two points (Manhattan distance)
def distance(x, y, target_x, target_y):
    return abs(x - target_x) + abs(y - target_y)

# Actions for moving in different directions
def move_up(state, agent, to_loc):
    state.loc[agent] = to_loc
    return state

def move_down(state, agent, to_loc):
    state.loc[agent] = to_loc
    return state

def move_left(state, agent, to_loc):
    state.loc[agent] = to_loc
    return state

def move_right(state, agent, to_loc):
    state.loc[agent] = to_loc
    return state

# Declare actions for each direction
gtpyhop.declare_actions(move_up, move_down, move_left, move_right)

# Task for moving forward
def move_forward(state, agent, goal_loc):
    current_loc = state.loc[agent]
    # print(current_loc)
    if current_loc == goal_loc:
        return [('do_nothing', 'agent', f"({current_loc[0]}, {current_loc[1]})")]  # If already at the goal, do nothing

    plan = []

    # Move in the direction of the goal if it's valid
    if current_loc[0] < goal_loc[0]:  # Move right
        next_loc = (current_loc[0] + 1, current_loc[1])
        plan.append(('move_right', 'agent', next_loc))
    elif current_loc[1] < goal_loc[1]:  # Move up
        next_loc = (current_loc[0], current_loc[1] + 1)
        plan.append(('move_up', 'agent', next_loc))
    elif current_loc[0] > goal_loc[0]:  # Move left
        next_loc = (current_loc[0] - 1, current_loc[1])
        plan.append(('move_left', 'agent', next_loc))
    elif current_loc[1] > goal_loc[1]:  # Move down
        next_loc = (current_loc[0], current_loc[1] - 1)
        plan.append(('move_down', 'agent', next_loc))
    plan.append(('move_forward', 'agent', goal_loc))
    if plan:
        return plan
    else:
        return [('do_nothing', 'agent', current_loc)]

# Task for doing nothing
def do_nothing(state, agent, goal_loc):
    current_loc = state.loc[agent]
    if current_loc == goal_loc:
        return [('do_nothing', 'agent', current_loc)]  # Do nothing if already at the goal
    return []

# Declare task methods
gtpyhop.declare_task_methods('move_forward', move_forward)
gtpyhop.declare_task_methods('do_nothing', do_nothing)

# # Initial state
# state0 = gtpyhop.State('state0')
# state0.loc = {'agent': (0, 0)}  # Starting position of the agent
# goal_loc = grid_layout['goal']

# # Plan to move the agent to the goal
# gtpyhop.verbose = 3
# result = gtpyhop.find_plan(state0, [('move_forward', 'agent', goal_loc)])

# print(result)

# Function to generate a random grid layout with cliffs
def generate_grid(grid_size):
    cliffs = [(1, col) for col in range(1, grid_size-2)] 
    return cliffs

# Function to generate a random valid goal location
def generate_goal_location(grid_size, cliffs):
    while True:
        goal_x = random.randint(0, grid_size - 1)
        goal_y = random.randint(0, grid_size - 1)
        if (goal_x, goal_y) not in cliffs:
            return (goal_x, goal_y)

# Function to run the test for a specific 
# grid size and report success rate and execution time
def test_grid_size(grid_size, num_trials=10):
    gtpyhop.verbose = 1
    cliffs = generate_grid(grid_size)
    success_count = 0
    total_time = 0

    for i in range(num_trials):
        if (i == 0):
            goal_loc = (grid_size-1, grid_size-1)
        else:
            goal_loc = generate_goal_location(grid_size, cliffs)
        
        # Set up the initial state for the agent
        state0 = gtpyhop.State('state0')
        state0.loc = {'agent': (0, 0)}  # Starting position of the agent

        # Run the planner and measure execution time
        start_time = time.time()

        try:
            result = gtpyhop.find_plan(state0, [('move_forward', 'agent', goal_loc)])
            # result = gtpyhop.run_lazy_lookahead(state0, [('move_forward', 'agent', goal_loc)])
            if result:
                success_count += 1  # If plan is found, it's a success
        except Exception as e:
            print(f"Error for grid size {grid_size} with goal {goal_loc}: {e}")
        
        end_time = time.time()
        total_time += (end_time - start_time)

    success_rate = (success_count / num_trials) * 100
    avg_time = total_time / num_trials

    return success_rate, avg_time

# Function to test multiple grid sizes
def test_multiple_grid_sizes(grid_sizes=[4, 8, 12, 16, 20, 24, 32, 36], num_trials=10):
    results = {}

    for grid_size in grid_sizes:
        success_rate, avg_time = test_grid_size(grid_size, num_trials)
        results[grid_size] = {
            'success_rate': success_rate,
            'avg_time': avg_time
        }
        print(f"Grid size {grid_size}x{grid_size}: Success rate = {success_rate:.2f}%, Average execution time = {avg_time:.4f} seconds")

    return results


def write_final_results(results, filename="final_results_RLL.txt"):
    with open(filename, 'w') as file:
        file.write("\nFinal Results RLL:\n")
        for grid_size, result in results.items():
            file.write(f"Grid size {grid_size}x{grid_size} - Success rate: {result['success_rate']:.2f}%, Avg execution time: {result['avg_time']:.4f} seconds\n")
    print(f"Final results written to {filename}")

# Run the tests for multiple grid sizes

results = test_multiple_grid_sizes()

# Output the final results in a readable format
write_final_results(results)
# Output the results in a readable format
print("\nFinal Results RLL:")
for grid_size, result in results.items():
    print(f"Grid size {grid_size}x{grid_size} - Success rate: {result['success_rate']:.2f}%, Avg execution time: {result['avg_time']:.4f} seconds")
