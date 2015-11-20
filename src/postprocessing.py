#! /usr/bin/env python

""" Collection of all the common tools used in the project """
import os
import argparse

import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from transform_data import fft  # TODO: remove!
from transform_data import fft_new
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

    freq, ft_abs, phase = fft(my, dt)

    # We plot the log of the power spectrum, for clarity
    ft_power = ft_abs ** 2
    length = len(freq) / 2

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))
    ax1.plot(ts * 1e9, my)
    ax1.set_xlabel('Time (ns)')
    ax1.set_ylabel('Magnetisation in Y')
    ax1.set_xlim([0, 2.5])

    ax2.plot(freq[0:length] * 1e-9, ft_power[0:length], '-', label='Real')
    ax2.set_xlabel('Frequency (GHz)')
    ax2.set_ylabel('Spectral density')
    ax2.set_xlim([0.1, 20])
    ax2.set_ylim([1e-5, 1e-0])
    ax2.set_yscale('log')

    fig.tight_layout()
    return fig


def make_figure3(data_reader, mys_ft_absLoc):
    ts = data_reader.get_timesteps()
    dt = data_reader.get_dt()
    my = data_reader.get_average_magnetisation('y')

    freq, ft_abs, phase = fft(my, dt)
    ft_power = ft_abs ** 2

    mys = np.load(mys_ft_absLoc)
    averaged = np.average(mys ** 2, axis=0)

    length = len(freq) / 2
    #freqs = freq[0:length] * 1e-9
    #ft_power = ft_power[0:length]
    averaged = averaged[0:length]

    freqs2, ft_power2, _ = fft_new(my, dt)
    #assert np.allclose(freqs2, freqs)
    #assert np.allclose(ft_power2, ft_power)

    #fft_computer = FFTComputer(data_reader)
    #freqs = fft_computer.get_frequencies()
    #averaged = fft_computer.get_spectral_density(spatially_resolved=False)
    #ft_power = fft_computer.get_spectral_density(spatially_resolved=True)

    fig = plt.figure(figsize=(7, 5.5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(freqs2, ft_power2, label='Spatially Averaged')
    ax.plot(freqs2, averaged, color="g", lw=2, label='Spatially Resolved')
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Spectral density')
    ax.set_xlim([0.2, 20])
    ax.set_ylim([1e-5, 1e0])
    ax.set_yscale('log')
    ax.legend(frameon=False)

    return fig


def make_figure4_and_5(txyzFileLoc,
                       mxs_ft_absLoc, mys_ft_absLoc, mzs_ft_absLoc,
                       mxs_ft_phaseLoc, mys_ft_phaseLoc, mzs_ft_phaseLoc,
                       software):

    import matplotlib.gridspec as gridspec
    import matplotlib as mpl
    import matplotlib.colors as colors
    from matplotlib import cm

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
        my_cmap = colors.LinearSegmentedColormap('my_hsv', _my_data, LUTSIZE)

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

    data = np.loadtxt(txyzFileLoc)
    ts = data[:, 0]
    n = len(ts)
    dt = ts[1] - ts[0]

    nx = 24
    ny = 24

    mx_abs = np.load(mxs_ft_absLoc)
    my_abs = np.load(mys_ft_absLoc)
    mz_abs = np.load(mzs_ft_absLoc)

    mx_phase = np.load(mxs_ft_phaseLoc)
    my_phase = np.load(mys_ft_phaseLoc)
    mz_phase = np.load(mzs_ft_phaseLoc)

    res_figs = []

    for peak, fignum in zip(peaks, ['4', '5']):
        figname = "figure{}_{}.pdf".format(fignum, software)
        index = find_freq_index(peak, n, dt)

        peakGHz = str(round((peak * 1e-9), 4))

        amp_x = mx_abs[:, index].reshape((ny, nx))
        amp_y = my_abs[:, index].reshape((ny, nx))
        amp_z = mz_abs[:, index].reshape((ny, nx))

        phase_x = mx_phase[:, index].reshape((ny, nx))
        phase_y = my_phase[:, index].reshape((ny, nx))
        phase_z = mz_phase[:, index].reshape((ny, nx))

        # Ensure that all three amplitude plots are on the same scale:
        max_X = np.amax(amp_x)
        max_Y = np.amax(amp_y)
        max_Z = np.amax(amp_z)
        maxVal = max([max_X, max_Y, max_Z])

        min_X = np.amin(amp_x)
        min_Y = np.amin(amp_y)
        min_Z = np.amin(amp_z)
        minVal = min([min_X, min_Y, min_Z])

        fig = plt.figure(figsize=(8, 6))
        gs = gridspec.GridSpec(2, 4, width_ratios=[4, 4, 4, 0.5],
                               height_ratios=[4, 4])
        plt.subplot(gs[0])
        ax = plt.gca()
        plt.imshow(amp_x, cmap=plt.cm.coolwarm, vmin=minVal, vmax=maxVal,
                   origin='lower')
        plt.title('x')
        plt.xticks([])
        plt.yticks([])

        plt.subplot(gs[1])
        ax = plt.gca()
        plt.imshow(amp_y, cmap=plt.cm.coolwarm, vmin=minVal, vmax=maxVal,
                   origin='lower')
        plt.title('y')
        plt.xticks([])
        plt.yticks([])

        plt.subplot(gs[2])
        ax = plt.gca()
        plt.imshow(amp_z, cmap=plt.cm.coolwarm, vmin=minVal, vmax=maxVal,
                   origin='lower')
        plt.xticks([])
        plt.yticks([])
        plt.title('z')

        plt.subplot(gs[3])
        ax = plt.gca()
        norm = mpl.colors.Normalize(vmin=minVal, vmax=maxVal)
        cb1 = mpl.colorbar.ColorbarBase(ax, plt.cm.coolwarm, norm=norm,
                                        orientation='vertical',
                                        ticks=[0, maxVal * 0.25, maxVal * 0.5,
                                               maxVal * 0.75, maxVal])
        cb1.set_label('Amplitude')

        my_hsv = rescale_cmap(cm.hsv, low=0.3, high=0.8, plot=False)

        plt.subplot(gs[4])
        ax = plt.gca()
        plt.imshow(phase_x, cmap=my_hsv, vmin=-np.pi, vmax=np.pi,
                   origin='lower')
        plt.title('x')
        plt.xticks([])
        plt.yticks([])

        plt.subplot(gs[5])
        ax = plt.gca()
        plt.imshow(phase_y, cmap=my_hsv, vmin=-np.pi, vmax=np.pi,
                   origin='lower')
        plt.title('y')
        plt.xticks([])
        plt.yticks([])

        plt.subplot(gs[6])
        ax = plt.gca()
        plt.imshow(phase_z, cmap=my_hsv, vmin=-np.pi, vmax=np.pi)
        plt.xticks([])
        plt.yticks([])
        plt.title('z')

        plt.subplot(gs[7])
        ax = plt.gca()

        norm = mpl.colors.Normalize(vmin=-np.pi, vmax=np.pi)
        cb1 = mpl.colorbar.ColorbarBase(ax, my_hsv, norm=norm,
                                        orientation='vertical',
                                        ticks=[-3.14, 0, 3.14])
        cb1.set_label('Phase')

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
        make_figure3(data_reader, "mys_ft_abs.npy")

        figure4_and_5("./dynamic_txyz.txt",
                      "mxs_ft_abs.npy", "mys_ft_abs.npy", "mzs_ft_abs.npy",
                      "mxs_ft_phase.npy", "mys_ft_phase.npy",
                      "mzs_ft_phase.npy",
                      software)
