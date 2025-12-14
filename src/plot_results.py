import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Set Plotting Style ---
# ... (其他代码保持不变)

# --- 2. Read Data from CSV Files ---

# Dataset 1: Changes with Number of Items (n_items)
# Corresponding file path: ../data/results/Exact_Baseline_Summary_Final.csv
try:
    # Use relative path to access data in the 'data/results' folder
    df_baseline = pd.read_csv('../data/results/Exact_Baseline_Summary_Final.csv')
    print("✅ Successfully read Exact_Baseline_Summary_Final.csv")
except FileNotFoundError:
    print("❌ Error: Exact_Baseline_Summary_Final.csv not found. Check path: ../data/results/")
    df_baseline = pd.DataFrame() 

# Dataset 2: Changes with Knapsack Capacity (W)
# Corresponding file path: ../data/results/W_sensitivity_results.csv
try:
    # Use relative path to access data in the 'data/results' folder
    df_sensitivity = pd.read_csv('../data/results/W_sensitivity_results.csv')
    # Dynamically calculate Optimality Gap
    # Formula: Gap = (Exact_DP_Value - Greedy_Value) / Exact_DP_Value * 100
    df_sensitivity['Optimality_Gap'] = (
        (df_sensitivity['Exact_DP_Value'] - df_sensitivity['Greedy_Value']) / 
        df_sensitivity['Exact_DP_Value'] * 100
    )
    print("✅ Successfully read W_sensitivity_results.csv and calculated Optimality_Gap")
except FileNotFoundError:
    print("❌ Error: W_sensitivity_results.csv not found. Check path: ../data/results/")
    df_sensitivity = pd.DataFrame()

# ... (后续的绘图函数和执行代码保持不变)

# Dataset 2: Changes with Knapsack Capacity (W)
# Corresponding file: W_sensitivity_results.csv (fixed n=200)
try:
    # Using relative path for GitHub/Jupyter portability
    df_sensitivity = pd.read_csv('W_sensitivity_results.csv')
    # Dynamically calculate Optimality Gap
    # Formula: Gap = (Exact_DP_Value - Greedy_Value) / Exact_DP_Value * 100
    df_sensitivity['Optimality_Gap'] = (
        (df_sensitivity['Exact_DP_Value'] - df_sensitivity['Greedy_Value']) / 
        df_sensitivity['Exact_DP_Value'] * 100
    )
    print("✅ Successfully read W_sensitivity_results.csv and calculated Optimality_Gap")
except FileNotFoundError:
    print("❌ Error: W_sensitivity_results.csv not found.")
    df_sensitivity = pd.DataFrame() # Create empty DataFrame to prevent downstream errors

# --- 3. Plotting Function ---
def plot_comparison(df, x_col, y1_col, y2_col, title, x_label, y_label, save_name):
    # Use figsize to ensure consistent plot size
    plt.figure(figsize=(8, 5))
    
    # Plot the two lines
    plt.plot(df[x_col], df[y1_col], **STYLE_DP)
    plt.plot(df[x_col], df[y2_col], **STYLE_GREEDY)
    
    # Set labels and title
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(save_name, dpi=300)

# --- 4. Independent Function for Optimality Gap Plot ---
def plot_optimality_gap(df, x_col, y_col, threshold, save_name):
    plt.figure(figsize=(8, 5))

    # Plot Gap line chart
    plt.plot(df[x_col], df[y_col], **STYLE_GAP)

    # Add critical threshold dashed line
    plt.axhline(y=threshold, color='gray', linestyle='--', alpha=0.7, label=f'Critical Threshold ({threshold}%)')

    # Annotate the highest point
    if not df.empty:
        max_gap = df[y_col].max()
        max_w = df.loc[df[y_col].idxmax(), x_col]
        # Optimize annotation position to avoid overlap
        plt.annotate(f'Max Gap: {max_gap:.2f}%', 
                     xy=(max_w, max_gap), 
                     xytext=(max_w, max_gap + 5), # Offset upwards slightly
                     ha='center', # Horizontal center alignment
                     arrowprops=dict(facecolor='black', shrink=0.05, width=0.5, headwidth=8))


    # Set labels and title
    plt.title('Weakness of Greedy Algorithm: Optimality Gap vs. Capacity (W)', fontsize=14, fontweight='bold')
    plt.xlabel('Capacity (W)', fontsize=12)
    plt.ylabel('Optimality Gap (%)', fontsize=12)
    # Dynamically set y-axis limits to ensure max point and threshold are visible
    plt.ylim(0, max(max_gap + 10, threshold + 5)) 
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save the figure
    plt.tight_layout()
    plt.savefig(save_name, dpi=300)


# ==========================================
# First set of plots: Changes with Number of Items (n_items)
# ==========================================
if not df_baseline.empty:
    print("\n--- Generating First Set of Plots (Baseline Analysis) ---")

    # 1.1 Value vs Items
    plot_comparison(df_baseline, 'n_items', 'Exact_DP_Value', 'Greedy_Value',
                    'Total Value vs. Number of Items', 'Number of Items (n)', 'Total Value',
                    'value_vs_items.png')

    # 1.2 Runtime vs Items
    plot_comparison(df_baseline, 'n_items', 'Exact_Runtime_sec', 'Greedy_Runtime_sec',
                    'Runtime vs. Number of Items', 'Number of Items (n)', 'Runtime (seconds)',
                    'runtime_vs_items.png')

    # 1.3 Memory vs Items
    plot_comparison(df_baseline, 'n_items', 'Exact_Memory_KB', 'Greedy_Memory_KB',
                    'Memory Usage vs. Number of Items', 'Number of Items (n)', 'Memory Usage (KB)',
                    'memory_vs_items.png')
    print("✅ First set of plots generated and saved")

# ==========================================
# Second set of plots: Changes with Capacity (W)
# ==========================================
if not df_sensitivity.empty:
    print("\n--- Generating Second Set of Plots (Sensitivity Analysis) ---")

    # 2.1 Value vs Capacity
    plot_comparison(df_sensitivity, 'W', 'Exact_DP_Value', 'Greedy_Value',
                    'Solution Value vs. Capacity (W)', 'Capacity (W)', 'Total Value',
                    'value_vs_capacity.png')

    # 2.2 Runtime vs Capacity
    plot_comparison(df_sensitivity, 'W', 'Exact_Runtime_sec', 'Greedy_Runtime_sec',
                    'Runtime vs. Capacity (W)', 'Capacity (W)', 'Runtime (seconds)',
                    'runtime_vs_capacity.png')

    # 2.3 Memory vs Capacity
    plot_comparison(df_sensitivity, 'W', 'Exact_Memory_KB', 'Greedy_Memory_KB',
                    'Memory Usage vs. Capacity (W)', 'Capacity (W)', 'Memory Usage (KB)',
                    'memory_vs_capacity.png')

    # 2.4 Optimality Gap vs Capacity (New Plot)
    plot_optimality_gap(df_sensitivity, 'W', 'Optimality_Gap', 20, 
                        'optimality_gap_vs_capacity.png')

    print("✅ Second set of plots (including Optimality Gap) generated and saved")
