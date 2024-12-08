import matplotlib.pyplot as plt
import re

# Function to parse the text file
def parse_file(file_path):
    grid_data = {}

    # Read the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex pattern to match grid size and probabilities
    grid_pattern = r"Grid size (\d+x\d+):\s*((?:\s*Probability (\d\.\d): Success rate = (\d+\.\d+)%\, Avg execution time = (\d+\.\d+) seconds\s*)+)"
    
    matches = re.findall(grid_pattern, content)

    for match in matches:
        grid_size = match[0]
        data = match[1]
        
        # Extracting each probability, success rate, and execution time
        probabilities = []
        success_rates = []
        execution_times = []
        
        probability_pattern = r"Probability (\d\.\d): Success rate = (\d+\.\d+)%\, Avg execution time = (\d+\.\d+) seconds"
        prob_matches = re.findall(probability_pattern, data)
        
        for prob_match in prob_matches:
            probabilities.append(float(prob_match[0]))
            success_rates.append(float(prob_match[1]))
            execution_times.append(float(prob_match[2]))
        
        grid_data[grid_size] = {
            'probabilities': probabilities,
            'success_rates': success_rates,
            'execution_times': execution_times
        }
    
    return grid_data

# Function to plot execution times for different grid sizes in a single diagram
def plot_execution_times(grid_data):
    plt.figure(figsize=(10, 6))

    # Plot execution times for each grid size
    for grid_size, data in grid_data.items():
        plt.plot(data['probabilities'], data['execution_times'], marker='o', label=f"Grid size {grid_size}")

    # Add labels, title, and legend
    plt.title("Execution Time vs. Probability for Different Grid Sizes")
    plt.xlabel("Probability")
    plt.ylabel("Avg Execution Time (seconds)")
    plt.legend(title="Grid Sizes")
    plt.grid(True)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

# # Main function to execute the script
# def main():
#     file_path = 'test_results.txt'  # Path to your text file containing the results
#     grid_data = parse_file(file_path)
#     plot_execution_times(grid_data)

# if __name__ == "__main__":
#     main()
# Function to plot success rates for different grid sizes in a single diagram
def plot_success_rates(grid_data):
    plt.figure(figsize=(10, 6))

    # Plot success rates for each grid size
    for grid_size, data in grid_data.items():
        plt.plot(data['probabilities'], data['success_rates'], marker='o', label=f"Grid size {grid_size}")

    # Add labels, title, and legend
    plt.title("Success Rate vs. Probability for Different Grid Sizes")
    plt.xlabel("Probability")
    plt.ylabel("Success Rate (%)")
    plt.legend(title="Grid Sizes")
    plt.grid(True)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

# Main function to execute the script
def main():
    file_path = 'test_results.txt'  # Path to your text file containing the results
    grid_data = parse_file(file_path)
    plot_success_rates(grid_data)

if __name__ == "__main__":
    main()