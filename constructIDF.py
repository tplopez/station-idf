"""
File name: constructIDF
Author: Tania Lopez-Cantu
E-mail: tlopez@andrew.cmu.edu

##############################

Purpose:

Generate IDF curves from hourly data

"""

from scipy.stats import genextreme as gev
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import argparse
import numpy as np


class AMS:

    """
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

    Type of data accepted:
       DataFrame, rainfall time series in a pandas two column dataframe format. One column should be the "date"
       of the record (i.e. "1960-05-24 00:00:00" if hourly records), and the second must be the rainfall values.
    """

    def __init__(self, path, durations):

        self.path = path
        self.durations = durations
        self.reformat()
        self.output = pd.DataFrame(
            self.reformatted_frame.date.dt.year.unique(), columns=['year'])

    def reformat(self):
        ts = pd.read_csv(self.path, index_col=0, parse_dates=['date'])
        self.reformatted_frame = ts.drop(['qflags', 'mflags'], axis=1)

    def calculate_AMS(self, ams_type):
        """
        Function to extract AMS from a time series.

        Parameters
        ----------
        Input:
            ams_type: str, either "sliding" for sliding maxima or "fixed" for fixed maxima.
        Output:
            rainfall annual maximum series in a pandas two column (year, AMS) dataframe format.
        """

        if ams_type == 'sliding':
            for d in self.durations:
                self.output[f"{d}H"] = self.reformatted_frame.groupby(pd.Grouper(key='date', freq='A')).agg(
                    lambda x: AMS.sliding_max(x, d)).values
        elif ams_type == 'fixed':
            for d in self.durations:
                self.output[f"{d}H"] = self.reformatted_frame.groupby(pd.Grouper(key='date', freq='A')).agg(
                    lambda x: AMS.fixed_max(x, d)).values

        return self.output

    @staticmethod
    def sliding_max(grouped_data, duration):
        """
        Function to extract AMS from a time series using the sliding maxima approach.

        Parameters
        ----------
        Input:
            grouped_data: pandas.core.groupby.Grouper, data grouped by year.
            duration: int, duration over which AMS will be computed. For example, if the data is at an hourly resolution, and
                    want to compute the 3-hour AMS, then k=3.
        Output:
            annual_maximum: float, annual maximum of the group (year).
        """
        tp = grouped_data.values
        period = 24 * 365
        agg_values = []
        start_j = 1
        end_j = duration * int(np.floor(period / duration))
        for j in range(start_j, end_j + 1):
            start_i = j - 1
            end_i = j + duration + 1
            agg_values.append(np.nansum(tp[start_i:end_i]))
        annual_maximum = max(agg_values)
        return annual_maximum

    @staticmethod
    def fixed_max(grouped_data, duration):
        """
        Function to extract AMS from a time series using the fixed maxima approach.

        Parameters
        ----------
        Input:
            grouped_data: pandas.core.groupby.Grouper.
            duration: int, duration over which AMS will be computed. For example, if the data is at an hourly resolution, and
                    want to compute the 3-hour AMS, then k=3.
        Output:
            annual_maximum: float, annual maximum of the group (year).
        """
        tp = grouped_data.values
        period = 24 * 365
        agg_values = []
        start_j = 1
        end_j = int(np.floor(period / duration))
        for j in range(start_j, end_j + 1):
            start_i = (j - 1)*duration
            end_i = (j*duration)
            agg_values.append(np.nansum(tp[start_i:end_i]))
        annual_maximum = max(agg_values)
        return annual_maximum


class IDF:

    """
    This class contains methods to generate IDF curves
    with confidence intervals using scipy genextreme
    library and custom bootstraping function using numpy.random.choice
    """
    # Hard coded durations here but can be specified by the user.

    def __init__(self, path, ci, number_bootstrap, alpha):
        self.ci = ci
        self.alpha = alpha
        self.number_bootstrap = number_bootstrap
        self.quantiles = [1 / 2, 1 / 5, 1 / 10,
                          1 / 25, 1 / 50, 1 / 100, 1 / 200]
        self.no_ci_columns = ['2-yr', '5-yr', '10-yr',
                              '25-yr', '50-yr', '100-yr', '200-yr']

        wci = []

        for bound in ['L', '', 'U']:
            for e in self.no_ci_columns:
                wci.append("{}{}".format(bound, e))
        self.ci_columns = wci

        self.path = path
        self.reformatted_ams()

        if self.ci:
            self.idf = pd.DataFrame(index=self.ci_columns)
        else:
            self.idf = pd.DataFrame(index=self.no_ci_columns)

    def reformatted_ams(self):

        if type(self.path) == str:
            ams = pd.read_csv(self.path, index_col=0)
            self.reformatted_ams = ams.drop(['year'], axis=1)
        elif type(self.path) == type(pd.DataFrame()):
            self.reformatted_ams = self.path.drop(['year'], axis=1)

    def construct_IDF(self):

        if self.ci:
            bts = {}
            for col in self.reformatted_ams.columns:
                mams = []
                for i in range(self.number_bootstrap):
                    bootsams = np.random.choice(
                        self.reformatted_ams[col].values, replace=True, size=len(self.reformatted_ams))
                    fit = gev.fit(bootsams)
                    mams.append(
                        gev.isf(self.quantiles, c=fit[0], loc=fit[1], scale=fit[2]))
                bts[col] = np.asarray(mams)

            p_lo = ((1.0-self.alpha)/2.0) * 100
            p_up = (self.alpha+((1.0-self.alpha)/2.0)) * 100
            for col in self.reformatted_ams.columns:
                lower = np.apply_along_axis(np.percentile, 0, bts[col], p_lo)
                upper = np.apply_along_axis(np.percentile, 0, bts[col], p_up)
                median = np.apply_along_axis(
                    np.percentile, 0, bts[col], 50)
                self.idf[col] = np.append(lower, np.append(median, upper))
        else:

            for col in self.reformatted_ams.columns:
                fit = gev.fit(self.reformatted_ams[col])
                self.idf[col] = gev.isf(self.quantiles, c=fit[0],
                                        loc=fit[1], scale=fit[2])

    def plot_IDF(self, path, figformat, savepath):

        # Hard coded params
        rcParams['xtick.labelsize'] = 14
        rcParams['ytick.labelsize'] = 14

        if self.ci:
            idf_transposed = self.idf.transpose()
            dfmean = idf_transposed.drop([x for x in idf_transposed.columns if (
                x[:1] == 'L' or x[:1] == 'U')], axis=1)

            fig, axs = plt.subplots(figsize=(13, 10))
            a1 = dfmean.plot(ax=axs)
            fill_alpha = 0.3

        # Hard coded this durations and return periods, could change to user input

            plt.xticks(np.arange(0, 8), ('1H', '2H', '3H',
                                         '6H', '12H', '24H', '48H', '72H'))
            # Hard coded to display only up to ARI 10 because others overlap
            plt.fill_between(np.arange(0, 8), idf_transposed['L2-yr'].values,
                             idf_transposed['U2-yr'].values, alpha=fill_alpha)
            plt.fill_between(np.arange(0, 8), idf_transposed['L5-yr'].values,
                             idf_transposed['U5-yr'].values, alpha=fill_alpha)
            plt.fill_between(np.arange(0, 8), idf_transposed['L10-yr'].values,
                             idf_transposed['U10-yr'].values, alpha=fill_alpha)
            legend = plt.legend(bbox_to_anchor=(1, 0.75),
                                title='Duration', fontsize=13)
            plt.setp(legend.get_title(), fontsize=15)
            plt.ylabel('Precipitation Depth (in)', {'fontsize': 18})
            plt.xlabel('Duration', {'fontsize': 18})
            plt.grid()

        else:
            self.idf.plot(figsize=(9, 7))
            legend = plt.legend(bbox_to_anchor=(1, 0.75),
                                title='Duration', fontsize=11)
            plt.setp(legend.get_title(), fontsize=15)
            plt.ylabel('Precipitation Depth (in)', {'fontsize': 18})
            plt.xlabel('Average Recurrence Interval', {'fontsize': 18})
            plt.grid()

        plt.savefig("{}/Figure_{}.{}".format(savepath,
                                             path.split('/')[-1][:-4], figformat), bbox_inches='tight')
