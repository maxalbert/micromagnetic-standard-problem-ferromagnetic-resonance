#! /usr/bin/env python

""" Collection of all the common tools used in the project """
import os
import argparse

import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm

from transform_data import fft      # TODO: remove!
from transform_data import get_spectrum_via_method_1, get_spectrum_via_method_2
from transform_data import get_mode_amplitudes, get_mode_phases
from data_reader import DataReader


def make_figure2(data_reader):
    """
    Create Fig. 2 in the paper.

    Returns a matplotlib figure with two subfigures showing (a) the ringdown
    dynamics of the spatially averaged y-component of the magnetisation, m_y,
    and (b) the power spectrum obtained from a Fourier transform of m_y.
    """
    ts = data_reader.get_timesteps()
    dt = data_reader.get_dt()
    my = data_reader.get_average_magnetisation('y')

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))
    ax1.plot(ts * 1e9, my)
    ax1.set_xlabel('Time (ns)')
    ax1.set_ylabel('Magnetisation in Y')
    ax1.set_xlim([0, 2.5])

    freqs, psd1 = get_spectrum_via_method_1(my, dt)

    ax2.plot(freqs, psd1, '-', label='Real')
    ax2.set_xlabel('Frequency (GHz)')
    ax2.set_ylabel('Spectral density')
    ax2.set_xlim([0.1, 20])
    ax2.set_ylim([1e-5, 1e-0])
    ax2.set_yscale('log')

    fig.tight_layout()
    return fig


def make_figure3(data_reader):
    """
    Create Fig. 3 in the paper.

    Returns a matplotlib figure with two curves for the power
    spectral densities of the magnetisation dynamics computed
    via method 1 and 2 (as described in section C1 and C2).
    """
    dt = data_reader.get_dt()
    my_avg = data_reader.get_average_magnetisation('y')
    my_full = data_reader.get_spatially_resolved_magnetisation('y')
    freqs, psd1 = get_spectrum_via_method_1(my_avg, dt)
    freqs, psd2 = get_spectrum_via_method_2(my_full, dt)

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


def make_figure4_and_5(data_reader, software):

    def find_freq_index(f, n, dt):
        freqs = np.fft.fftfreq(n, dt)

        df = freqs[1] - freqs[0]
        for i in range(n):
            if abs(f - freqs[i]) < 1e-5 * df:
                return i

        raise Exception("Failed to find the index of given frequency!")

    def rescale_cmap(cmap_name, low=0.0, high=1.0, plot=False):
        import matplotlib._cm as _cm
        '''
        Example 1:
        # equivalent scaling to cplot_like(blah, l_bias=0.33, int_exponent=0.0)
        my_hsv = rescale_cmap('hsv', low = 0.3)
        Example 2:
        my_hsv = rescale_cmap(cm.hsv, low = 0.3)
        '''
        if type(cmap_name) is str:
            cmap = eval('_cm._%s_data' % cmap_name)
        else:
            cmap = eval('_cm._%s_data' % cmap_name.name)
        LUTSIZE = plt.rcParams['image.lut']
        r = np.array(cmap['red'])
        g = np.array(cmap['green'])
        b = np.array(cmap['blue'])
        range = high - low
        r[:, 1:] = r[:, 1:] * range + low
        g[:, 1:] = g[:, 1:] * range + low
        b[:, 1:] = b[:, 1:] * range + low
        _my_data = {'red': tuple(map(tuple, r)),
                    'green': tuple(map(tuple, g)),
                    'blue': tuple(map(tuple, b))
                    }
        my_cmap = mpl.colors.LinearSegmentedColormap('my_hsv', _my_data, LUTSIZE)

        if plot:
            print('plotting')
            plt.figure()
            plt.plot(r[:, 0], r[:, 1], 'r', g[:, 0], g[:, 1], 'g', b[:, 0],
                     b[:, 1], 'b', lw=3)
            plt.axis(ymin=-0.2, ymax=1.2)
            plt.show()

        return my_cmap

    # Different simulation tools produce slightly different peaks:
    if software.lower() == 'OOMMF'.lower():
        peaks = [8.25e9, 11.25e9, 13.9e9]
    elif software.lower() == 'Nmag'.lower():
        peaks = [8.1e9, 11.0e9, 13.5e9]
    else:
        raise ValueError(
            "You must specify the software used to generate the data")

    ts = data_reader.get_timesteps()
    dt = data_reader.get_dt()
    n = len(ts)

    nx = 24
    ny = 24

    res_figs = []

    for peak, fignum in zip(peaks, ['4', '5']):
        figname = "figure{}_{}.pdf".format(fignum, software)
        index = find_freq_index(peak, n, dt)

        peakGHz = str(round((peak * 1e-9), 4))

        amp_x = get_mode_amplitudes(data_reader, 'x', index, (nx, ny))
        amp_y = get_mode_amplitudes(data_reader, 'y', index, (nx, ny))
        amp_z = get_mode_amplitudes(data_reader, 'z', index, (nx, ny))

        phase_x = get_mode_phases(data_reader, 'x', index, (nx, ny))
        phase_y = get_mode_phases(data_reader, 'y', index, (nx, ny))
        phase_z = get_mode_phases(data_reader, 'z', index, (nx, ny))

        # Ensure that all three amplitude plots are on the same scale:
        minVal = np.min([amp_x, amp_y, amp_z])
        maxVal = np.max([amp_x, amp_y, amp_z])

        fig = plt.figure(figsize=(8, 6))
        gs = gridspec.GridSpec(2, 4, width_ratios=[4, 4, 4, 0.5],
                               height_ratios=[4, 4])

        my_hsv = rescale_cmap(cm.hsv, low=0.3, high=0.8, plot=False)

        cmap_amplitude = cm.coolwarm
        cmap_phase = my_hsv

        def plot_amplitudes(gs, data, label):
            ax = fig.add_subplot(gs)
            ax.imshow(data, cmap=cmap_amplitude, vmin=minVal, vmax=maxVal, origin='lower')
            ax.set_title(label)
            ax.set_xticks([])
            ax.set_yticks([])

        def plot_colorbar(gs, label, cmap, vmin, vmax, num_ticks, ticklabels=None):
            ax = fig.add_subplot(gs)
            norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
            ticks = np.linspace(vmin, vmax, num_ticks)
            cbar = mpl.colorbar.ColorbarBase(
                       ax, cmap, norm=norm, orientation='vertical', ticks=ticks)
            cbar.set_label(label)
            if ticklabels:
                cbar.ax.set_yticklabels(ticklabels)

        def plot_phases(gs, data, label):
            ax = fig.add_subplot(gs)
            ax.imshow(data, cmap=cmap_phase, vmin=-np.pi, vmax=np.pi, origin='lower')
            ax.set_title(label)
            ax.set_xticks([])
            ax.set_yticks([])

        plot_amplitudes(gs[0], amp_x, 'x')
        plot_amplitudes(gs[1], amp_y, 'y')
        plot_amplitudes(gs[2], amp_z, 'z')
        plot_colorbar(gs[3], 'Amplitude', cmap_amplitude, vmin=0, vmax=maxVal, num_ticks=5)

        plot_phases(gs[4], phase_x, 'x')
        plot_phases(gs[5], phase_y, 'y')
        plot_phases(gs[6], phase_z, 'z')
        plot_colorbar(gs[7], 'Phase', cmap_phase, vmin=-np.pi, vmax=np.pi, num_ticks=3, ticklabels=['-3.14', '0', '-3.14'])

        fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, wspace=0.1)
        fig.suptitle('%s GHz' % peakGHz, fontsize=20)
        fig.tight_layout()
        res_figs.append(fig)

    return res_figs


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

    if args.figures:
        make_figure2(data_reader)
        make_figure3(data_reader)

        figure4_and_5(data_reader, software)
