from matplotlib import pyplot as plt
import glob
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from blitzcurve.utils import setup_matplotlib_dark_background
import blitzcurve.utils as utils


def run_compare(data_dir, file_list="all", name_list= None, testing_mode=False):
    setup_matplotlib_dark_background(plt)

    fc = utils.FlourescentColours()
    csv_files = glob.glob(os.path.join(data_dir, "*.txt"))

    # drop any files not in the list
    if file_list != "all":
        for csv in csv_files:
            if os.path.basename(csv) not in file_list:
                csv_files.remove(csv)

    if testing_mode:
        csv_files = csv_files[0:2]

    summ_csv = os.path.join(data_dir, "summary", "fit_summary.csv")
    df_summ = pd.read_csv(summ_csv)

    for csv in csv_files:
        # paths for the output files
        p = utils.OutFilepaths(data_dir, csv)
        with open(p.fitdata_pickle, "rb") as pic:
            fd = pickle.load(pic)

