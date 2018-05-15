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

plt.style.use('dark_background')
plt.rcParams['errorbar.capsize'] = 3
plt.rcParams['figure.figsize'] = (5,5)
plt.rcParams["savefig.dpi"] = 240

create_orig_fig = False
create_savgol_fig = False
create_savgol_poly = False
create_desc1_rinf_fig = True
create_desc2_rinf_fig = True

#
# #fits_dir = r"D:\drive\schweris\Projects\smFRET_fit\20171017_data\analysis\fits"
# schweris_dir = r"D:\drive\schweris"
# data_dir = os.path.join(schweris_dir, "Projects\\smFRET_fit\\20171017_data")
# max_figs = 20

def run_fit(data_dir, max_figs):
    fc = utils.FlourescentColours()
    csv_files = glob.glob(os.path.join(data_dir, "*.txt"))
    for csv in csv_files[0:max_figs]:
        print(csv)
        df = pd.read_csv(csv)
        # print(df.head())
        fits_dir = os.path.join(data_dir, "fits")
        rotat_dir = os.path.join(fits_dir, "rotat")
        savgol_dir = os.path.join(fits_dir, "savgol")
        seg1_dir = os.path.join(fits_dir, "seg1")
        seg2_dir = os.path.join(fits_dir, "seg2")
        for path in [fits_dir, rotat_dir, savgol_dir, seg1_dir, seg2_dir]:
            if not os.path.isdir(path):
                os.makedirs(path)

        rotat_fit_png = os.path.join(rotat_dir, os.path.basename(csv)[:-4] + "_rotat_fit.png")
        savgol_fit_png = os.path.join(savgol_dir, os.path.basename(csv)[:-4] + "_savgol_fit.png")
        savgol_fit_peak_png = os.path.join(savgol_dir, os.path.basename(csv)[:-4] + "_savgol_fit_peak.png")
        savgol_fit_desc_png = os.path.join(seg1_dir, os.path.basename(csv)[:-4] + "_savgol_fit_desc.png")
        exp_fit_seg1_png = os.path.join(seg1_dir, os.path.basename(csv)[:-4] + "_seg1.png")
        exp_fit_seg2_png = os.path.join(seg2_dir, os.path.basename(csv)[:-4] + "_seg2.png")

        if create_orig_fig:
            plt.close("all")
            fig, ax = plt.subplots()
            df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data")
            df.plot(x="time_ns", y="fit", ax=ax, color=fc.red, label="rotational correlation fit")
            fig.savefig(rotat_fit_png)

        _min = 0
        x = df.time_ns[_min:].as_matrix()
        y = df.anisotropy[_min:].as_matrix()
        y_fit = savgol_filter(y, 51, 3)


        if create_savgol_fig:
            plt.close("all")
            fig, ax = plt.subplots()
            df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data", s=1)
            df["savgol"] = y_fit
            ax.plot(x, y_fit, color="r")
            ax.set_title("savitzky-golay fit")
            ax.legend()
            fig.savefig(savgol_fit_png, dpi=240)
            ax.set_xlim(0.4, 2)
            ax.set_ylim(0.3, 0.6)
            ax.set_title("savitzky-golay fit for peak only")
            fig.savefig(savgol_fit_peak_png)

        # get max, index max, and time associated with max anisotropy
        ypeak = y_fit.max()
        ypeak_index = y_fit.argmax()
        ypeak_time = x[ypeak_index]
        # get region after peak for polyfit, to calculate rinf
        datapoints_after_peak = 40
        start_seg1 = ypeak_index + datapoints_after_peak
        end_seg1 = 300
        start_seg2 = end_seg1
        end_seg2 = df.time_ns.max()

        xmax_seg1 = df.time_ns[end_seg1]


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

        if create_desc1_rinf_fig:
            plt.close("all")
            fig, ax = plt.subplots()

            df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data", s=1, zorder=2)

            df_exp1 = df.loc[start_seg1:end_seg1, :].copy()
            x = df_exp1.time_ns.as_matrix()
            y = df_exp1.anisotropy.as_matrix()

            xmax_fit = x.max() + 3

            guess = (0.35, 0.3, 0.18)

            popt, pcov = curve_fit(utils.exp_func, x, y, p0=guess)

            # annotate the function on the graph
            function_string = r"y = %0.2f * $e^{(-%0.2fx)}$ + %0.2f" % (popt[0], popt[1], popt[2])
            ax.annotate(function_string, (np.median(x) + 0.2, np.median(y) + 0.05), color=fc.magenta)

            xfit = np.linspace(0, xmax_seg1, 500)
            yfit = utils.exp_func(xfit, *popt)
            ax.plot(xfit, yfit, color=fc.magenta, label="exponential fit")

            ymin, ymax = ax.get_ylim()
            xmin, xmax = ax.get_xlim()
            height = ymax - ymin
            width = x[-1] - x[0]
            rect = Rectangle((x[0], ymin), width, height, color="0.2", zorder=1)
            ax.add_patch(rect)

            ax.set_title("fit to segment 1")
            ax.legend()
            fig.savefig(exp_fit_seg1_png)



        if create_desc2_rinf_fig:
            plt.close("all")
            fig, ax = plt.subplots()

            df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data", s=1, zorder=2)

            df_exp2 = df.loc[end_seg1:, :].copy()
            x = df_exp2.time_ns.as_matrix()
            y = df_exp2.anisotropy.as_matrix()

            xmax_fit = x.max() + 3

            guess = (0.35, 0.3, 0.18)
            popt, pcov = curve_fit(utils.exp_func, x, y, p0=guess)

            # annotate the function on the graph
            function_string = r"y = %0.2f * $e^{(-%0.2fx)}$ + %0.2f" % (popt[0], popt[1], popt[2])
            ax.annotate(function_string, (x[0] + 0.2, y[0] + 0.05), color=fc.pink)

            xfit = np.linspace(0, xmax_fit, 500)
            yfit = utils.exp_func(xfit, *popt)
            ax.plot(xfit, yfit, color=fc.pink, label="exponential fit segment 2")

            ax.hlines(popt[-1], 0, xmax_fit, color=fc.pink)

            ymin, ymax = ax.get_ylim()
            xmin, xmax = ax.get_xlim()
            height = ymax - ymin
            width = x[-1] - x[0]
            rect = Rectangle((x[0],ymin),width, height, color="0.2", zorder=1)
            ax.add_patch(rect)

            ax.set_title("fit to segment 2")
            ax.legend()
            fig.savefig(exp_fit_seg2_png)



