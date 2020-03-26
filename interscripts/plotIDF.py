"""
File name: constructIDF
Author: Tania Lopez-Cantu
E-mail: tlopez@andrew.cmu.edu

##############################

Purpose:

Creates and save a IDF/DDF curves plot.

"""
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import argparse
import numpy as np

rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14


def makeIDFplot(path, idf, savepath, figformat, CI=False):
    """
    Make a plot of IDF curves for different durations
    and return periods and saves the figure to the same location
    where the data to be plotted is stored.

    Parameters
    ----------
    idf: dataframe, columns must be each return period rainfall depth, to
    be plotted and rows must be the duration. For example, columns could be "2-yr", "5-yr", "10-yr",
    and rows must be "1H", "2H", "3H". If plotting CI, then columns should be:
    "L_2-yr", "2-yr", "U_2-yr", for each return period to plot, in that specific order, rows stay the same.

    """
    if CI == False:
        idf.plot(figsize=(9, 7))
        legend = plt.legend(bbox_to_anchor=(1, 0.75),
                            title='Duration', fontsize=11)
        plt.setp(legend.get_title(), fontsize=15)
        plt.ylabel('Precipitation Depth (in)', {'fontsize': 18})
        plt.xlabel('Average Recurrence Interval', {'fontsize': 18})
        plt.grid()

        plt.savefig("{}/F_{}.{}".format(savepath,
                                        path.split('/')[-1][:-4], figformat), bbox_inches='tight')

    elif CI == True:
        dfmean = idf.drop([x for x in idf.columns if (
            x[:1] == 'L' or x[:1] == 'U')], axis=1)

        fig, axs = plt.subplots(figsize=(13, 10))
        a1 = dfmean.plot(ax=axs)
        fill_alpha = 0.3

        # Hard coded this durations and return periods, could change to user input

        plt.xticks(np.arange(0, 8), ('1H', '2H', '3H',
                                     '6H', '12H', '24H', '48H', '72H'))

        plt.fill_between(np.arange(0, 8), idf['L2-yr'].values,
                         idf['U2-yr'].values, alpha=fill_alpha)
        plt.fill_between(np.arange(0, 8), idf['L5-yr'].values,
                         idf['U5-yr'].values, alpha=fill_alpha)
        plt.fill_between(np.arange(0, 8), idf['L10-yr'].values,
                         idf['U10-yr'].values, alpha=fill_alpha)
        # plt.fill_between(np.arange(0, 8), idf['L25-yr'].values,
        #                  idf['U25-yr'].values, alpha=fill_alpha)
        # plt.fill_between(np.arange(0, 8), idf['L50-yr'].values,
        #                  idf['U50-yr'].values, alpha=fill_alpha)
        # plt.fill_between(np.arange(0, 8), idf['L100-yr'].values,
        #                  idf['U100-yr'].values, alpha=fill_alpha)

        # plt.fill_between(np.arange(0, 8), idf['L{}'.format(col)].values,
        #                  idf['U{}'.format(col)].values, alpha=fill_alpha)

        legend = plt.legend(bbox_to_anchor=(1, 0.75),
                            title='Duration', fontsize=13)
        plt.setp(legend.get_title(), fontsize=15)
        plt.ylabel('Precipitation Depth (in)', {'fontsize': 18})
        plt.xlabel('Duration', {'fontsize': 18})
        plt.grid()
        plt.savefig("{}/F_{}.{}".format(savepath,
                                        path.split('/')[-1][:-4], figformat), bbox_inches='tight')


def main(args):
    """
    Make a plot of IDF curves for different durations
    and return periods

    Parameters
    ----------
    input:

    """

    idf = pd.read_csv(args.path, index_col=0)
    dfmean = idf.drop([x for x in idf.columns if (
        x[:1] == 'L' or x[:1] == 'U')], axis=1)
    makeIDFplot(args.path, idf.transpose(), args.savepath,
                args.format, args.includeCI)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Extract the annual maximum precipitation (AMS) from a precipitation time series")

    parser.add_argument("--path", required=True, type=str,
                        help="Full path where the ams csv file is located. The first column of the data should be the year, and the rest columns should be each durations ' AMS")
    parser.add_argument("--format", required=True, type=str,
                        help="figure file format, either png or pdf")
    parser.add_argument("--savepath", required=True, type=str,
                        help="Full path where to save the extracted AMS as a .csv file")
    parser.add_argument("--includeCI", default=False, type=bool,
                        help='Should plot include confidence intervals? This option only available if input data contains CI curves for each duration and return period')
    args = parser.parse_args()

    main(args)
