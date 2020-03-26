import pandas as pd
import numpy as np
import itertools
import argparse


class AMS:


"""
Author: Tania Lopez-Cantu
E-mail: tlopez@andrew.cmu.edu

#############################
Purpose


This class contains methods to clean a timeseries, and an implementation of
the fixed maxima and sliding
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

    def __init__(self, *args, **kwargs):

        pd.read_csv.__init__(self, *args, **kwargs)

    def reformat(self, path):
        ts = pd.read_csv(path, index_col=0, parse_dates=['date'])
        self.reformat = ts.drop(['qflags', 'mflags'], axis=1)
        return self.reformat

    def sliding_max(self, k, data):
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
        self.sliding_max = max(agg_values)
        return self.sliding_max

    def fixed_max(self, k, data):
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
        self.fixed_max = maxx(agg_values)
        return self.fixed_max
