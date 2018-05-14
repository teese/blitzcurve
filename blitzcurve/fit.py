import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import numpy.polynomial.polynomial as poly
from scipy.signal import savgol_filter

plt.style.use('seaborn-whitegrid')
plt.rcParams['errorbar.capsize'] = 3

schweris_dir = r"D:\drive\schweris"
data_dir = os.path.join(schweris_dir, "Projects\\smFRET_fit\\20171017_data")
csv_files = glob.glob(r"D:\drive\schweris\Projects\smFRET_fit\20171017_data\*.txt")
_max_figs = 20
for csv in csv_files[0:_max_figs]:
    df = pd.read_csv(csv)
    # print(df.head())
    out_dir = r"D:\drive\schweris\Projects\smFRET_fit\20171017_data\analysis\fits"
    savgol_fit_png = os.path.join(out_dir, "sg_full", "all", os.path.basename(csv)[:-4] + "_savgol_fit.png")
    savgol_fit_peak_png = os.path.join(out_dir, "sg_full", "peak", os.path.basename(csv)[:-4] + "_savgol_fit_peak.png")
    savgol_fit_desc_png = os.path.join(out_dir, "sg_desc", os.path.basename(csv)[:-4] + "_savgol_fit_desc.png")
    plt.close("all")
    fig, ax = plt.subplots()
    df.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax)
    _min = 0
    x = df.time_ns[_min:].as_matrix()
    y = df.anisotropy[_min:].as_matrix()
    y_fit = savgol_filter(y, 51, 3)
    df["savgol"] = y_fit
    ax.plot(x, y_fit, color="r")
    ax.set_title("savitzky_golay using scipy signal")
    ax.legend()
    fig.savefig(savgol_fit_png, dpi=240)
    ax.set_xlim(0.4, 2)
    ax.set_ylim(0.3, 0.6)
    fig.savefig(savgol_fit_peak_png, dpi=240)

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
    y_fit = savgol_filter(y, 201, 3)
    df.loc[start:, "savgol_descending"] = y_fit
    plt.close("all")
    fig, ax = plt.subplots()
    df_desc.plot(kind="scatter", x="time_ns", y="anisotropy", ax=ax)
    ax.plot(x, y_fit, color="r", label="savitzky-golay")

    start_poly = 300

    coeffs = poly.polyfit(x[start_poly:], y_fit[start_poly:], 2)
    x_fit = np.linspace(x[start_poly], 32, 200)
    # y_fit_sg_p = poly.polyval((x[500:], coeffs)
    y_fit_sg_p = poly.polyval(x_fit, coeffs)
    # ax.plot(x[500:], y_fit_sg_p, color="0.5", label="sg_p")
    ax.plot(x_fit, y_fit_sg_p, color="0.5", label="polynomial of savitzky-golay")
    ax.set_title("fit savitzky-golay with wider window to datapoints after peak")
    ax.legend()
    fig.savefig(savgol_fit_desc_png, dpi=240)