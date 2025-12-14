# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 21:37:42 2025

@author: lenovo
"""

import os
import time
import pandas as pd
import tracemalloc

from DP import knapsack_dp   

DATA_DIR = "datasets"

def load_csv(path):
    df = pd.read_csv(path)
    weights = df["weight"].tolist()
    values = df["value"].tolist()
    return weights, values

def run_one(dataset_file, W, repeats=3, use_memory=True):
    path = os.path.join(DATA_DIR, dataset_file)
    weights, values = load_csv(path)

    if use_memory:
        tracemalloc.start()

    times = []
    ans = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        ans = knapsack_dp(weights, values, W)
        t1 = time.perf_counter()
        times.append(t1 - t0)

    avg_time = sum(times) / len(times)

    peak_kb = ""
    if use_memory:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_kb = peak / 1024

    return ans, avg_time, peak_kb

def main():
    datasets = [
        "knapsack_instance_50.csv",
        "knapsack_instance_100.csv",
        "knapsack_instance_150.csv",
        "knapsack_instance_200.csv",
        "knapsack_instance_300.csv",
        "knapsack_instance_500.csv",
    ]

    W = 480
    results = []

    for f in datasets:
        print(f"\n[DP] Running on {f} ...")
        value, avg_time, peak_kb = run_one(f, W, repeats=3, use_memory=True)

        n_items = int(f.split("_")[-1].split(".")[0])
        results.append({
            "Dataset": f.replace(".csv", ""),
            "n_items": n_items,
            "Capacity_W": W,
            "Exact_DP_Value": value,
            "Exact_Runtime_sec": avg_time,
            "Exact_Memory_KB": peak_kb,
        })

    out = pd.DataFrame(results)
    out.to_csv("DP_runtime_summary.csv", index=False)
    print("\n✅ Saved: DP_runtime_summary.csv")

if __name__ == "__main__":
    main()
