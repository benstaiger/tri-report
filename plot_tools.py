import datetime
import bisect
import itertools

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def time_ticks(x, _):
    d = datetime.timedelta(seconds=x)
    return str(d)


def plot_time_hist(data, line, axis, prefix):
    formatter = matplotlib.ticker.FuncFormatter(time_ticks)
    axis.yaxis.set_major_formatter(formatter)
    sorted_values = sorted([d for d in data if d != 0])
    axis.hist(sorted_values, 50)
    ranked = bisect.bisect_left(sorted_values, line) + 1  # 1-based index
    axis.set_title(
        f"{prefix} Rank {ranked}/{len(data)} "
        f"({np.round(100 - ranked/len(data)*100)}%-tile)"
    )
    axis.set_xlabel("Time")
    axis.set_ylabel("# of Competitors")
    axis.axvline(
        x=line, color="r", linestyle="dashed", linewidth=2,
    )


def plot_ranked_participants(data, line, axis, prefix):
    sorted_values = sorted([d for d in data if d != 0])
    formatter = matplotlib.ticker.FuncFormatter(time_ticks)
    axis.yaxis.set_major_formatter(formatter)
    axis.plot(
        np.arange(1, len(sorted_values) + 1),  # 1-based index
        sorted_values,
        # drawstyle="steps-post",
    )
    ranked = bisect.bisect_left(sorted_values, line) + 1
    axis.set_title(
        f"{prefix} Rank {ranked}/{len(data)} "
        f"({np.round(100 - ranked/len(data)*100):0.0f}%-tile)"
    )
    axis.set_xlabel("Rank")
    axis.set_ylabel("Time Taken")
    axis.axhline(
        y=line, color="r", linestyle="dashed", linewidth=1,
    )


def create_timeseries(result, distances):
    order = ["SWIM", "T1", "BIKE", "T2", "Run"]
    distance_covered = itertools.accumulate([distances[d] for d in order])
    time_taken = itertools.accumulate([result[d] for d in order])
    return list(time_taken), list(distance_covered)


def compare_result(results):
    my_results = results[results["Last Name"] == "Staiger"].iloc[0]
    top = results[results["Place"] == 1].iloc[0]
    distances = {
        "SWIM": 0.4,
        "T1": 0,
        "BIKE": 25,
        "T2": 0,
        "Run": 5,
    }
    my_result = create_timeseries(my_results, distances)
    top_result = create_timeseries(top, distances)
    # Maybe a relative ranking over time / section would be more easily read?
    plt.plot(my_result[0], my_result[1], drawstyle="steps-post")
    plt.plot(top_result[0], top_result[1], drawstyle="steps-post")
    plt.show()
