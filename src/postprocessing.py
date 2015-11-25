#! /usr/bin/env python

""" Collection of all the common tools used in the project """
import os
import argparse

import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm

from transform_data import fft      # TODO: remove!
from transform_data import get_mode_amplitudes, get_mode_phases
from data_reader import DataReader
from eigenmode_plotter import EigenmodePlotter


def make_figure2(data_reader, component='y'):
    """
    Create Fig. 2 in the paper.

    Returns a matplotlib figure with two subfigures showing (a) the ringdown
    dynamics of the spatially averaged y-component of the magnetisation, m_y,
    and (b) the power spectrum obtained from a Fourier transform of m_y.
    """
    # Read timesteps and spatially averaged magnetisation (y-component).
    ts = data_reader.get_timesteps(unit='ns')
    mys = data_reader.get_average_magnetisation(component)

    # Compute power spectrum from averaged magnetisation.
    freqs = data_reader.get_fft_frequencies(unit='GHz')
    dt = data_reader.get_dt()
    psd = data_reader.get_spectrum_via_method_1(component)

    # Plot magnetisation dynamics and power spectrum into two subplots.
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))

    ax1.plot(ts, mys)
    ax1.set_xlabel('Time (ns)')
    ax1.set_ylabel('Magnetisation in Y')
    ax1.set_xlim([0, 2.5])

    ax2.plot(freqs, psd, '-', label='Real')
    ax2.set_xlabel('Frequency (GHz)')
    ax2.set_ylabel('Spectral density')
    ax2.set_xlim([0.1, 20])
    ax2.set_ylim([1e-5, 1e-0])
    ax2.set_yscale('log')

    fig.tight_layout()
    return fig


def make_figure3(data_reader, component='y'):
    """
    Create Fig. 3 in the paper.

    Returns a matplotlib figure with two curves for the power
    spectral densities of the magnetisation dynamics computed
    via method 1 and 2 (as described in section C1 and C2).
    """
    dt = data_reader.get_dt()

    # Read average and spatially resolved magnetisation (y-component).
    mys_avg = data_reader.get_average_magnetisation(component)
    mys_full = data_reader.get_spatially_resolved_magnetisation(component)

    # Compute frequencies and power spectrum via the two different methods.
    freqs = data_reader.get_fft_frequencies(unit='GHz')
    psd1 = data_reader.get_spectrum_via_method_1(component)
    psd2 = data_reader.get_spectrum_via_method_2(component)

    # Plot both power spectra into the same figure
    fig = plt.figure(figsize=(7, 5.5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(freqs, psd1, label='Spatially Averaged')
    ax.plot(freqs, psd2, color='g', lw=2, label='Spatially Resolved')
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Spectral density')
    ax.set_xlim([0.2, 20])
    ax.set_ylim([1e-5, 1e0])
    ax.set_yscale('log')
    ax.legend(frameon=False)

    return fig


def make_figure_4(data_reader):
    if data_reader.software == 'OOMMF':
        peak_freq = 8.25e9
    elif data_reader.software == 'Nmag':
        peak_freq = 8.1e9
    else:
        raise RuntimeError()
    eigenmode_plotter = EigenmodePlotter(data_reader)
    fig = eigenmode_plotter.plot_mode(peak_freq)
    return fig


def make_figure_5(data_reader):
    if data_reader.software == 'OOMMF':
        peak_freq = 11.25e9
    elif data_reader.software == 'Nmag':
        peak_freq = 11e9
    else:
        raise RuntimeError()
    eigenmode_plotter = EigenmodePlotter(data_reader)
    fig = eigenmode_plotter.plot_mode(peak_freq)
    return fig


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Helper function for micromagnetic_standard_problem_FMR")

    parser.add_argument("--figures", help="Generate Figs~(2-5)",
                        action="store_true")
    parser.add_argument("--software", help="Software used to create data",
                        default="")

    args = parser.parse_args()
    software = args.software

    data_reader = DataReader(data_dir='../../data/oommf/', software='OOMMF')
    component = 'y'

    if args.figures:
        make_figure2(data_reader, component)
        make_figure3(data_reader, component)
        make_figure4(data_reader)
        make_figure5(data_reader)
