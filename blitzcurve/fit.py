import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import numpy.polynomial.polynomial as poly
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
from matplotlib.patches import Rectangle
import blitzcurve.utils as utils


#
# #fits_dir = r"D:\drive\schweris\Projects\smFRET_fit\20171017_data\analysis\fits"
# schweris_dir = r"D:\drive\schweris"
# data_dir = os.path.join(schweris_dir, "Projects\\smFRET_fit\\20171017_data")
# max_figs = 20

class OutFilepaths:
    def __init__(self, data_dir, csv):
        self.fits_dir = os.path.join(data_dir, "fits")
        self.rotat_dir = os.path.join(self.fits_dir, "rotat")
        self.savgol_dir = os.path.join(self.fits_dir, "savgol")
        self.seg1_dir = os.path.join(self.fits_dir, "seg1")
        self.seg2_dir = os.path.join(self.fits_dir, "seg2")
        for path in [self.fits_dir, self.rotat_dir, self.savgol_dir, self.seg1_dir, self.seg2_dir]:
            if not os.path.isdir(path):
                os.makedirs(path)
        self.filename = os.path.basename(csv)
        self.rotat_fit_png = os.path.join(self.rotat_dir, self.filename[:-4] + "_rotat_fit.png")
        self.savgol_fit_png = os.path.join(self.savgol_dir, self.filename[:-4] + "_savgol_fit.png")
        self.savgol_fit_peak_png = os.path.join(self.savgol_dir, self.filename[:-4] + "_savgol_fit_peak.png")
        self.savgol_fit_desc_png = os.path.join(self.seg1_dir, self.filename[:-4] + "_savgol_fit_desc.png")
        self.exp_fit_seg1_png = os.path.join(self.seg1_dir, self.filename[:-4] + "_seg1.png")
        self.exp_fit_seg2_png = os.path.join(self.seg2_dir, self.filename[:-4] + "_seg2.png")

def run_fit(data_dir, figs_to_plot="all"):

    plt.style.use('dark_background')
    plt.rcParams['errorbar.capsize'] = 3
    plt.rcParams['figure.figsize'] = (5, 5)
    plt.rcParams["savefig.dpi"] = 240

    fc = utils.FlourescentColours()
    csv_files = glob.glob(os.path.join(data_dir, "*.txt"))

    nested_out_dict = {}
    for csv in csv_files:
        print(csv)
        df = pd.read_csv(csv)
        # paths for the output files
        p = OutFilepaths(data_dir, csv)
        fit_dict = fit_single_sample(df, fc, p, figs_to_plot=figs_to_plot)
        nested_out_dict[p.filename] = fit_dict

    summ_dir = os.path.join(data_dir, "summary")
    summ_csv = os.path.join(summ_dir, "fit_summary.csv")
    if not os.path.isdir(summ_dir):
        os.makedirs(summ_dir)
    df_summ = pd.DataFrame(nested_out_dict)
    df_summ.to_csv(summ_csv)


def fit_single_sample(df, fc, p, figs_to_plot):

    fit_dict = {}

    if "all" or "rotat" in figs_to_plot:
        plt.close("all")
        fig, ax = plt.subplots()
        df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data")
        df.plot(x="time_ns", y="fit", ax=ax, color=fc.red, label="rotational correlation fit")
        fig.savefig(p.rotat_fit_png)
        print(p.rotat_fit_png)

    _min = 0
    x = df.time_ns[_min:].as_matrix()
    y = df.anisotropy[_min:].as_matrix()
    y_fit = savgol_filter(y, 51, 3)

    if "all" or "savgol" in figs_to_plot:
        plt.close("all")
        fig, ax = plt.subplots()
        df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data", s=1)
        df["savgol"] = y_fit
        ax.plot(x, y_fit, color="r")
        ax.set_title("savitzky-golay fit")
        ax.legend()
        fig.savefig(p.savgol_fit_png, dpi=240)
        ax.set_xlim(0.4, 2)
        ax.set_ylim(0.3, 0.6)
        ax.set_title("savitzky-golay fit for peak only")
        fig.savefig(p.savgol_fit_peak_png)

    # get max, index max, and time associated with max anisotropy
    fit_dict["ypeak"] = y_fit.max()
    fit_dict["ypeak_index"] = y_fit.argmax()
    fit_dict["ypeak_time"] = x[fit_dict["ypeak_index"]]

    # get region after peak for polyfit, to calculate rinf
    datapoints_after_peak = 40
    start_seg1 = fit_dict["ypeak_index"] + datapoints_after_peak
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

        a1, b1, c1 = popt
        fit_dict["a1"], fit_dict["b1"] ,fit_dict["c1"] = a1, b1, c1

        # annotate the function on the graph
        function_string = r"y = %0.2f * $e^{(-%0.2fx)}$ + %0.2f" % (a1, b1, c1)
        ax.annotate(function_string, (np.median(x) + 0.2, np.median(y) + 0.05), color=fc.magenta)

        xfit = np.linspace(0, xmax_seg1, 500)
        yfit = utils.exp_func(xfit, *popt)
        ax.plot(xfit, yfit, color=fc.magenta, label="exponential fit")

        ymin, ymax = ax.get_ylim()
        height = ymax - ymin
        width = x[-1] - x[0]
        rect = Rectangle((x[0], ymin), width, height, color="0.2", zorder=1)
        ax.add_patch(rect)

        ax.set_title("fit to segment 1")
        ax.legend()
        fig.savefig(p.exp_fit_seg1_png)

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

        a2, b2, c2 = popt
        fit_dict["a2"], fit_dict["b2"] ,fit_dict["c2"] = a2, b2, c2

        # annotate the function on the graph
        function_string = r"y = %0.2f * $e^{(-%0.2fx)}$ + %0.2f" % (a2, b2, c2)
        ax.annotate(function_string, (x[0] + 0.2, y[0] + 0.05), color=fc.pink)

        xfit = np.linspace(0, xmax_fit, 500)
        yfit = utils.exp_func(xfit, *popt)
        ax.plot(xfit, yfit, color=fc.pink, label="exponential fit segment 2")

        ax.hlines(popt[-1], 0, xmax_fit, color=fc.pink)

        ymin, ymax = ax.get_ylim()
        height = ymax - ymin
        width = x[-1] - x[0]
        rect = Rectangle((x[0], ymin), width, height, color="0.2", zorder=1)
        ax.add_patch(rect)

        ax.set_title("fit to segment 2")
        ax.legend()
        fig.savefig(p.exp_fit_seg2_png)
    return fit_dict
        

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