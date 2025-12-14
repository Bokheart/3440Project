# Experimental Analysis of Knapsack Problem Algorithms: Dynamic Programming vs. Greedy

## 🚀 Project Overview

This project provides an experimental comparison of two major approaches to solving the classic **0/1 Knapsack Problem (KP)**: the exact **Dynamic Programming (DP)** algorithm and the heuristic **Greedy Algorithm**.

The analysis focuses on the trade-offs between **Solution Quality** (Optimality Gap), **Computational Efficiency** (Runtime), and **Resource Consumption** (Memory Usage) across different scales ($N$ items) and constraints ($W$ capacity).

## ▶️ Quick Launch (Run on Binder)

Click the button below to launch the project's analysis code in a cloud-based JupyterLab environment. No local installation is required.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Bokheart/3440Project/main?urlpath=lab/tree/src/plot_results.ipynb)

### How to Run

1.  Click the **Binder badge** above.
2.  Wait for the environment to build and launch (the JupyterLab interface will open).
3.  The file `src/plot_results.ipynb` should automatically open.
4.  Execute all cells in the Notebook sequentially to:
    * Read the CSV data from `data/results/`.
    * Calculate the Optimality Gap.
    * Generate and save the six comparison charts in the project directory.

## 📁 Repository Structure

The project structure ensures proper relative path handling in the Notebook:
