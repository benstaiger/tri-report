import requests

import pandas as pd

from clean_data import convert_to_sec


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
    clean_runsignup_results(results)
    return results


def clean_runsignup_results(results):
    results["SWIM"] = results["SWIM"].map(convert_to_sec)
    results["T1"] = results["T1"].map(convert_to_sec)
    results["BIKE"] = results["BIKE"].map(convert_to_sec)
    results["T2"] = results["T2"].map(convert_to_sec)
    results["Run"] = results["Run"].map(convert_to_sec)
    results["Chip Time"] = results["Chip Time"].map(convert_to_sec)
    results["Clock Time"] = results["Clock Time"].map(convert_to_sec)
