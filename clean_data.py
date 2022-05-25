from itertools import accumulate
import pandas as pd


def format_time_str(s):
    """
    Convert degenerate time strings to something consistently formatted. %H:%M:%S.
    >>> format_time_str("8:0.32")
    00:08:00.32
    """
    print(s)
    sections = s.split(":")

    while len(sections) < 3:
        sections = ["00"] + sections

    for i, sect in enumerate(sections[:-1]):
        assert len(sect) <= 2
        if len(sect) == 1:
            sections[i] = f"0{sect}"

    # Deal with seconds field?
    secs = sections[-1].split(".")
    while len(secs[0]) < 2:
        secs[0] = f"0{secs[0]}"
    secs = ".".join(secs)
    sections[-1] = secs

    return ":".join(sections)

def convert_to_sec(str_time):
    comps = [float(v) for v in str_time.split(":")]
    if len(comps) == 2:
        return comps[0] * 60 + comps[1]
    elif len(comps) == 3:
        return comps[0] * 60 * 60 + comps[1] * 60 + comps[2]
    else:
        raise ValueError(f"Unrecognized time format {str_time}")

def str_to_secs(s):
    """
    Convert a string formatted as %H:%M:%S to a float number of seconds.
    """
    sections = s.split(":")
    assert len(sections) == 3
    return float(sections[0]) * 60 * 60 + float(sections[1]) * 60 + float(sections[2])


def cumulative_time_format(data, columns):
    def convert_row(row):
        times = row[columns].values
        times = list(accumulate(times))
        row[columns] = times
        return row

    return data.apply(convert_row, axis=1)


def convert_columns_to_time(data, columns, inplace=False):
    if not inplace:
        data = data.copy()
    for c in columns:
        data[c] = data[c].map(lambda x: str_to_secs(format_time_str(x)))
    return data
