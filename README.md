[![Build Status](https://travis-ci.org/maxalbert/micromagnetic-standard-problem-ferromagnetic-resonance.svg?branch=master)](https://travis-ci.org/maxalbert/micromagnetic-standard-problem-ferromagnetic-resonance)

# Proposal of a micromagnetic standard problem for ferromagnetic resonance simulations

This repository accompanies the paper _"Proposal of a standard problem for ferromagnetic resonance simulations"_ available at _[...]_.
It provides the data files and scripts which allow the reader to reproduce these results.

Start by reading ["Quick start"](#quick-start) below to get an overview of the contents of this repository and how you can use it.

## Authors
Alexander Baker, Marijan Beg, Gregory Ashton, Weiwei Wang,
Maximilian Albert, Dmitri Chernyshenko, Shilei Zhang, Marc-Antonio Bisotti, Matteo Franchin,
Chun Lian Hu, Robert Stamps, Thorsten Hesjedal, and Hans Fangohr*

*fangohr@soton.ac.uk

## Quick start

Depending on your expertise and interest, you can use this repository in various ways.

- Browse or download the data files underlying the figures 2 to 5 in the paper.

- Re-produce the main figures 2 to 5 in the paper. (No micromagnetic software needed.)

- Run our micromagnetic simulation scripts to re-generate the data files (OOMMF required).


The [data/](./data/) subfolder contains the data files from which Figures 2 and 3 in the paper are generated. You can look at the ["Guide to reproducing figures"](Guide_to_reproducing_figures.ipynb) to see how these figures are produced. Since the guide is written as a Jupyter notebook (see the [Jupyter documentation](https://jupyter.readthedocs.org/) for more information), you can also execute it yourself to reproduce the figures from the data. _TODO: Add a comment to say that this notebook duplicates the contents of some of the scripts in the `src/` folder._ These data files may also be useful to compare our results with output produced by your own software, so you may want to download them. None of these steps requires any micromagnetic software to be installed.

The [src/](./src/) subfolder contains scripts for two purposes:

  - To produce the main figures in the paper. These scripts are an extended (and more automated) version of the ["Guide to reproducing figures"](Guide_to_reproducing_figures.ipynb) mentioned above). _TODO: Clarify how the scripts relate to the notebook and which code is duplicated._ Running these also does not require any micromagnetic software.

  - To re-generate the data files underlying the figures in the paper. The relevant scripts implement the simulation setup for the FMR standard problem which we propose in the paper. You can use these in conjunction with two different micromagnetic software packages (OOMMF, Nmag) to produce the actual data files. We have automated as much of this as possible; see the section ["Reproducing results"](#reproducing-results) below for details.

    Running these scripts requires the relevant software to be installed. See the section ["Software"](#software) for details.


## Software

To run the code in this repository, the following software must be installed:

* [OOMMF](http://math.nist.gov/oommf/)
* [Nmag](http://nmag.soton.ac.uk/nmag/)
* [Python](https://www.python.org)
* Python modules:
  * numpy
  * matplotlib

_TODO: Mention the versions that are required (if any), or at least the ones we used for testing._


### Checking the installation

To check you have the required software:

* For `OOMMF` please check the output of

    ```bash
    $ tclsh $OOMMFTCL +version
    ```

  Note that `$OOMMFTCL` is an environment variable pointing to the installed
  `oommf.tcl` file in the directory where `OOMMF` is installed. This can be
  set in `.bashrc` by

    ```bash
    export OOMMFTCL=/path/to/install/oommf/oommf.tcl
    ```

  For more information on installing and running OOMMF, refer to:
  http://math.nist.gov/oommf/software-12.html

* For `Nmag` check your installation by running

    ```bash
    nsim --version
    ```

  For more information on installing and running Nmag, refer to:
  http://nmag.soton.ac.uk

## Instructions

### Cloning

To get a local copy of this repository, clone it by running

```bash
git clone https://github.com/fangohr/micromagnetic-standard-problem-ferromagnetic-resonance.git
```

### Reproducing results

This repository contains scripts to reproduce the standard problem results as
presented in the paper. There are two directories in `src/` directory: `nmag_scripts/` and `oommf_scripts/`. Each directory contains the scripts to create figures 2, 3, 4 and 5 from the paper. For each folder we include a `Makefile` which can be run in several ways:

1. To produce figures using the data in the repository, execute `make figures`.

2. To produce the data, execute `make data`.

3. Executing `make clean_all`, deletes all figures and data from the current directory, and then `make all` can be executed. This will generate both the data and figures without using any precomputed (saved) data.

If the data provided by this repository has been overwritten, the data can be retrieved by:

```bash
$ git checkout Dynamic_txyz.txt mxs.npy mys.npy mzs.npy
```

### Nmag mesh discretization

As discussed in the section 3D of the paper, finite element and finite difference techniques produce slightly different results due to their different handling
of demagnetization energy.

The finite element approach can be brought into agreement with finite difference through an appropriate choice of mesh discretization. The standard simulation uses one based on a 5x5x5nm cell size, but in figure 13 we show the spectra resulting from a 2x2x1nm cell size. This mesh is also provided, and can be utilized in simulations by changing the variable `mesh_name` in both `relaxation_stage.py` and `dynamic_stage.py` to `mesh_name = meshes/mesh_221.nmesh.h5`
