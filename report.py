import matplotlib.pyplot as plt

from plot_tools import plot_ranked_participants
from run_sign_up import get_tri_data


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
    plot_results(results)
