import pandas as pd
import os

def knapsack_dp(weights, values, W):
    """
    Dynamic Programming algorithm for 0/1 Knapsack.
    weights: list of item weights (must be integers)
    values: list of item values
    W: capacity of the knapsack (integer)
    """
    # Error handling: check the validity of the input data
    if len(weights) != len(values):
        raise ValueError("weights and values list lengths must match")
    if not isinstance(W, int) or W < 0:
        raise ValueError("backpack capacity W must be a non-negative integer")
    
    # Number of items
    n = len(weights)
    
    # Initialize the DP table: dp[i][w] represents the maximum value
    # for the first i items with capacity w
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):          # Iterate through each item
        for w in range(W + 1):         # Iterate through each possible capacity
            if weights[i - 1] <= w:    # If the item can be included
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )
            else:                      # If the item cannot be included
                dp[i][w] = dp[i - 1][w]
    
    # Return the maximum value for all items and full capacity
    return dp[n][W]

def load_data_from_csv(file_path):
    """
    Load weights and values from a CSV file.
    CSV must contain at least two columns: 'weight' and 'value'.
    """
    # Use pandas to read the CSV file
    df = pd.read_csv(file_path)

    # Convert weight and value columns to lists
    if 'weight' not in df.columns or 'value' not in df.columns:
        raise ValueError(f"File {file_path} must contain 'weight' and 'value' columns.")
    
    weights = df['weight'].tolist()
    values = df['value'].tolist()

    # Ensure all weights are integers (required for DP indexing)
    try:
        weights = [int(w) for w in weights]
    except ValueError:
        raise ValueError(f"All weights must be integers in file {file_path}.")

    # Get backpack capacity from the user and ensure it is an integer
    W = int(float(input(f"Please enter the capacity of the backpack for dataset {file_path}: ")))
    
    return weights, values, W

def test_multiple_datasets_in_directory(directory_path):
    """
    Automatically test the DP knapsack algorithm on all CSV files
    in the given directory.
    """
    # List all CSV files in the directory
    file_names = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    
    if not file_names:
        print(f"No CSV files found in directory: {directory_path}")
        return
    
    # Sort file names to have a stable order
    file_names.sort()

    # Test each CSV file
    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        print("\n==============================")
        print(f"Testing dataset: {file_path}")
        
        try:
            # Load data
            weights, values, W = load_data_from_csv(file_path)
            
            # Run DP knapsack
            max_value = knapsack_dp(weights, values, W)
            
            # Print results
            print(f"Capacity: {W}")
            print(f"Maximum value of the knapsack (DP): {max_value}")
        
        except ValueError as e:
            print(f"Error in dataset {file_name}: {e}")

# Main entry (works in script; in Jupyter you can just call the function directly)
if __name__ == "__main__":
    # Use current directory '.' or a specific folder like 'datasets'
    directory_path = "datasets"   
    
    test_multiple_datasets_in_directory(directory_path)
