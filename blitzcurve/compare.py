import glob
import os
import pickle
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle
from blitzcurve.utils import setup_matplotlib_dark_background
import blitzcurve.utils as utils
import sys
import blitzcurve

def run_compare(data_dir, file_list="all", name_dict= None):
    """

    Parameters
    ----------
    data_dir : str
        Path to directory with the input text files.
    file_list : str, list
        List of files to analyse.
        E.g. ["10nM-FGC1-2min_aniso.txt", "10nM-FGC2-2min_aniso.txt"]
        Default is "all", which analyses all files in folder
    name_dict : dict
        Dictionary to rename long filenames for plotting.

    Returns
    -------

    Usage
    -----
    import blitzcurve
    data_dir = r"D:\data\20180229_TRdata"
    # fit
    blitzcurve.run_fit(data_dir, figs_to_plot=figs_to_plot, testing_mode=False)
    # compare
    name_dict = {"10nM-FGC1-2min_aniso.txt": "FGC1", "10nM-FGC2-2min_aniso.txt": "FGC2", "10nM-FGC3-2min_aniso.txt": "FGC3"}
    blitzcurve.run_compare(data_dir, name_dict=name_dict)
    """

    # create object with the compare file paths
    cfp = utils.CompareFilePaths(data_dir)

    setup_matplotlib_dark_background(plt)

    fc = utils.FlourescentColours()
    csv_files = glob.glob(os.path.join(data_dir, "*.txt"))

    # drop any files not in the list
    if file_list != "all":
        for csv in csv_files:
            if os.path.basename(csv) not in file_list:
                csv_files.remove(csv)

    summ_csv = os.path.join(data_dir, "summary", "fit_summary.csv")
    df = pd.read_csv(summ_csv, index_col=0)

    df["orig_names"] = df.index

    if name_dict is not None:
        # rename the index
        df.rename(index=name_dict, inplace=True)
    else:
        # no naming dict available
        # cut off the ".txt" in the filename before plotting.
        df.index = df.index.str[:-4]

    create_barcharts = True

    if create_barcharts:
        #########################################################################
        #                   Barchart maximum anisotropy                         #
        #########################################################################
        fig, ax = plt.subplots()
        width = 0.6
        df["r_max"].plot(kind="bar", ax=ax, color=fc.blue, width=width, label="segment 1")
        ax.set_ylabel(r"$r_{max}$", fontsize=16)
        # adjust margins around bars
        ax.set_xlim(-0.6, df.shape[0] - 0.4)
        ax.set_ylim(df["r_max"].min() - 0.005, df["r_max"].max() + 0.005)
        fig.tight_layout()
        fig.savefig(cfp.barchart_r_max)
        sys.stdout.write("\n{}".format(cfp.barchart_r_max))

        #########################################################################
        #                              Barchart r_inf                           #
        #########################################################################
        fig, ax = plt.subplots()
        width = 0.6
        df["r_inf"].plot(kind="bar", ax=ax, color=fc.blue, width=width, label="segment 1")
        ax.set_ylabel(r"$r_{inf}$", fontsize=16)
        # adjust margins around bars
        ax.set_xlim(-0.6, df.shape[0] - 0.4)
        ax.set_ylim(df["r_inf"].min() - 0.005, df["r_inf"].max() + 0.005)
        fig.tight_layout()
        fig.savefig(cfp.barchart_r_inf)
        sys.stdout.write("\n{}".format(cfp.barchart_r_inf))

        #########################################################################
        #               Barchart variable a, segments 1 and 2                   #
        #########################################################################

        #generate only dataframe with a_seg1 and a_seg2
        df_a_bars = pd.concat([df["a_seg1"], df["a_seg2"]], axis=1)
        df_a_bars.columns = ["a_seg1", "a_seg2"]

        fig, ax = plt.subplots()
        width = 0.8
        df_a_bars.plot(kind="bar", ax=ax, color=[fc.blue,fc.lemon], width=width, legend=False)
        #gets handles for the legend (also gets and labels - rudimentary)
        handles, labels = ax.get_legend_handles_labels()
        #brings segment b to secondary y axis
        ax2 = ax.twinx()
        for r in ax.patches[len(df_a_bars):]:
            r.set_transform(ax2.transData)
        #defines labels
        labels = ["segment 1", "segment 2"]

        ax.set_ylabel("variable a in segment 1", color=fc.blue)
        ax.tick_params("y", colors=fc.blue)
        ax2.set_ylabel("variable a in segment 2", color=fc.lemon)
        ax2.tick_params("y", colors=fc.lemon)
        # adjust margins around bars
        ax.set_xlim(-0.6, df.shape[0] - 0.4)
        ax.set_ylim(df["a_seg1"].min() - 0.005, df["a_seg1"].max() + 0.01)
        ax2.set_ylim(df["a_seg2"].min() - 0.005, df["a_seg2"].max() + 0.01)
        fig.legend(handles,labels,ncol=2, loc="upper center", bbox_to_anchor=(0, 0.85, 1.1, .102))

        fig.tight_layout()
        fig.savefig(cfp.barchart_variable_a_png)
        sys.stdout.write("\n{}".format(cfp.barchart_variable_a_png))


        #########################################################################
        #               Barchart variable b, segments 1 and 2                   #
        #########################################################################

        #generate only dataframe with b_seg1 and b_seg2
        df_b_bars = pd.concat([df["b_seg1"], df["b_seg2"]], axis=1)
        df_b_bars.columns = ["b_seg1", "b_seg2"]

        fig, ax = plt.subplots()
        width = 0.8
        df_b_bars.plot(kind="bar", ax=ax, color=[fc.blue, fc.lemon], width=width, legend=False)
        # gets handles for the legend (also gets and labels - rudimentary)
        handles, labels = ax.get_legend_handles_labels()
        # brings segment b to secondary y axis
        ax2 = ax.twinx()
        for r in ax.patches[len(df_b_bars):]:
            r.set_transform(ax2.transData)
        # defines labels
        labels = ["segment 1", "segment 2"]

        ax.set_ylabel("variable b in segment 1", color=fc.blue)
        ax.tick_params("y", colors=fc.blue)
        ax2.set_ylabel("variable b in segment 2", color=fc.lemon)
        ax2.tick_params("y", colors=fc.lemon)
        # adjust margins around bars
        ax.set_xlim(-0.6, df.shape[0] - 0.4)
        ax.set_ylim(df["b_seg1"].min() - 0.005, df["b_seg1"].max() + 0.02)
        ax2.set_ylim(df["b_seg2"].min() - 0.005, df["b_seg2"].max() + 0.02)
        fig.legend(handles,labels,ncol=2, loc="upper center", bbox_to_anchor=(0, 0.85, 1.1, .102))

        fig.tight_layout()
        fig.savefig(cfp.barchart_variable_b_png)
        sys.stdout.write("\n{}".format(cfp.barchart_variable_b_png))

        #########################################################################
        #               Barchart variable c, segments 1 and 2 (r_inf)           #
        #########################################################################
        plt.close("all")

        # generate only dataframe with c_seg1 and r_inf
        df_c_rinf_bars = pd.concat([df["c_seg1"], df["r_inf"]], axis=1)
        df_c_rinf_bars.columns = ["c_seg1", "r_inf"]

        fig, ax = plt.subplots()
        width = 0.8
        df_c_rinf_bars.plot(kind="bar", ax=ax, color=[fc.blue, fc.lemon], width=width, legend=False)
        # gets handles for the legend (also gets and labels - rudimentary)
        handles, labels = ax.get_legend_handles_labels()
        # brings segment b to secondary y axis
        ax2 = ax.twinx()
        for r in ax.patches[len(df_c_rinf_bars):]:
            r.set_transform(ax2.transData)
        # defines labels
        labels = ["segment 1", "segment 2"]

        ax.set_ylabel("variable c in segment 1", color=fc.blue)
        ax.tick_params("y", colors=fc.blue)
        ax2.set_ylabel("variable c (r_inf) in segment 2", color=fc.lemon)
        ax2.tick_params("y", colors=fc.lemon)
        # adjust margins around bars
        ax.set_xlim(-0.6, df.shape[0] - 0.4)
        ax.set_ylim(df["c_seg1"].min() - 0.005, df["c_seg1"].max() + 0.01)
        ax2.set_ylim(df["r_inf"].min() - 0.005, df["r_inf"].max() + 0.01)

        fig.legend(handles,labels,ncol=2, loc="upper center", bbox_to_anchor=(0, 0.85, 1.1, .102))
        fig.tight_layout()
        fig.savefig(cfp.barchart_variable_c_png)
        sys.stdout.write("\n{}".format(cfp.barchart_variable_c_png))


    fig_sg, ax_sg = plt.subplots()
    fig_seg1, ax_seg1 = plt.subplots()
    fig_seg2, ax_seg2 = plt.subplots()

    for csv in csv_files:
        # paths for the output files
        p = utils.FitFilePaths(data_dir, csv)
        with open(p.fitdata_pickle, "rb") as pic:
            #fd = blitzcurve.fit.OutputFitData()
            fd = pickle.load(pic)
            print("fd.filename", fd.filename)
            #for item in [fd.fit_savgol, fd.seg1_xfit, fd.seg1_yfit, fd.seg2_xfit, fd.seg2_yfit]:
            #    assert item is not None
            if name_dict is not None:
                label = name_dict[fd.filename] if fd.filename in name_dict else fd.filename
            else:
                label = fd.filename
            ax_sg.plot(fd.time, fd.y_fit_savgol, label=label)

            ax_seg1.plot(fd.time, fd.y_fit_savgol, color="0.3", zorder=0)
            ax_seg1.plot(fd.seg1_xfit, fd.seg1_yfit, label=label)

            ax_seg2.plot(fd.time, fd.y_fit_savgol, color="0.3", zorder=0)
            ax_seg2.plot(fd.seg2_xfit, fd.seg2_yfit, label=label)

    ax_sg.set_xlabel("time (ns)")
    ax_sg.set_ylabel("anisotropy, r")
    ax_sg.legend()
    fig_sg.tight_layout()
    fig_sg.savefig(cfp.linechart_savgol)

    ax_seg1.set_xlabel("time (ns)")
    ax_seg1.set_ylabel("anisotropy, r")
    ax_seg1.legend()
    fig_seg1.tight_layout()
    fig_seg1.savefig(cfp.linechart_seg1)

    ax_seg2.set_xlabel("time (ns)")
    ax_seg2.set_ylabel("anisotropy, r")
    ax_seg2.legend()
    fig_seg2.tight_layout()
    fig_seg2.savefig(cfp.linechart_seg2)

