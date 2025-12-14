import pandas as pd
import os

# Greedy Knapsack Algorithm
def knapsack_greedy(weights, values, W):
    # Step 1: Calculate the value-to-weight ratio for each item
    n = len(weights)
    ratio = [(values[i] / weights[i], weights[i], values[i]) for i in range(n)]  # (value/weight ratio, weight, value)
    
    # Step 2: Sort items based on the value-to-weight ratio in descending order
    ratio.sort(reverse=True, key=lambda x: x[0])  # Sort by value-to-weight ratio
    
    total_value = 0  # Total value of items in the knapsack
    total_weight = 0  # Total weight in the knapsack
    
    # Step 3: Add items to the knapsack
    for r in ratio:
        if total_weight + r[1] <= W:  # If the item can fit in the remaining space
            total_weight += r[1]
            total_value += r[2]
        else:
            break  # If the item cannot fit, stop adding items
    
    return total_value

# Load data from CSV file
def load_data_from_csv(file_path):
    # Use pandas to read the CSV file
    df = pd.read_csv(file_path)

    # Convert weight and value columns to lists
    weights = df['weight'].tolist()
    values = df['value'].tolist()

    # Get backpack capacity from the user
    W = int(float(input(f"Please enter the capacity of the backpack for dataset {file_path}: ")))  # Force conversion to integer
    
    return weights, values, W

# Function for automating tests on multiple datasets in a directory
def test_multiple_datasets_in_directory(directory_path):
    # List all files in the directory
    file_paths = [f for f in os.listdir(directory_path) if f.endswith('.csv')]  # Filter CSV files
    
    for file_name in file_paths:
        file_path = os.path.join(directory_path, file_name)  # Get the full path of the CSV file
        print(f"\nTesting dataset: {file_path}")
        
        # Load the data from CSV file
        weights, values, W = load_data_from_csv(file_path)
        
        # Calculate the maximum value using greedy knapsack algorithm
        max_value = knapsack_greedy(weights, values, W)
        
        # Output the result
        print(f"Maximum value for {file_name}: {max_value}")

# Main function to run automated tests
if __name__ == "__main__":
    # Specify the directory where the datasets are stored
    directory_path = 'datasets'  # Replace with your directory path containing CSV files

    # Run the automated testing on multiple datasets in the specified directory
    test_multiple_datasets_in_directory(directory_path)
