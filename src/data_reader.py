import numpy as np
import os


class DataReader(object):
    """
    This class facilitates loading of raw data (as produced
    by OOMMF or Nmag) in a unified way, suitable for further
    post-processing or visualisation.
    """
    def __init__(self, data_dir, software):
        self.data_dir = data_dir
        self.software = software
        assert self.software in ['OOMMF', 'Nmag']

        data_avg_filename = os.path.join(self.data_dir, 'dynamic_txyz.txt')
        self.data_avg = np.loadtxt(data_avg_filename)

    @staticmethod
    def _convert_to_unit(val, unit):
        if unit == 's':
            return val
        elif unit == 'ns':
            return val * 1e9
        else:
            msg = ("The argument `unit` must be either 's' (= seconds) "
                   "or 'ns' (= nanoseconds). Got: '{}'".format(unit))
            raise ValueError(msg)

    def get_timesteps(self, unit='s'):
        """
        Return a 1D numpy array containing the timesteps at which
        the magnetisation was saved during the simulation.

        The argument `unit` can either be 's' (= seconds) or 'ns'
        (= nanoseconds).
        """
        # Timestamps are contained in the first column of the averaged data
        timesteps = self.data_avg[:, 0]
        return self._convert_to_unit(timesteps, unit)

    def get_num_timesteps(self):
        return len(self.get_timesteps())

    def get_dt(self, unit='s'):
        """
        Return the size of the timestep used during the simulation.
        This is determined as the difference between the first and
        second timestep of the simulation run (all subsequent
        timesteps are ignored). In particular, it assumes that all
        timesteps used in the simulation are equal.
        """
        ts = self.get_timesteps()
        dt = ts[1] - ts[0]
        return self._convert_to_unit(dt, unit)

    @staticmethod
    def _get_index_of_m_avg_component(component):
        """
        Internal helper function to return the column index for
        the x/y/z component of the average magnetisation.
        """
        try:
            idx = {'x': 1, 'y': 2, 'z': 3}[component]
        except IndexError:
            raise ValueError(
                "Argument 'component' must be one of 'x', 'y', 'z'. "
                "Got: '{}'".format(component))
        return idx

    def get_average_magnetisation(self, component):
        """
        Return a 1D numpy array containing the values of the
        spatially averaged magnetization sampled at the time-
        steps during the simulation.
        """
        idx = self._get_index_of_m_avg_component(component)
        return self.data_avg[:, idx]

    def get_spatially_resolved_magnetisation(self, component):
        """
        Return a numpy array of shape (N, nx, ny) containing the values
        of the spatially resolved magnetization sampled at all N timesteps
        the simulation. The time dimension is along the first axis - i.e.,
        `m[:, i, j]` is the time series of the magnetisation at the grid
        point (i, j).
        """
        filename = os.path.join(self.data_dir, 'm{}s.npy'.format(component))
        m = np.load(filename)
        assert m.ndim == 3
        return m

    def get_fft_frequencies(self, unit='Hz'):
        if unit == 'Hz':
            timestep_unit = 's'
        elif unit == 'GHz':
            timestep_unit = 'ns'
        else:
            raise ValueError("Invalid unit: '{}'. Allowed values: 's', 'ns'")

        n = self.get_num_timesteps()
        dt = self.get_dt(unit=timestep_unit)
        freqs = np.fft.rfftfreq(n, dt)
        # FIXME: We ignore the last element for now so that we can compare with the existing data.
        return freqs[:-1]

    def find_freq_index(self, f, unit='Hz', rtol=1e-5):
        """
        Return index `i` such that `data_reader.get_fft_frequencies()[i]` is
        as close as possible to the given frequency `f`.

        Raises an exception if the relative difference is above the given
        tolerance `rtol`.
        """
        freqs = self.get_fft_frequencies(unit=unit)
        df = freqs[1] - freqs[0]

        i = np.argmin(np.abs(freqs - f))

        if np.abs(freqs[i] - f) > rtol * df:
            raise Exception("Failed to find the index of given frequency!")

        return i

    def get_FFT_coeffs_of_average_m(self, component):
        m_vals = self.get_average_magnetisation(component)
        fft_coeffs = np.fft.rfft(m_vals, axis=0)
        return fft_coeffs

    def get_FFT_coeffs_of_spatially_resolved_m(self, component):
        m_vals = self.get_spatially_resolved_magnetisation(component)
        fft_coeffs = np.fft.rfft(m_vals, axis=0)
        return fft_coeffs

    def get_FFT_coeffs_for_frequency(self, freq, component):
        fft_coeffs = self.get_FFT_coeffs_of_spatially_resolved_m(component)
        idx = self.find_freq_index(freq)
        return fft_coeffs[idx, :]

    def get_mode_amplitudes(self, freq, component):
        fft_coeffs_mode = self.get_FFT_coeffs_for_frequency(freq, component)
        return np.absolute(fft_coeffs_mode)

    def get_mode_phases(self, freq, component):
        fft_coeffs_mode = self.get_FFT_coeffs_for_frequency(freq, component)
        return np.angle(fft_coeffs_mode)

    def get_spectrum_via_method_1(self, component):
        """Compute power spectrum from spatially averaged magnetisation dynamics.

        The returned array contains the power spectral densities `S_y(f)` as
        defined in Eq. (1) of the paper.

        Parameters
        ----------
        data_avg :  1D numpy array

            Time series representing dynamics of a single component
            of the spatially averaged magnetisation (e.g. `m_y`).

        dt :  float

            Size of the timestep at which the magnetisation was sampled
            during the simulation (e.g. `dt=5e-12` for every 5 ps).

        Returns
        -------
        Pair of `numpy.array`s

            Frequencies and power spectral densities of the magnetisation
            data. Note that the frequencies are returned in GHz (not Hz).
        """
        fft_data_avg = self.get_FFT_coeffs_of_average_m(component)
        psd_data_avg = np.abs(fft_data_avg)**2
        # FIXME: We ignore the last element for now so that we can compare with the existing data.
        return psd_data_avg[:-1]

    def get_spectrum_via_method_2(self, component):
        r"""Compute power spectrum from spatially resolved magnetisation dynamics.

        The returned array contains the power spectral densities `\tilde{S}_y(f)`
        as defined in Eq. (5) of the paper.

        Parameters
        ----------
        data :  2D numpy array

            Time series representing dynamics of a single component
            of the spatially resolved magnetisation. It is assumed
            that time is along the first dimension, i.e. `data[k, j]`
            contains the magnetisation at timestep `t_k` for the
            grid point `r_j`.

        dt :  float

            Size of the timestep at which the magnetisation was sampled
            during the simulation (e.g. `dt=5e-12` for every 5 ps).

        Returns
        -------
        Pair of `numpy.array`s

            Frequencies and power spectral densities of the magnetisation
            data. Note that the frequencies are returned in GHz (not Hz).
        """
        fft_data_full = self.get_FFT_coeffs_of_spatially_resolved_m(component)
        psd_data_full = np.abs(fft_data_full)**2
        psd_data_avg = np.mean(psd_data_full, axis=(1, 2))
        # FIXME: We ignore the last element for now so that we can compare with the existing data.
        return psd_data_avg[:-1]
