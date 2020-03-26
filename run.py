from constructIDF import *
import pandas as pd
import numpy as np
import itertools
import argparse


def main(args):

    ftype = args.ftype
    fpath = args.path

    # Hard coded durations here, but could be input from the user
    durations = [1, 2, 3, 6, 12, 24, 48, 72]

    ts = AMS(args.path, durations)

    out = ts.calculate_AMS(args.ftype)

    if args.saveAMS == True:
        out.to_csv("{}/AMS_{}".format(args.savepath, fpath.split('/')[-1]))

    data = IDF(out, args.ci, args.number_bootstrap, args.alpha)
    data.construct_IDF()

    data.idf.to_csv("{}/IDF_{}".format(args.savepath,
                                       args.path.split('/')[-1]))

    data.plot_IDF(args.path, args.format, args.savepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Extract the annual maximum precipitation (AMS) from a precipitation time series")

    parser.add_argument("--path", required=True, type=str,
                        help="Full path where the .csv file of hourly rainfall records is located.")
    parser.add_argument("--saveAMS", default=True, type=bool,
                        help="Option to save the AMS")
    parser.add_argument("--ftype", required=True, type=str,
                        help="Type of approach. There are only two options: 'sliding' or 'fixed'")
    parser.add_argument("--ci", default=False, type=bool,
                        help="Should CI be computed?")
    parser.add_argument("--number_bootstrap", default=100, type=int,
                        help="Number of bootsrap samples to generate, default 100")
    parser.add_argument("--alpha", default=0.9,
                        help="confidence level, e.g. 0.9 or 0.99, default 0.9")
    parser.add_argument("--savepath", required=True, type=str,
                        help="Full path where to save all outputs")
    parser.add_argument("--format", required=True, type=str,
                        help="figure file format, either png or pdf")

    args = parser.parse_args()

    main(args)
