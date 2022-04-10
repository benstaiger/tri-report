import itertools
import requests
import pandas as pd
from matplotlib import pyplot as plt


def get_runsignup_data(race_id, event_id):
    params = {
        "format": "json",
        "event_id": str(event_id),
        "include_total_finishers": "F",
        "include_split_time_ms": "F",
        "page": "1",
        "results_per_page": "2500",
    }
    response = requests.get(
        f"https://runsignup.com/Rest/race/{race_id}/results/get-results", params=params,
    )
    return response.json()


def get_tri_data():
    """
    Return data from 2021 Tri-ing for Children's Sprint Triathlon
    """
    data = get_runsignup_data(99534, 434161)  # TODO: cache data
    print(len(data["individual_results_sets"][0]["results"]))
    results = pd.DataFrame(data["individual_results_sets"][0]["results"])
    results = results[~results.place.isna()]
    results.rename(
        data["individual_results_sets"][0]["results_headers"], axis=1, inplace=True,
    )
    return results


def clean_results(results):
    def convert_to_sec(str_time):
        comps = [float(v) for v in str_time.split(":")]
        if len(comps) == 2:
            return comps[0] * 60 + comps[1]
        elif len(comps) == 3:
            return comps[0] * 60 * 60 + comps[1] * 60 + comps[2]
        else:
            raise ValueError(f"Unrecognized time format {str_time}")

    results["SWIM"] = results["SWIM"].map(convert_to_sec)
    results["T1"] = results["T1"].map(convert_to_sec)
    results["BIKE"] = results["BIKE"].map(convert_to_sec)
    results["T2"] = results["T2"].map(convert_to_sec)
    results["Run"] = results["Run"].map(convert_to_sec)
    results["Chip Time"] = results["Chip Time"].map(convert_to_sec)
    results["Clock Time"] = results["Clock Time"].map(convert_to_sec)


def create_timeseries(result, distances):
    order = ["SWIM", "T1", "BIKE", "T2", "Run"]
    distance_covered = itertools.accumulate([distances[d] for d in order])
    time_taken = itertools.accumulate([result[d] for d in order])
    return list(time_taken), list(distance_covered)


def compare_result(results):
    my_results = results[results["Last Name"] == "Staiger"].iloc[0]
    top = results[results["Place"] == 1].iloc[0]
    my_results = results[results["Place"] == 2].iloc[0]
    print(my_results)
    print(top)
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
    print(my_result)
    plt.plot(my_result[0], my_result[1])
    plt.plot(top_result[0], top_result[1])
    plt.show()


def plot_results(results):
    def plot_time_hist(data, line, axis, prefix):
        n, bins, patches = axis.hist(data, 50)

        def bin_search(data, x):
            lower = 0
            upper = len(data) - 1
            while lower < upper:
                mid = (lower + upper) // 2
                if data[mid] < x:
                    lower = mid + 1
                elif data[mid] > x:
                    upper = mid - 1
                else:
                    return mid
            return (lower + upper) // 2

        sorted_values = sorted(data)
        ranked = bin_search(sorted_values, line) + 1
        axis.set_title(
            f"{prefix} Ranked {ranked}/{len(data)} " f"({ranked/len(data)*100:.2f}%)"
        )
        axis.set_xlabel("Time (seconds)")
        axis.set_ylabel("# of Competitors")
        axis.axvline(
            x=line, color="r", linestyle="dashed", linewidth=2,
        )

    my_results = results[results["Last Name"] == "Staiger"]

    # graphs = ["SWIM", "BIKE", "Run"]
    graphs = ["SWIM", "T1", "BIKE", "T2", "Run", "Chip Time"]
    filters = {
        "Overall": ~results["Place"].isna(),
        "Gender": results["Gender"] == "M",
        "Age Group": ~results["M2529"].isna(),
    }
    fig, ax = plt.subplots(
        len(filters), len(graphs), figsize=(3 * len(graphs), 3 * len(filters))
    )

    ax_row = 0
    for f_name, f in filters.items():
        ax_col = 0
        for g in graphs:
            data = results[g][f].values
            plot_time_hist(
                data, my_results[g].values[0], ax[ax_row][ax_col], f"{g} {f_name}",
            )
            print(f"Fastest {f_name} {g} {data[data == min(data)]}.")
            ax_col += 1
        ax_row += 1

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    results = get_tri_data()
    clean_results(results)
    compare_result(results)
