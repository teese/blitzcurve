==========
blitzcurve
==========

Data analysis of time-resolved fluorescence anisotropy measurements (TRAMs).

TRAMs are state-of-the-art techniques that can be used to analyse protein function and interaction.

Why use TRAM techniques?
~~~~~~~~~~~~~~~~~~~~~~~~

To measure molecule rotation speeds (e.g. protein size, structure, ligand binding).

To measure oligomerisation properties, via Foerster Resonance Energy Transfer (FRET) between two fluorescent molecules.

What is blitzcurve for?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* fitting curves to experimental TRAM data
* extracting useful fit parameters
* comparing samples

How does the experiment work?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* excitation of fluorescent molecules
* measurement of the depolorisation of the emitted light (polarisation / anisotropy)
* time-resolved methods: pulse excitation, and measurement of the change in anisotropy over time in nanoseconds

Analysis methods
~~~~~~~~~~~~~~~~

* appropriate fitting methods are still under development
* current input: csv with anisotropy and time (ns) values
* current fitting methods for anisotropy vs time
   - Savitzky Golay fit to all raw data
   - Exponential fit to initial decay data
   - Exponential fit to final decay data
* key measured parameters:
   - r_inf (predicted anisotropy at an infinite range in time)
   - r_max (maximum anisotropy measured at any timepoint)

Installation
~~~~~~~~~~~~
::

    pip install blitzcurve

* Blitzcurve should be compatable with `Anaconda python`__ 3.x or any scientific python package

.. _AnacondaLink: https://www.anaconda.com/download/

__ AnacondaLink_

Usage
~~~~~

.. code:: python

    import blitzcurve
    # define data directory with csv files
    data_dir = r"D:\data\20180229_TRdata"
    # OPTIONAL: define which data files will be analysed
    file_list = ["10nM-FGC1-2min_aniso.txt", "10nM-FGC2-2min_aniso.txt"]
    # run blitzcurve function to fit curves to individual samples
    blitzcurve.run_fit(data_dir, figs_to_plot=file_list)
    # setup a dictionary to shorten long sample names
    name_dict = {"10nM-FGC1-2min_aniso.txt": "FGC1", "10nM-FGC2-2min_aniso.txt": "FGC2", "10nM-FGC3-2min_aniso.txt": "FGC3"}
    # run blitzcurve function to compare curves and parameters for multiple samples
    blitzcurve.run_compare(data_dir, name_dict=name_dict)

Contribute
~~~~~~~~~~

Collaborators and pull requests are welcome. Send us an email.

License
~~~~~~~

This python package is released under the permissive MIT license.

Contact
~~~~~~~
Contact details are available at the staff pages of `Mark Teese`__ or `Philipp Heckmeier`__ within the `Langosch lab`__
of the Technical University of Munich.

.. _MarkWebsite: http://cbp.wzw.tum.de/index.php?id=49&L=1
.. _PhilippWebsite: http://cbp.wzw.tum.de/index.php?id=55
.. _LangoschWebsite: http://cbp.wzw.tum.de/index.php?id=9

__ MarkWebsite_
__ PhilippWebsite_
__ LangoschWebsite_


.. image:: https://raw.githubusercontent.com/teese/eccpy/master/docs/images/signac_seine_bei_samois.png
   :height: 150px
   :width: 250px

Examples
~~~~~~~~

**fit to obtain r_max**

.. image:: https://raw.githubusercontent.com/teese/blitzcurve/master/blitzcurve/images/aniso_savgol_fit.png
   :height: 500 px
   :width: 500 px

**fit to obtain r_inf**

.. image:: https://raw.githubusercontent.com/teese/blitzcurve/master/blitzcurve/images/aniso_seg2_fit.png
   :height: 500 px
   :width: 500 px

**full two phase exponential fit**

.. image:: https://raw.githubusercontent.com/teese/blitzcurve/master/blitzcurve/images/two_phase_exp_decay.png
   :height: 500 px
   :width: 500 px

**barchart comparing r_max**

.. image:: https://raw.githubusercontent.com/teese/blitzcurve/master/blitzcurve/images/01_barchart_r_max.png
   :height: 200 px
   :width: 200 px

**barchart comparing r_inf**

.. image:: https://raw.githubusercontent.com/teese/blitzcurve/master/blitzcurve/images/02_barchart_r_inf.png
   :height: 200 px
   :width: 200 px

**linechart comparing fit to full data for three samples**

.. image:: https://raw.githubusercontent.com/teese/blitzcurve/master/blitzcurve/images/06_linechart_savgol.png
   :height: 500 px
   :width: 500 px

**linechart comparing fit to r_inf for three samples**

.. image:: https://raw.githubusercontent.com/teese/blitzcurve/master/blitzcurve/images/08_linechart_seg2.png
   :height: 500 px
   :width: 500 px