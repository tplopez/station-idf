"""
File name: constructIDF
Author: Tania Lopez-Cantu
E-mail: tlopez@andrew.cmu.edu

##############################

Purpose:

Generates a IDF curves with confidence intervals
using scipy genextreme library and custom bootstraping
function using numpy.random.choice

"""


from scipy.stats import genextreme as gev
import pandas as pd
import argparse

rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14


def main(args):

    ams = pd.read_csv(args.path, index_col=0)
    ams.drop(['year'], axis=1, inplace=True)

    # Hard coded durations here but can be specified by the user.

    x = [1 / 2, 1 / 5, 1 / 10, 1 / 25, 1 / 50, 1 / 100, 1 / 200]
    noci = ['2-yr', '5-yr', '10-yr', '25-yr', '50-yr', '100-yr', '200-yr']

    wci = []

    for bound in ['L', '', 'U']:
        for e in noci:
            wci.append("{}{}".format(bound, e))
    if args.ci == True:
        idf = pd.DataFrame(index=wci)
        bts = {}
        for col in ams.columns:
            mams = []
            for i in range(args.nbootstrap):
                bootsams = np.random.choice(
                    ams[col].values, replace=True, size=len(ams))
                fit = gev.fit(bootsams)
                mams.append(gev.isf(x, c=fit[0], loc=fit[1], scale=fit[2]))
            bts[col] = np.asarray(mams)
        alpha = args.alpha
        p_lo = ((1.0-alpha)/2.0) * 100
        p_up = (alpha+((1.0-alpha)/2.0)) * 100
        for col in ams.columns:
            lower = np.apply_along_axis(np.percentile, 0, bts[col], p_lo)
            upper = np.apply_along_axis(np.percentile, 0, bts[col], p_up)
            mean = np.apply_along_axis(np.mean, 0, bts[col])

            idf[col] = np.append(lower, np.append(mean, upper))

    elif:
        idf = pd.DataFrame(index=noci)
        args.ci == False:
        for col in ams.columns:
            fit = gev.fit(ams[col])
            idf[col] = gev.isf(x, c=fit[0], loc=fit[1], scale=fit[2])

    else:
        print('True, False are the only valid options for --ci')
        idf = pd.DataFrame()

    idf.to_csv("{}/IDF_{}".format(args.savepath,
                                  args.path.split('/')[-1]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Extract the annual maximum precipitation (AMS) from a precipitation time series")

    parser.add_argument("--path", required=True, type=str,
                        help="Full path where the ams csv file is located. The first column of the data should be the year, and the rest columns should be each durations ' AMS")
    parser.add_argument("--format", required=True, type=str,
                        help="figure file format, either png or pdf")
    parser.add_argument("--ci", default=False, type=bool,
                        help="Should CI be computed?")
    parser.add_argument("--nbootsrap", default=100, type=int,
                        help="Number of bootsrap samples to generate, default 100")
    parser.add_argument("--alpha", default=False,
                        help="confidence level, e.g. 0.1 or     0.01")
    parser.add_argument("--savepath", required=True, type=str,
                        help="Full path where to save the extracted AMS as a .csv file")

    args = parser.parse_args()

    main(args)
