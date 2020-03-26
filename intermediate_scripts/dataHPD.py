"""
File name: dataHPD
Author: Tania Lopez-Cantu
E-mail: tlopez@andrew.cmu.edu

##############################

Purpose:

Obtain data from the Hourly Precipitation Data (HDP) Network
and reformat.

"""

import pandas as pd
import argparse
import numpy as np
import numpy as np
import pandas as pd
import sys
import io
import os
import fnmatch


# Connecting to the server

class dataHPD:
     """
    This class contains methods to retrieve hourly time series from
    the NOAA Hourly Precipitation Data Network and reformat into a
    more friendly format.
    """

    def __init__(self, lat, lon):

        self.lat = lat
        self.lon = lon

    def getData(self):
        server = "ftp.ncdc.noaa.gov"
        ftp = ftplib.FTP(server)
        ftp.login()

        ftp.cwd('/pub/data/coop-/')
