# blitzcurve #

Data analysis of time-resolved fluorescence anisotropy measurements (TRAMs).

### Background ###

TRAMs are state-of-the-art techniques that can be used to analyse protein function and interaction. 

Aims:
* measure molecule rotation speeds (e.g. protein size, structure, ligand binding)
* measure oligomerisation properties, via Förster Resonance Energy Transfer (FRET) between two fluorescent molecules

Experimental methods:
* excitation of fluorescent molecules
* measurement of the depolorisation of the emitted light (polarisation / anisotropy)
* time-resolved methods: pulse excitation, and measurement of the change in anisotropy over time in nanoseconds

Analysis methods:
* methods are still under development for the quantitative of TRAM data
* key parameters include:
  * r_inf (predicted anisotropy at an infinite range in time)
  * r_max (maximum anisotropy measured at any timepoint)

### What is this repository for? ###

* fitting curves to experimental TRAM data
  * current input: experimentally determined anisotropy and time (ns) data
* extracting useful fit parameters
* comparing samples

### How do I get set up? ###

* Recommended python package: Install Anaconda python 3.x or any scientific python package
* From Github : download blitzcurve as zip from GitHub, or install using git
* Run "python setup.py install"

### Who do I talk to? ###

* Mark Teese
* Philipp Heckmeier