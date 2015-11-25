#!/usr/bin/env python

import numpy as np
import os


def fft(mx, dt=5e-12):
    """ FFT of the data at dt """
    n = len(mx)
    freq = np.fft.fftfreq(n, dt)

    ft_mx = np.fft.fft(mx)

    ft_abs = np.abs(ft_mx)
    ft_phase = np.angle(ft_mx)

    return freq, ft_abs, ft_phase


def fft_new(mx, dt=5e-12):
    """ FFT of the data at dt """
    n = len(mx)
    freq = np.fft.fftfreq(n, dt)

    ft_mx = np.fft.fft(mx)

    ft_abs = np.abs(ft_mx)
    ft_phase = np.angle(ft_mx)

    freqs = freq[:(n//2)] * 1e-9
    ft_power = ft_abs[:(n//2)]**2
    return freqs, ft_power, ft_phase[:(n//2)]


def fft_real(mx, dt=5e-12):
    """ FFT of the data at dt """
    n = len(mx)
    rfreq = np.fft.rfftfreq(n, dt)

    rft_mx = np.fft.rfft(mx)

    rft_abs = np.abs(rft_mx)
    rft_phase = np.angle(rft_mx)

    # Ignore the last element for the time being so that we can
    # compare with the arrays as they are currently computed.
    rfreqs = rfreq[:-1] * 1e-9
    rft_power = rft_abs[:-1]**2
    return rfreqs, rft_power, rft_phase


def get_mode_amplitudes(data_reader, component, idx, shape):
    data = data_reader.get_spatially_resolved_magnetisation(component)
    ft_data = np.fft.rfft(data, axis=0)
    amplitudes = np.abs(ft_data[idx, :])
    return amplitudes.reshape(shape)


def get_mode_phases(data_reader, component, idx, shape):
    data = data_reader.get_spatially_resolved_magnetisation(component)
    ft_data = np.fft.rfft(data, axis=0)
    amplitudes = np.angle(ft_data[idx, :])
    return amplitudes.reshape(shape)


def spatial_fft(dataname):
    """ Spatially averaged FFT as defined in Eqn. (5) """
    ft_abs = []
    ft_phase = []

    mys = np.load(dataname)
    m, n = mys.shape

    for i in range(n):
        f, ft_a, ft_p = fft(mys[:, i])
        ft_abs.append(ft_a)
        ft_phase.append(ft_p)

    np.save(dataname[:-4] + '_ft_abs.npy', np.array(ft_abs))
    np.save(dataname[:-4] + '_ft_phase.npy', np.array(ft_phase))


def transform_data():
    """ Helper function to spatially transform data for each direction"""
    for direction in ["x", "y", "z"]:
        source = 'm{}s.npy'.format(direction)
        targetA = 'm{}s_ft_abs.npy'.format(direction)
        targetB = 'm{}s_ft_phase.npy'.format(direction)

        if not os.path.isfile(source):
            raise IOError("Source file {} does not exist in the current "
                " directory. Try running the Makefile".format(source))
        if not os.path.isfile(targetA) or not os.path.isfile(targetB):
            spatial_fft(source)


if __name__ == '__main__':
    transform_data()
