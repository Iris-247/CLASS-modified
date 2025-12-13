# CLASS-modified
Modified CLASS code for my graduation thesis, and also for practise.

# Undergraduate Thesis Project


**Research on the Impact of Dark Matter Properties on Gravitational Lensing Effects**

**Author**: Ma Tianyang (https://github.com/Iris-247)

**Date**: December 2025

**Supervisor**: Xu lixin

This repository contains a modified version of the official CLASS (Cosmic Linear Anisotropy Solving System) code to implement and compare two Warm Dark Matter (WDM) fluid-approximation models for my undergraduate thesis.

## Abstract

This thesis investigates the linear perturbation behavior of two fluid-approximation models of Warm Dark Matter (WDM) within the CLASS numerical framework. 

The first model, referred to as the **quasi-free-streaming model**, includes anisotropic stress by retaining density, velocity, and shear perturbations. This structure forms a simplified framework analogous to a truncated Boltzmann hierarchy. Numerical simulations demonstrate that this model leads to a scale-wide suppression of structure formation, which becomes more pronounced with increasing values of the equation-of-state parameter *w*. This effect is particularly evident in the matter power spectrum and CMB lensing potential, reflecting the enhanced smoothing of gravitational potentials caused by WDM free-streaming.

In contrast, the **entropy perturbation model** excludes the shear term and instead introduces non-adiabatic pressure and momentum feedback. Power suppression primarily appears at intermediate scales, and the overall response remains weak across variations in *w*. The lensing potential also shows limited sensitivity, suggesting that non-adiabatic effects alone contribute modestly to gravitational potential evolution. However, instabilities emerge at very large and small scales, indicating insufficient feedback closure in the absence of shear damping.

These behaviors are broadly consistent with the predictions of the Generalized Dark Matter (GDM) framework. This study provides a comparative characterization of two physically distinct WDM models and analyzes their respective impacts on structure growth and CMB lensing signatures.

**Key Words**: Warm Dark Matter; Non-cold Dark Matter; Linear Perturbation; Gravitational Lensing; CLASS

→ [Full Thesis PDF (42 pages)](https://your-pdf-link-here)  <!-- e.g., Baidu Netdisk or Google Drive share link -->

## Modifications
- Primary changes in `source/perturbations.c`: Implemented perturbation equations for both WDM models.
- Root directory: Added custom `.ini` files (`auto_ncdmf_nab_fw*.ini`) for systematic *w* parameter scans.

## Build and Run Instructions
Tested on Ubuntu Linux with GCC.


make clean && make -j8   # Compile (fast, ~1 minute)
./build/class auto_ncdmf_nab_fw50_synchronous.ini   # Run an example

#CLASS: Cosmic Linear Anisotropy Solving System  {#mainpage}
==============================================

Authors: Julien Lesgourgues, Thomas Tram, Nils Schoeneberg

with several major inputs from other people, especially Benjamin
Audren, Simon Prunet, Jesus Torrado, Miguel Zumalacarregui, Francesco
Montanari, Deanna Hooper, Samuel Brieden, Daniel Meinert, Matteo Lucca, etc.

For download and information, see http://class-code.net


Compiling CLASS and getting started
-----------------------------------

(the information below can also be found on the webpage, just below
the download button)

Download the code from the webpage and unpack the archive (tar -zxvf
class_vx.y.z.tar.gz), or clone it from
https://github.com/lesgourg/class_public. Go to the class directory
(cd class/ or class_public/ or class_vx.y.z/) and compile (make clean;
make class). You can usually speed up compilation with the option -j:
make -j class. If the first compilation attempt fails, you may need to
open the Makefile and adapt the name of the compiler (default: gcc),
of the optimization flag (default: -O4 -ffast-math) and of the OpenMP
flag (default: -fopenmp; this flag is facultative, you are free to
compile without OpenMP if you don't want parallel execution; note that
you need the version 4.2 or higher of gcc to be able to compile with
-fopenmp). Many more details on the CLASS compilation are given on the
wiki page

https://github.com/lesgourg/class_public/wiki/Installation

(in particular, for compiling on Mac >= 10.9 despite of the clang
incompatibility with OpenMP).

To check that the code runs, type:

    ./class explanatory.ini

The explanatory.ini file is THE reference input file, containing and
explaining the use of all possible input parameters. We recommend to
read it, to keep it unchanged (for future reference), and to create
for your own purposes some shorter input files, containing only the
input lines which are useful for you. Input files must have a *.ini
extension. We provide an example of an input file containing a
selection of the most used parameters, default.ini, that you may use as a
starting point.

If you want to play with the precision/speed of the code, you can use
one of the provided precision files (e.g. cl_permille.pre) or modify
one of them, and run with two input files, for instance:

    ./class test.ini cl_permille.pre

The files *.pre are suppposed to specify the precision parameters for
which you don't want to keep default values. If you find it more
convenient, you can pass these precision parameter values in your *.ini
file instead of an additional *.pre file.

The automatically-generated documentation is located in

    doc/manual/html/index.html
    doc/manual/CLASS_manual.pdf

On top of that, if you wish to modify the code, you will find lots of
comments directly in the files.

Python
------

To use CLASS from python, or ipython notebooks, or from the Monte
Python parameter extraction code, you need to compile not only the
code, but also its python wrapper. This can be done by typing just
'make' instead of 'make class' (or for speeding up: 'make -j'). More
details on the wrapper and its compilation are found on the wiki page

https://github.com/lesgourg/class_public/wiki

Plotting utility
----------------

Since version 2.3, the package includes an improved plotting script
called CPU.py (Class Plotting Utility), written by Benjamin Audren and
Jesus Torrado. It can plot the Cl's, the P(k) or any other CLASS
output, for one or several models, as well as their ratio or percentage
difference. The syntax and list of available options is obtained by
typing 'pyhton CPU.py -h'. There is a similar script for MATLAB,
written by Thomas Tram. To use it, once in MATLAB, type 'help
plot_CLASS_output.m'

Developing the code
--------------------

If you want to develop the code, we suggest that you download it from
the github webpage

https://github.com/lesgourg/class_public

rather than from class-code.net. Then you will enjoy all the feature
of git repositories. You can even develop your own branch and get it
merged to the public distribution. For related instructions, check

https://github.com/lesgourg/class_public/wiki/Public-Contributing

Using the code
--------------

You can use CLASS freely, provided that in your publications, you cite
at least the paper `CLASS II: Approximation schemes <http://arxiv.org/abs/1104.2933>`. Feel free to cite more CLASS papers!

Support
-------

To get support, please open a new issue on the

https://github.com/lesgourg/class_public

webpage!
