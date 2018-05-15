import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import numpy.polynomial.polynomial as poly
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit

plt.style.use('dark_background')
plt.rcParams['errorbar.capsize'] = 3
plt.rcParams['figure.figsize'] = (5,5)
plt.rcParams["savefig.dpi"] = 240

create_orig_fig = False
create_savgol_fig = False
create_savgol_poly = False



# get dict and list of fluorescent colours
#https://www.w3schools.com/colors/colors_crayola.asp
fc_dict =    {"Red":"#FF355E",
                "Watermelon":"#FD5B78",
                "Orange":"#FF6037",
                "Tangerine":"#FF9966",
                "Carrot":"#FF9933",
                "Sunglow":"#FFCC33",
                "Lemon":"#FFFF66",
                "Yellow":"#FFFF66",
                "Lime":"#CCFF00",
                "Green":"#66FF66",
                "Mint":"#AAF0D1",
                "Blue":"#50BFE6",
                "Pink":"#FF6EFF",
                "Rose":"#EE34D2",
                "Magenta":"#FF00CC",
                "Pizzazz":"FF00CC"}
fl_col_keys = sorted(fc_dict)
fl_col_list = [fc_dict[k] for k in fl_col_keys]

class FlourescentColours:
    def __init__(self):
        self.red = "#FF355E"
        self.watermelon = "#FD5B78"
        self.orange = "#FF6037"
        self.tangerine = "#FF9966"
        self.carrot = "#FF9933"
        self.sunglow = "#FFCC33"
        self.lemon = "#FFFF66"
        self.yellow = "#FFFF66"
        self.lime = "#CCFF00"
        self.green = "#66FF66"
        self.mint = "#AAF0D1"
        self.blue = "#50BFE6"
        self.pink = "#FF6EFF"
        self.rose = "#EE34D2"
        self.magenta = "#FF00CC"
        self.pizzazz = "FF00CC"

fc = FlourescentColours()


def exp_func(x, a, b, c):
    y = a * np.exp(-b * x) + c
    return y

schweris_dir = r"D:\drive\schweris"
data_dir = os.path.join(schweris_dir, "Projects\\smFRET_fit\\20171017_data")
csv_files = glob.glob(r"D:\drive\schweris\Projects\smFRET_fit\20171017_data\*.txt")
_max_figs = 20
for csv in csv_files[0:_max_figs]:
    df = pd.read_csv(csv)
    # print(df.head())
    out_dir = r"D:\drive\schweris\Projects\smFRET_fit\20171017_data\analysis\fits"
    orig_fit_png = os.path.join(out_dir, "orig", os.path.basename(csv)[:-4] + "_orig_fit.png")
    savgol_fit_png = os.path.join(out_dir, "sg_full", "all", os.path.basename(csv)[:-4] + "_savgol_fit.png")
    savgol_fit_peak_png = os.path.join(out_dir, "sg_full", "peak", os.path.basename(csv)[:-4] + "_savgol_fit_peak.png")
    savgol_fit_desc_png = os.path.join(out_dir, "desc", "savgol", os.path.basename(csv)[:-4] + "_savgol_fit_desc.png")
    exp_fit_desc_png = os.path.join(out_dir, "desc", "exp", os.path.basename(csv)[:-4] + "_savgol_fit_desc.png")

    if create_orig_fig:
        plt.close("all")
        fig, ax = plt.subplots()
        df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data")
        df.plot(x="time_ns", y="fit", ax=ax, color=fc.red, label="original fit")
        fig.savefig(orig_fit_png)




    _min = 0
    x = df.time_ns[_min:].as_matrix()
    y = df.anisotropy[_min:].as_matrix()
    y_fit = savgol_filter(y, 51, 3)
    if create_savgol_fig:
        plt.close("all")
        fig, ax = plt.subplots()
        df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data")
        df["savgol"] = y_fit
        ax.plot(x, y_fit, color="r")
        ax.set_title("savitzky_golay using scipy signal")
        ax.legend()
        fig.savefig(savgol_fit_png, dpi=240)
        ax.set_xlim(0.4, 2)
        ax.set_ylim(0.3, 0.6)
        fig.savefig(savgol_fit_peak_png)


    if create_savgol_poly:
        # get max, index max, and time associated with max anisotropy
        savgol_max = y_fit.max()
        savgol_max_index = y_fit.argmax()
        savgol_max_time = x[savgol_max_index]

        # get region after peak for polyfit, to calculate rinf
        datapoints_after_peak = 40
        start = savgol_max_index + datapoints_after_peak

        # dataframe for descending data
        df_desc = df.loc[start:, :].copy()
        x = df_desc.time_ns.as_matrix()
        y = df_desc.anisotropy.as_matrix()
        # fit savitzky golay again, this time with a wider window
        y_fit_desc_sg = savgol_filter(y, 201, 3)
        df.loc[start:, "savgol_descending"] = y_fit_desc_sg
        plt.close("all")
        fig, ax = plt.subplots()
        df_desc.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data")
        ax.plot(x, y_fit_desc_sg, color="r", label="savitzky-golay")

        start_poly = 300

        coeffs = poly.polyfit(x[start_poly:], y_fit_desc_sg[start_poly:], 2)
        x_fit = np.linspace(x[start_poly], 32, 200)
        # y_fit_sg_p = poly.polyval((x[500:], coeffs)
        y_fit_sg_p = poly.polyval(x_fit, coeffs)
        # ax.plot(x[500:], y_fit_sg_p, color="0.5", label="sg_p")
        ax.plot(x_fit, y_fit_sg_p, color="0.5", label="polynomial of savitzky-golay")
        ax.set_title("fit savitzky-golay with wider window to datapoints after peak")
        ax.legend()
        fig.savefig(savgol_fit_desc_png, dpi=240)



    plt.close("all")
    fig, ax = plt.subplots()
    df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax, color=fc.green, label="data", s=1)

    start_exp2 = 300
    df_exp2 = df.loc[start_exp2:, :].copy()
    x = df_exp2.time_ns.as_matrix()
    y = df_exp2.anisotropy.as_matrix()
    guess = np.array([0.35, 0.3, 0.18])
    #popt, pcov = curve_fit(exp_func, x, y_fit_desc_sg, p0=guess)
    popt, pcov = curve_fit(exp_func, x, y, p0=guess)
    print(popt)
    xfit = np.linspace(0, 60, 500)
    yfit = exp_func(xfit, *popt)
    ax.plot(xfit, yfit, color=fc.magenta, label="exponential fit descending")

    yfitted_region = exp_func(x, *popt)
    ax.plot(x, yfitted_region, color="w", linestyle = ":", label="fitted region")

    ax.set_xlim(0, 60)
    ax.legend()
    fig.savefig(exp_fit_desc_png)



