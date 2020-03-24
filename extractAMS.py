"""
File name: extractAMS
Author: Tania Lopez-Cantu
E-mail: tlopez@andrew.cmu.edu

##############################

Purpose:

Generates a csv file with the sliding or fixed maxima per year from a
time series of rainfall observations.

This script contains an implementation of the fixed maxima and sliding
maxima algorithms provided in

Papalexiou, S. M., Dialynas, Y. G., & Grimaldi, S. (2016).
Hershfield factor revisited: Correcting annual maximum precipitation.
Journal of Hydrology, 542, 884–895. https://doi.org/10.1016/j.jhydrol.2016.09.058

These two functions extract the annual maximum precipitation (AMS)
from a precipitation time series. The two approaches arise from the need to account for the
fact that precipitation is systematicall recorded. For example, at a meteorological station,
someone will check the tipping bucket pluviographs at some fixed local time each day which is
then recorded as a "daily rainfall time series" at a particular location. This case results
in "fixed" records, but "fixed" records have been shown inappropriate for
estimating rainfall maxima. Because rainfall is a continuous variable, discretizing it can result
in biases when estimating extreme rainfall, so it is advised to estimate
annual maximum series using the sliding maxima approach.

"""

import pandas as pd
import numpy as np
import itertools
import argparse


def reformat(path):
    ts = pd.read_csv(path, index_col=0, parse_dates=['date'])
    ts.drop(['qflags', 'mflags'], axis=1, inplace=True)
    return ts


def sliding_max(k, data):
    """
    Function to extract AMS from a time series using the sliding maxima approach.

    Parameters
    ----------
    Input:
        k: int, duration over which AMS will be computed. For example, if the data is at an hourly resolution, and
                want to compute the 3-hour AMS, then k=3.
        data: DataFrame, rainfall time series in a pandas two column dataframe format. One column should be the "date"
                of the record (i.e. "1960-05-24 00:00:00" if hourly records), and the second must be the rainfall values.
    """
    tp = data.values
    period = 24*365
    agg_values = []
    start_j = 1
    end_j = k*int(np.floor(period/k))
    for j in range(start_j, end_j + 1):
        start_i = j - 1
        end_i = j + k + 1
        agg_values.append(np.nansum(tp[start_i:end_i]))
    return max(agg_values)


def fixed_max(k, data):
    """
    Function to extract AMS from a time series using the fixed maxima approach.

    Parameters
    ----------
    Input:
        k: int, duration over which AMS will be computed. For example, if the data is at an hourly resolution, and
                want to compute the 3-hour AMS, then k=3.
        data: DataFrame, rainfall time series in a pandas two column dataframe format. One column should be the "date"
                of the record (i.e. "1960-05-24 00:00:00" if hourly records), and the second must be the rainfall values.
    """
    tp = data.values
    period = 24*365
    agg_values = []
    start_j = 1
    end_j = int(np.floor(period/k))
    for j in range(start_j, end_j + 1):
        start_i = (j - 1)*k
        end_i = (j*k)
        agg_values.append(np.nansum(tp[start_i:end_i]))

    return max(agg_values)


def main(args):

    ftype = args.ftype
    print(ftype)
    fpath = args.path

    # Hard coded durations here, but could be input from the user
    durations = [1, 2, 3, 6, 12, 24, 48, 72]

    ts = reformat(fpath)
    ams = pd.DataFrame(ts.date.dt.year.unique())
    ams.columns = ['year']

    if ftype == 'sliding':

        for d in durations:
            ams['{}H'.format(d)] = ts.groupby(pd.Grouper(key='date', freq='A')).agg(
                lambda x: sliding_max(d, x)).values

    if ftype == 'fixed':

        for d in durations:
            ams['{}H'.format(d)] = ts.groupby(pd.Grouper(key='date', freq='A')).agg(
                lambda x: fixed_max(d, x)).values

    ams.to_csv("{}/AMS_{}".format(args.savepath, fpath.split('/')[-1]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Extract the annual maximum precipitation (AMS) from a precipitation time series")

    parser.add_argument("--path", required=True, type=str,
                        help="Full path where the .csv file of hourly rainfall records is located.")
    parser.add_argument("--ftype", required=True, type=str,
                        help="Type of approach. There are only two options: 'sliding' or 'fixed'")
    parser.add_argument("--savepath", required=True, type=str,
                        help="Full path where to save the extracted AMS as a .csv file")

    args = parser.parse_args()

    main(args)
