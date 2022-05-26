import matplotlib.pyplot as plt
import pandas as pd

from plot_tools import plot_ranked_participants
from run_sign_up import get_tri_data


def plot_ranking_results(results, columns):
    my_results = results[results["Last Name"] == "Staiger"].iloc[0]
    filters = {
        "Overall": ~results["Place"].isna(),
        "Gender": results["Gender"] == "M",
        "Age Group": results["Age Group"] == my_results["Age Group"],
    }
    fig, ax = plt.subplots(
        len(filters),
        len(columns),
        figsize=(3 * len(columns), 3 * len(filters)),
    )
    ax_row = 0
    for f_name, f in filters.items():
        ax_col = 0
        for g in columns:
            data = results[g][f].values
            plot_ranked_participants(
                # plot_time_hist(
                data,
                my_results[g],
                ax[ax_row][ax_col],
                f"{g} {f_name}",
            )
            print(f"Fastest {f_name} {g} {data[data == min(data)]}.")
            ax_col += 1
        ax_row += 1

    fig.tight_layout()
    plt.show()


def generate_childrens_tri_2021():
    results = get_tri_data()
    graphs = ["SWIM", "BIKE", "Run", "Chip Time"]
    # TODO: merge age group columns
    plot_ranking_results(results, graphs)


def generate_brickyard_tri_2022():
    results = pd.read_csv("data/processed/brickyard_sprint_2022.csv")
    results["Place"] = results["Overall Rank"]
    results["Age Group"] = results["Age Group"].map(
        lambda x: x.replace("-", "")
    )
    results = results.fillna(0.0)
    print(results.head(6))
    plot_ranking_results(results, ["Swim Time", "Bike Time", "Run Time"])


if __name__ == "__main__":
    generate_brickyard_tri_2022()
