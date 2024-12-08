import matplotlib.pyplot as plt
import re

# Function to parse the text file and extract data for RLL and RL
def parse_file(file_path):
    rll_execution_times = []
    rl_execution_times = []
    grid_sizes = []

    with open(file_path, 'r') as file:
        content = file.read()

    # Regex to match RLL and RL execution times for each grid size
    pattern = r"(RLL|RL):Grid size (\d+x\d+) - Success rate: \d+\.\d+%, Avg execution time: (\d+\.\d+) seconds"

    # Find all matches of the pattern
    matches = re.findall(pattern, content)

    # Organize execution times by grid size
    for match in matches:
        method, grid_size, execution_time = match
        grid_sizes.append(grid_size)
        
        # Convert execution time to float for plotting
        execution_time = float(execution_time)

        # Separate RLL and RL data
        if method == "RLL":
            rll_execution_times.append(execution_time)
        elif method == "RL":
            rl_execution_times.append(execution_time)

    # Ensure both lists have the same length (filter based on grid size)
    aligned_grid_sizes = list(set(grid_sizes))  # remove duplicates for the x-axis
    aligned_rll_times = []
    aligned_rl_times = []

    for grid_size in aligned_grid_sizes:
        if grid_size in grid_sizes:
            aligned_rll_times.append(rll_execution_times[grid_sizes.index(grid_size)])
            aligned_rl_times.append(rl_execution_times[grid_sizes.index(grid_size)])

    return aligned_grid_sizes, aligned_rll_times, aligned_rl_times

# Function to plot execution times for RLL and RL
def plot_execution_times(grid_sizes, rll_execution_times, rl_execution_times):
    plt.figure(figsize=(10, 6))

    # Plot execution times for RLL and RL
    plt.plot(grid_sizes, rll_execution_times, marker='o', label='RLL', color='b')
    plt.plot(grid_sizes, rl_execution_times, marker='x', label='RL', color='g')

    # Add labels, title, and legend
    plt.title("Execution Time vs. Grid Size for RLL and RL")
    plt.xlabel("Grid Size")
    plt.ylabel("Avg Execution Time (seconds)")
    plt.legend(title="Method")
    plt.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

# Main function to execute the script
def main():
    file_path = 'final_results_combined.txt'  # Path to your text file containing the results
    grid_sizes, rll_execution_times, rl_execution_times = parse_file(file_path)

    # Plot the execution times for RLL and RL
    plot_execution_times(grid_sizes, rll_execution_times, rl_execution_times)

if __name__ == "__main__":
    main()
