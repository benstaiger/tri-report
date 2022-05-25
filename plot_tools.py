import bisect
import itertools

import matplotlib.pyplot as plt
import numpy as np


def plot_time_hist(data, line, axis, prefix):
    axis.hist(data, 50)
    sorted_values = sorted(data)
    ranked = bisect.bisect(sorted_values, line)
    axis.set_title(
        f"{prefix} Rank {ranked}/{len(data)} "
        f"({np.round(100 - ranked/len(data)*100)}%-tile)"
    )
    axis.set_xlabel("Time (seconds)")
    axis.set_ylabel("# of Competitors")
    axis.axvline(
        x=line, color="r", linestyle="dashed", linewidth=2,
    )


def plot_ranked_participants(data, line, axis, prefix):
    sorted_values = sorted(data)
    axis.plot(np.arange(len(sorted_values)), sorted_values, drawstyle="steps-post")
    ranked = bisect.bisect(sorted_values, line)
    axis.set_title(
        f"{prefix} Rank {ranked}/{len(data)} "
        f"({np.round(100 - ranked/len(data)*100):0.0f}%-tile)"
    )
    axis.set_xlabel("Rank")
    axis.set_ylabel("Time Taken (seconds)")
    axis.axvline(
        x=ranked, color="r", linestyle="dashed", linewidth=2,
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
