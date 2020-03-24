"""
File name: constructIDF
Author: Tania Lopez-Cantu
E-mail: tlopez@andrew.cmu.edu

##############################

Purpose:

Generates a IDF curves and saves the figure as a png or pdf file.

"""


from scipy.stats import genextreme as gev
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
import argparse

rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14


def main(args):

    ams = pd.read_csv(args.path, index_col=0)
    ams.drop(['year'], axis=1, inplace=True)

    # Hard coded durations here but can be specified by the user.

    idf = pd.DataFrame(index=['2-yr', '5-yr', '10-yr',
                              '25-yr', '50-yr', '100-yr', '200-yr'])

    x = [1/2, 1/5, 1/10, 1/25, 1/50, 1/100, 1/200]

    for col in ams.columns:
        fit = gev.fit(ams[col])
        idf[col] = gev.isf(x, c=fit[0], loc=fit[1], scale=fit[2])

    idf.plot(figsize=(9, 7))
    legend = plt.legend(bbox_to_anchor=(1, 0.75),
                        title='Duration', fontsize=11)
    plt.setp(legend.get_title(), fontsize=15)
    plt.ylabel('Precipitation Depth (in)', {'fontsize': 18})
    plt.xlabel('Average Recurrence Interval', {'fontsize': 18})
    plt.grid()

    plt.savefig("{}/IDF_{}.{}".format(args.savepath,
                                      args.path.split('/')[-1][:-4], args.format), bbox_inches='tight')

    idf.to_csv("{}/IDF_{}".format(args.savepath,
                                  args.path.split('/')[-1]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Extract the annual maximum precipitation (AMS) from a precipitation time series")

    parser.add_argument("--path", required=True, type=str,
                        help="Full path where the ams csv file is located. The first column of the data should be the year, and the rest columns should be each durations ' AMS")
    parser.add_argument("--format", required=True, type=str,
                        help="figure file format, either png or pdf")
    parser.add_argument("--savepath", required=True, type=str,
                        help="Full path where to save the extracted AMS as a .csv file")

    args = parser.parse_args()

    main(args)
