import gtpyhop
import random
import time



domain_name = "Cliff Walking"
the_domain = gtpyhop.Domain(domain_name)
# Function to generate a random grid layout with cliffs
def generate_grid(grid_size):
    cliffs = [(row, col) for row in range(1, grid_size-1) for col in range(1, grid_size-1)]
    return cliffs

# Function to generate a random valid goal location
def generate_goal_location(grid_size, cliffs):
    while True:
        goal_x = random.randint(0, grid_size - 1)
        goal_y = random.randint(0, grid_size - 1)
        if (goal_x, goal_y) not in cliffs:
            return (goal_x, goal_y)

# Actions for moving in different direc
# tions
def move_up(state, agent, to_loc, move_wrongly_probability):
    if random.random() < move_wrongly_probability:  
        next_loc = (to_loc[0] + 1, to_loc[1]-1)  # Move right instead of up
        state.loc[agent] = next_loc
    else:
        state.loc[agent] = to_loc
    return state

def move_down(state, agent, to_loc, move_wrongly_probability):
    if random.random() < move_wrongly_probability:  
        next_loc = (to_loc[0], to_loc[1]+2)  # Move up instead of down
        state.loc[agent] = next_loc
    else:
        state.loc[agent] = to_loc
    return state

def move_left(state, agent, to_loc, move_wrongly_probability):
    if random.random() < move_wrongly_probability:  
        next_loc = (to_loc[0] - 1, to_loc[1]-1)  # Move down instead of left
        state.loc[agent] = next_loc
    else:
        state.loc[agent] = to_loc
    return state

def move_right(state, agent, to_loc, move_wrongly_probability):
    if random.random() < move_wrongly_probability: 
        next_loc = (to_loc[0] - 2, to_loc[1])  # Move left instead of right
        state.loc[agent] = next_loc
    else:
        state.loc[agent] = to_loc
    return state
# Declare actions for each direction with move_wrongly_probability as a parameter
gtpyhop.declare_actions(move_up, move_down, move_left, move_right)

# Task for moving forward
def move_forward(state, agent, goal_loc, move_wrongly_probability):
    current_loc = state.loc[agent]
    if current_loc == goal_loc:
        return [('do_nothing', 'agent', f"({current_loc[0]}, {current_loc[1]})")]  # If already at the goal, do nothing

    plan = []

    # Move in the direction of the goal if it's valid
    if current_loc[0] < goal_loc[0]:  # Move right
        next_loc = (current_loc[0] + 1, current_loc[1])
        plan.append(('move_right', 'agent', next_loc, move_wrongly_probability))
    elif current_loc[1] < goal_loc[1]:  # Move up
        next_loc = (current_loc[0], current_loc[1] + 1)
        plan.append(('move_up', 'agent', next_loc, move_wrongly_probability))  
    elif current_loc[0] > goal_loc[0]:  # Move left
        next_loc = (current_loc[0] - 1, current_loc[1])
        plan.append(('move_left', 'agent', next_loc, move_wrongly_probability))  
    elif current_loc[1] > goal_loc[1]:  # Move down
        next_loc = (current_loc[0], current_loc[1] - 1)
        plan.append(('move_down', 'agent', next_loc, move_wrongly_probability))  
    plan.append(('move_forward', 'agent', goal_loc, move_wrongly_probability))
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

# Function to run the test for a specific grid size and report success rate and execution time
def test_grid_size(grid_size, move_wrongly_probability, num_trials=10):
    gtpyhop.verbose = 1
    cliffs = generate_grid(grid_size)
    success_count = 0
    total_time = 0

    for _ in range(num_trials):
        goal_loc = generate_goal_location(grid_size, cliffs)

        # Set up the initial state for the agent
        state0 = gtpyhop.State('state0')
        state0.loc = {'agent': (0, 0)}  # Starting position of the agent

        # Run the planner and measure execution time
        start_time = time.time()

        try:
            result = gtpyhop.find_plan(state0, [('move_forward', 'agent', goal_loc, move_wrongly_probability)])
            if result:  # If the result is not empty (plan found), increment success_count
                success_count += 1
        except Exception as e:
            print(f"Error for grid size {grid_size} with goal {goal_loc}: {e}")
        
        end_time = time.time()
        total_time += (end_time - start_time)

    success_rate = (success_count / num_trials) * 100
    avg_time = total_time / num_trials

    return success_rate, avg_time

# Function to test multiple grid sizes with different probabilities
def test_multiple_grid_sizes(grid_sizes=[4, 8, 12, 16, 20, 24], probability_range=(0.1, 0.9), num_trials=10):
    results = {}

    for grid_size in grid_sizes:
        results[grid_size] = {}
        for probability in [round(x * 0.1, 1) for x in range(int(probability_range[0]*10), int(probability_range[1]*10)+1)]:
            success_rate, avg_time = test_grid_size(grid_size, probability, num_trials)
            results[grid_size][probability] = {
                'success_rate': success_rate,
                'avg_time': avg_time
            }
            print(f"Grid size {grid_size}x{grid_size}, Probability {probability:.1f}: Success rate = {success_rate:.2f}%, Average execution time = {avg_time:.4f} seconds")

    return results

# Save the results to a file
def save_results_to_file(results, filename="test_results.txt"):
    with open(filename, 'w') as file:
        for grid_size, grid_results in results.items():
            file.write(f"Grid size {grid_size}x{grid_size}:\n")
            for probability, result in grid_results.items():
                file.write(f"  Probability {probability:.1f}: Success rate = {result['success_rate']:.2f}%, Avg execution time = {result['avg_time']:.4f} seconds\n")
            file.write("\n")
    print(f"Results have been saved to {filename}")

# Run the tests for multiple grid sizes and different probabilities
results = test_multiple_grid_sizes()

# Output the results to a file
save_results_to_file(results)
