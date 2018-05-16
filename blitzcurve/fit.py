import glob
import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter

import blitzcurve.utils as utils
#
# #fits_dir = r"D:\drive\schweris\Projects\smFRET_fit\20171017_data\analysis\fits"
# schweris_dir = r"D:\drive\schweris"
# data_dir = os.path.join(schweris_dir, "Projects\\smFRET_fit\\20171017_data")
# max_figs = 20
from blitzcurve.utils import setup_matplotlib_dark_background, OutFilepaths


def run_fit(data_dir, figs_to_plot="all", testing_mode=False):

    setup_matplotlib_dark_background(plt)

    fc = utils.FlourescentColours()
    csv_files = glob.glob(os.path.join(data_dir, "*.txt"))

    if testing_mode:
        csv_files = csv_files[0:2]

    nested_summ_dict = {}
    for csv in csv_files:
        print(csv)
        df = pd.read_csv(csv)
        # paths for the output files
        p = OutFilepaths(data_dir, csv)
        summ_dict, fd = fit_single_sample(df, fc, p, figs_to_plot)
        nested_summ_dict[p.filename] = summ_dict

        with open(p.fitdata_pickle, "wb") as pic:
            pickle.dump(fd, pic, protocol=pickle.HIGHEST_PROTOCOL)

    summ_dir = os.path.join(data_dir, "summary")
    summ_csv = os.path.join(summ_dir, "fit_summary.csv")
    if not os.path.isdir(summ_dir):
        os.makedirs(summ_dir)
    df_summ = pd.DataFrame(nested_summ_dict).T
    df_summ.to_csv(summ_csv)


class OutputFitData:
    def __init__(self, fit_savgol=None, seg1_xfit=None, seg1_yfit=None, seg2_xfit=None, seg2_yfit=None):
        self.fit_savgol = fit_savgol
        self.seg1_xfit = seg1_xfit
        self.seg1_yfit = seg1_yfit
        self.seg2_xfit = seg2_xfit
        self.seg2_yfit = seg2_yfit

def fit_single_sample(df, fc, p, figs_to_plot):
    summ_dict = {}
    # initialise fit-data-object (holds arrays with fitted curves, etc)
    fd = OutputFitData()

    if "all" or "rotat" in figs_to_plot:
        plt.close("all")
        fig, ax = plt.subplots()
        df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data")
        df.plot(x="time_ns", y="fit", ax=ax, color=fc.red, label="rotational correlation fit")
        fig.savefig(p.rotat_fit_png)

    _min = 0
    x = df.time_ns[_min:].as_matrix()
    y = df.anisotropy[_min:].as_matrix()
    y_fit_savgol = savgol_filter(y, 51, 3)
    #curve_dict["fit_savgol"] = y_fit_savgol
    fd.y_fit_savgol = y_fit_savgol

    # get max, index max, and time associated with max anisotropy
    summ_dict["r_max"] = y_fit_savgol.max()
    summ_dict["r_max_index"] = y_fit_savgol.argmax()
    summ_dict["r_max_time"] = x[summ_dict["r_max_index"]]

    if "all" or "savgol" in figs_to_plot:
        plt.close("all")
        fig, ax = plt.subplots()
        df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data", s=1)
        ax.plot(x, y_fit_savgol, color=fc.red, label="savitzky-golay fit")
        # annotate the anosotropy associated with the peak on the graph
        peak_string = "max anisotropy : {:.02f}\n   time : {:.02f} ns".format(summ_dict["r_max"], summ_dict["r_max_time"])
        ax.annotate(peak_string, (summ_dict["r_max_time"] + 0.2, summ_dict["r_max"] - 0.02), color=fc.red)
        ax.set_title("savitzky-golay fit")
        ax.legend()
        fig.savefig(p.savgol_fit_png, dpi=240)

        plt.close("all")
        fig, ax = plt.subplots()
        df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data", s=1)
        ax.plot(x, y_fit_savgol, color=fc.red, label="savitzky-golay fit")
        # annotate the anosotropy associated with the peak on the graph
        peak_string = "max anisotropy : {:.02f}\ntime : {:.02f} ns".format(summ_dict["r_max"], summ_dict["r_max_time"])
        ax.annotate(peak_string, (summ_dict["r_max_time"] + 0.1, summ_dict["r_max"] + 0.005), color=fc.red)
        ax.set_title("savitzky-golay fit")
        ax.legend()
        ax.set_xlim(0.4, 2)
        ax.set_ylim(0.3, 0.6)
        ax.set_title("savitzky-golay fit for peak only")
        fig.savefig(p.savgol_fit_peak_png)


    # get region after peak for polyfit, to calculate rinf
    datapoints_after_peak = 40
    start_seg1 = summ_dict["r_max_index"] + datapoints_after_peak
    end_seg1 = 300
    start_seg2 = end_seg1
    end_seg2 = df.time_ns.max()

    xmax_seg1 = df.time_ns[end_seg1]

    if "all" or "seg1" in figs_to_plot:
        plt.close("all")
        fig, ax = plt.subplots()

        df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data", s=1, zorder=2)

        df_exp1 = df.loc[start_seg1:end_seg1, :].copy()
        x = df_exp1.time_ns.as_matrix()
        y = df_exp1.anisotropy.as_matrix()

        guess = (0.35, 0.3, 0.18)
        popt, pcov = curve_fit(utils.exp_func, x, y, p0=guess)

        a_seg1, b_seg1, c_seg1 = popt
        summ_dict["a_seg1"], summ_dict["b_seg1"] ,summ_dict["c_seg1"] = a_seg1, b_seg1, c_seg1

        # annotate the function on the graph
        function_string = r"y = %0.2f * $e^{(-%0.2fx)}$ + %0.2f" % (a_seg1, b_seg1, c_seg1)
        ax.annotate(function_string, (np.median(x) + 0.2, np.median(y) + 0.05), color=fc.magenta)

        seg1_xfit = np.linspace(0, xmax_seg1, 500)
        seg1_yfit = utils.exp_func(seg1_xfit, *popt)
        ax.plot(seg1_xfit, seg1_yfit, color=fc.magenta, label="exponential fit")

        ymin, ymax = ax.get_ylim()
        height = ymax - ymin
        width = x[-1] - x[0]
        rect = Rectangle((x[0], ymin), width, height, color="0.2", zorder=1)
        ax.add_patch(rect)

        ax.set_title("fit to segment 1")
        ax.legend()
        fig.savefig(p.exp_fit_seg1_png)

        # add data to output curve dictionary
        #curve_dict["seg1_xfit"] = seg1_xfit
        #curve_dict["seg1_yfit"] = seg1_yfit
        fd.seg1_xfit = seg1_xfit
        fd.seg1_yfit = seg1_yfit


    if "all" or "seg2" in figs_to_plot:
        plt.close("all")
        fig, ax = plt.subplots()

        df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data", s=1, zorder=2)

        df_exp2 = df.loc[start_seg2:, :].copy()
        x = df_exp2.time_ns.as_matrix()
        y = df_exp2.anisotropy.as_matrix()

        xmax_fit = x.max() + 3

        guess = (0.35, 0.3, 0.18)
        popt, pcov = curve_fit(utils.exp_func, x, y, p0=guess)

        a_seg2, b_seg2, r_inf = popt
        summ_dict["a_seg2"], summ_dict["b_seg2"] ,summ_dict["r_inf"] = a_seg2, b_seg2, r_inf

        # annotate the function on the graph
        function_string = r"y = %0.2f * $e^{(-%0.2fx)}$ + %0.2f" % (a_seg2, b_seg2, r_inf)
        ax.annotate(function_string, (x[0] + 0.2, y[0] + 0.05), color=fc.pink)

        seg2_xfit = np.linspace(0, xmax_fit, 500)
        seg2_yfit = utils.exp_func(seg2_xfit, *popt)
        ax.plot(seg2_xfit, seg2_yfit, color=fc.pink, label="exponential fit segment 2")

        ax.hlines(popt[-1], 0, xmax_fit, color=fc.pink)

        ymin, ymax = ax.get_ylim()
        height = ymax - ymin
        width = x[-1] - x[0]
        rect = Rectangle((x[0], ymin), width, height, color="0.2", zorder=1)
        ax.add_patch(rect)

        ax.set_title("fit to segment 2")
        ax.legend()
        fig.savefig(p.exp_fit_seg2_png)

        # save fitted data to output
        fd.seg2_xfit = seg2_xfit
        fd.seg2_yfit = seg2_yfit

    return summ_dict, fd
        

# Attempt at polynomial fit to savitzky golay fitted data
# DEPRECATED
# if create_savgol_poly:
#     # dataframe for descending data
#     df_desc = df.loc[start_seg1:, :].copy()
#     x = df_desc.time_ns.as_matrix()
#     y = df_desc.anisotropy.as_matrix()
#     # fit savitzky golay again, this time with a wider window
#     y_fit_desc_sg = savgol_filter(y, 201, 3)
#     df.loc[start_seg1:, "savgol_descending"] = y_fit_desc_sg
#     plt.close("all")
#     fig, ax = plt.subplots()
#     df_desc.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data", s=1)
#     ax.plot(x, y_fit_desc_sg, color="r", label="savitzky-golay")
#
#     start_poly = 300
#
#     coeffs = poly.polyfit(x[start_poly:], y_fit_desc_sg[start_poly:], 2)
#     x_fit = np.linspace(x[start_poly], 32, 200)
#     # y_fit_sg_p = poly.polyval((x[500:], coeffs)
#     y_fit_sg_p = poly.polyval(x_fit, coeffs)
#     # ax.plot(x[500:], y_fit_sg_p, color="0.5", label="sg_p")
#     ax.plot(x_fit, y_fit_sg_p, color="0.5", label="polynomial of savitzky-golay")
#     ax.set_title("fit savitzky-golay with wider window to datapoints after peak")
#     ax.legend()
#     fig.savefig(savgol_fit_desc_png, dpi=240)