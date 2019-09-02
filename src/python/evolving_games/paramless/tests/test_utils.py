import os

import numpy as np

from paramless import utils


def test_times_series_io():
    file_name = 'test_out.csv'
    x = np.arange(0, 5, 1, dtype=float)
    y = np.arange(10, 15, 1, dtype=float)

    X, Y = np.meshgrid(x, y, indexing='ij')

    original_time_series = []

    for _ in range(6):
        if (_%2==0):
            original_time_series.append(X)
        else:
            original_time_series.append(Y)

    utils.time_series_to_csv(file_name, original_time_series)
    new_time_series = utils.csv_to_time_series_array(file_name)

    # Cleaning up after myself
    os.remove(file_name)

    for i in range(len(original_time_series)):
        assert original_time_series[i].all() == new_time_series[i].all()
