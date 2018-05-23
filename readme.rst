==========
blitzcurve
==========

Data analysis of time-resolved fluorescence anisotropy measurements (TRAMs).

Background
~~~~~~~~~~

TRAMs are state-of-the-art techniques that can be used to analyse protein function and interaction.

Why use TRAM techniques?
~~~~~~~~~~~~~~~~~~~~~~~~

To measure molecule rotation speeds (e.g. protein size, structure, ligand binding)
To measure oligomerisation properties, via Förster Resonance Energy Transfer (FRET) between two fluorescent molecules

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