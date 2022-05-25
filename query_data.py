import requests

import matplotlib.pyplot as plt
import pandas as pd

from clean_data import convert_to_sec
from plot_tools import plot_time_hist, plot_ranked_participants


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
    results["SWIM"] = results["SWIM"].map(convert_to_sec)
    results["T1"] = results["T1"].map(convert_to_sec)
    results["BIKE"] = results["BIKE"].map(convert_to_sec)
    results["T2"] = results["T2"].map(convert_to_sec)
    results["Run"] = results["Run"].map(convert_to_sec)
    results["Chip Time"] = results["Chip Time"].map(convert_to_sec)
    results["Clock Time"] = results["Clock Time"].map(convert_to_sec)


def plot_results(results):
    my_results = results[results["Last Name"] == "Staiger"]
    # graphs = ["SWIM", "T1", "BIKE", "T2", "Run", "Chip Time"]
    graphs = ["SWIM", "BIKE", "Run", "Chip Time"]
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
            plot_ranked_participants(
                # plot_time_hist(
                data,
                my_results[g].values[0],
                ax[ax_row][ax_col],
                f"{g} {f_name}",
            )
            print(f"Fastest {f_name} {g} {data[data == min(data)]}.")
            ax_col += 1
        ax_row += 1

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    results = get_tri_data()
    clean_results(results)
    # compare_result(results)
    plot_results(results)
