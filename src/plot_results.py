import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. CONFIGURATION AND FILE PATHS ---

# Define file paths based on the new repository structure
BASE_SUMMARY_PATH = 'data/results/Exact_Baseline_Summary_Final.csv' 
SENSITIVITY_PATH = 'data/results/W_sensitivity_results.csv' 

# Set up plotting style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12, 'figure.figsize': (8, 5)})

# Define common styles for DP and Greedy lines
STYLE_DP = {'color': 'blue', 'marker': 'o', 'label': 'Exact (DP)'}
STYLE_GREEDY = {'color': 'orange', 'marker': 's', 'label': 'Greedy'}


# --- 2. DATA LOADING ---

def load_data(file_path):
    """Safely loads data from a CSV file."""
    try:
        # Assuming the files are converted to CSV for simplicity and robust loading
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: Data file not found at {file_path}. Please check your repository structure.")
        raise

# Load the two main datasets
try:
    df_baseline = load_data(BASE_SUMMARY_PATH)
    df_sensitivity = load_data(SENSITIVITY_PATH)
except:
    # Exit if data cannot be loaded, as the plots cannot be generated
    exit() 


# --- 3. DATA PROCESSING: CALCULATING THE CRITICAL GAP ---

# Calculate Optimality Gap for the sensitivity analysis (W variation)
# Gap (%) = (DP_Value - Greedy_Value) / DP_Value * 100
df_sensitivity['Optimality_Gap'] = (df_sensitivity['Exact_DP_Value'] - df_sensitivity['Greedy_Value']) / df_sensitivity['Exact_DP_Value'] * 100


# --- 4. PLOTTING FUNCTIONS ---

def plot_comparison(df, x_col, y1_col, y2_col, title, x_label, y_label, save_name):
    """Plots Runtime, Memory, or Value comparison between DP and Greedy."""
    plt.figure()
    
    # Plot two lines
    plt.plot(df[x_col], df[y1_col], **STYLE_DP)
    plt.plot(df[x_col], df[y2_col], **STYLE_GREEDY)
    
    # Set labels and title
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Save image
    plt.tight_layout()
    plt.savefig(save_name, dpi=300)
    plt.close() # Close plot to free memory


def plot_optimality_gap(df, save_name):
    """Generates the critical Figure 7: Optimality Gap vs. Capacity."""
    plt.figure()
    
    # Plot line, using red to highlight the gap
    plt.plot(df['W'], df['Optimality_Gap'], 
             color='red', marker='D', linestyle='-', linewidth=2, markersize=8, label='Optimality Gap (%)')

    # Add 20% dashed line (the professor's critical threshold)
    plt.axhline(y=20, color='gray', linestyle='--', alpha=0.7, label='Critical Threshold (20%)')

    # Annotate the highest point (W=120)
    max_gap = df['Optimality_Gap'].max()
    max_w = df.loc[df['Optimality_Gap'].idxmax(), 'W']
    plt.annotate(f'Max Gap: {max_gap:.1f}%', 
                 xy=(max_w, max_gap), 
                 xytext=(max_w + 20, max_gap + 2),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    # Set labels and title
    plt.title('Weakness of Greedy Algorithm: Optimality Gap vs. Capacity', fontsize=14, fontweight='bold')
    plt.xlabel('Capacity (W)', fontsize=12)
    plt.ylabel('Optimality Gap (%)', fontsize=12)
    plt.ylim(0, 30) # Fix y-axis range to make the 22.5% spike clear
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save image
    plt.tight_layout()
    plt.savefig(save_name, dpi=300)
    plt.close()


# --- 5. EXECUTION ---

if __name__ == "__main__":
    print("--- Generating Baseline Analysis Plots (Figure 1-3) ---")

    # 5.1 Analysis by Number of Items (n_items)
    plot_comparison(df_baseline, 'n_items', 'Exact_DP_Value', 'Greedy_Value',
                    'Total Value vs. Number of Items (W=480)', 'Number of Items (n)', 'Total Value',
                    'Figure_1_value_vs_items.png')

    plot_comparison(df_baseline, 'n_items', 'Exact_Runtime_sec', 'Greedy_Runtime_sec',
                    'Runtime vs. Number of Items (W=480)', 'Number of Items (n)', 'Runtime (seconds)',
                    'Figure_2_runtime_vs_items.png')

    plot_comparison(df_baseline, 'n_items', 'Exact_Memory_KB', 'Greedy_Memory_KB',
                    'Memory Usage vs. Number of Items (W=480)', 'Number of Items (n)', 'Memory Usage (KB)',
                    'Figure_3_memory_vs_items.png')

    print("\n--- Generating Sensitivity Analysis Plots (Figure 4-7) ---")

    # 5.2 Analysis by Capacity (W)
    plot_comparison(df_sensitivity, 'W', 'Exact_DP_Value', 'Greedy_Value',
                    'Solution Value vs. Capacity (n=200)', 'Capacity (W)', 'Total Value',
                    'Figure_4_value_vs_capacity.png')

    plot_comparison(df_sensitivity, 'W', 'Exact_Runtime_sec', 'Greedy_Runtime_sec',
                    'Runtime vs. Capacity (n=200)', 'Capacity (W)', 'Runtime (seconds)',
                    'Figure_5_runtime_vs_capacity.png')

    plot_comparison(df_sensitivity, 'W', 'Exact_Memory_KB', 'Greedy_Memory_KB',
                    'Memory Usage vs. Capacity (n=200)', 'Capacity (W)', 'Memory Usage (KB)',
                    'Figure_6_memory_vs_capacity.png')
    
    # 5.3 Critical Optimality Gap Plot (Figure 7)
    plot_optimality_gap(df_sensitivity, 'Figure_7_optimality_gap.png')
    
    print("\n✅ All 7 figures have been generated and saved.")