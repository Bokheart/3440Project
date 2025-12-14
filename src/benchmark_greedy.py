# -*- coding: utf-8 -*-
"""
Greedy Knapsack Runtime & Memory Benchmark
Created on Fri Dec 12 2025

@author: lenovo
"""

import os
import time
import tracemalloc
import pandas as pd

from Greedy import knapsack_greedy   # 

DATA_DIR = "datasets"


def load_csv(path):
    df = pd.read_csv(path)
    weights = df["weight"].tolist()
    values = df["value"].tolist()
    return weights, values


def run_one(dataset_file, W, repeats=10):
    path = os.path.join(DATA_DIR, dataset_file)
    weights, values = load_csv(path)

    times = []
    ans = None

    # 🔹 开始内存监控
    tracemalloc.start()

    for _ in range(repeats):
        t0 = time.perf_counter()
        ans = knapsack_greedy(weights, values, W)
        t1 = time.perf_counter()
        times.append(t1 - t0)

    # 🔹 获取峰值内存
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    avg_time = sum(times) / len(times)
    peak_kb = peak / 1024  # 转成 KB

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
        print(f"\n[Greedy] Running on {f} ...")

        value, avg_time, peak_mem = run_one(f, W, repeats=20)

        n_items = int(f.split("_")[-1].split(".")[0])

        results.append({
            "Dataset": f.replace(".csv", ""),
            "n_items": n_items,
            "Capacity_W": W,
            "Greedy_Value": value,
            "Greedy_Runtime_sec": avg_time,
            "Greedy_Memory_KB": peak_mem,
        })

    out = pd.DataFrame(results)
    out.to_csv("Greedy_runtime_summary.csv", index=False)

    print("\n✅ Saved: Greedy_runtime_summary.csv")


if __name__ == "__main__":
    main()
