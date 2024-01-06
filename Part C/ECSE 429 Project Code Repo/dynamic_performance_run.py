import os
import subprocess
from threading import Event, Thread
from time import perf_counter, sleep
import time

import pandas as pd
import psutil

from performance.test_categories import (
    test_add_categories,
    test_update_categories,
    test_delete_categories,
)
from performance.test_projects import (
    test_delete_projects,
    test_update_projects,
    test_add_projects,
)
from performance.test_todos import test_delete_todos, test_add_todos, test_update_todos
import numpy as np
PID = -1
get_file_name = lambda description: os.path.join(
    "performance/output/csv",
    "_".join(description.split(" ")[1:]).lower() + "_system_logs.csv",
)
get_graph_name = lambda description: os.path.join(
    "performance/output/graph",
    "_".join(description.split(" ")[1:]).lower() + ".png",
)


def logger(stop_event, description):
    log_data = []
    process = psutil.Process(PID)
    while not stop_event.is_set():
        now = perf_counter()
        cpu_usage = process.cpu_percent()
        used_memory = process.memory_info().rss
        free_memory = psutil.virtual_memory().available
        log_data.append([now, cpu_usage, used_memory, free_memory])
        sleep(0.01)

    log_df = pd.DataFrame(
        log_data,
        columns=["Time", "CPU Usage (%)", "Memory Usage (MB)", "Free Memory (MB)"],
    )
    log_df.to_csv(get_file_name(description), index=False)


import matplotlib.pyplot as plt


def plot_image(df, description, smooth=False):
    MB = 1024 * 1024
    df["Memory Usage (MB)"] = df["Memory Usage (MB)"] / MB
    df["Free Memory (MB)"] = df["Free Memory (MB)"] / MB

    if smooth:
        description += " Smoothed"

    def smooth_curve(y, window_size=5):
        window = np.ones(window_size) / window_size
        smoothed_y = np.convolve(y, window, mode='same')
        return smoothed_y

    fig, ax1 = plt.subplots()
    fig.set_size_inches(8, 4)
    ax2 = ax1.twinx()
    # plt.subplots_adjust(right=0.8)
    ax1.set_title(
        "CPU and Memory Usage for "
        + " ".join(description.split(" ")[1:])
        + " Operation"
    )

    (p1,) = ax1.plot(
        df["Time"].to_numpy(),
        smooth_curve(df["CPU Usage (%)"].to_numpy()) if smooth else df["CPU Usage (%)"].to_numpy(),
        color="tab:blue",
        label="CPU Usage (%)",
        linewidth=0.75
    )
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("CPU Usage (%)")

    (p2,) = ax2.plot(
        df["Time"].to_numpy(),
        df["Memory Usage (MB)"].to_numpy(),
        color="tab:green",
        label="Memory Usage (MB)",
        linewidth=0.75
    )
    # (p3,) = ax2.plot(
    #     df["Time"].to_numpy(),
    #     df["Free Memory (MB)"].to_numpy(),
    #     color="tab:red",
    #     label="Free Memory (MB)",
    #     linewidth=0.75
    # )

    ax1.set(ylabel="CPU Usage (%)", xlabel="Time (s)")#ylim=(-5, 105)
    ax2.set(ylabel="Memory Usage (MB)")
    ax2.grid(True)
    ax1.legend(loc="upper left", labelcolor="linecolor")
    ax2.legend(loc="upper right", labelcolor="linecolor")

    ax1.tick_params(axis="y", colors=p1.get_color())
    ax2.tick_params(axis="y", colors=p2.get_color())
    # ax3.tick_params(axis='y', colors=p3.get_color())

    fig.tight_layout()
    plt.savefig(get_graph_name(description))


def run_test(test_function, description):
    print(f"Starting Test ---- {description} ----")
    stop_logging = Event()
    logger_thread = Thread(target=logger, args=(stop_logging, description))
    test_thread = Thread(target=test_function, args=(None,))
    logger_thread.start()
    test_thread.start()
    test_thread.join()
    stop_logging.set()
    logger_thread.join()

    records = pd.read_csv(get_file_name(description))
    img = records.plot(
        title="CPU Usage for " + " ".join(description.split(" ")[1:]) + " Operation"
    ).get_figure()
    img.savefig(get_graph_name(description))
    plot_image(records, description)
    # plot_image(records, description, True)


def main():
    os.makedirs("performance/output/csv", exist_ok=True)
    os.makedirs("performance/output/graph", exist_ok=True)

    # start server
    subprocess.call(["curl", "http://localhost:4567/shutdown"], shell=True)
    process = subprocess.Popen(["starter.bat"], shell=True)
    status_code = subprocess.call(["curl", "http://localhost:4567"], shell=True)
    while status_code:
        status_code = subprocess.call(["curl", "http://localhost:4567"], shell=True)
        time.sleep(0.1)

    global PID
    PID = psutil.Process(process.pid).children()[0].pid
    # PID debug
    process = psutil.Process(PID)
    print(
        "Server PID", PID, process.name(), process.cpu_percent(), process.memory_info()
    )

    # start tests
    run_test(test_add_todos, "Test Add Todo")
    run_test(test_update_todos, "Test Change Todo")
    run_test(test_delete_todos, "Test Delete Todo")

    run_test(test_add_projects, "Test Add Project")
    run_test(test_update_projects, "Test Change Project")
    run_test(test_delete_projects, "Test Delete Project")

    run_test(test_add_categories, "Test Add Category")
    run_test(test_update_categories, "Test Change Category")
    run_test(test_delete_categories, "Test Delete Category")

    # clean up
    subprocess.call(["curl", "http://localhost:4567/shutdown"], shell=True)
    process.kill()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
