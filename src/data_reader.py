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

    def get_timesteps(self, unit='s'):
        """
        Return a 1D numpy array containing the timesteps at which
        the magnetisation was saved during the simulation.

        The argument `unit` can either be 's' (= seconds) or 'ns'
        (= nanoseconds).
        """
        # Timestamps are contained in the first column of the averaged data
        try:
            factor = {'s': 1.0, 'ns': 1e9}[unit]
        except KeyError:
            msg = ("The argument `unit` must be either 's' (= seconds) "
                   "or 'ns' (= nanoseconds). Got: '{}'".format(unit))
            raise ValueError(msg)

        return self.data_avg[:, 0] * factor

    def get_dt(self):
        """
        Return the size of the timestep used during the simulation.
        This is determined as the difference between the first and
        second timestep of the simulation run (all subsequent
        timesteps are ignored). In particular, it assumes that all
        timesteps used in the simulation are equal.
        """
        ts = self.get_timesteps()
        return ts[1] - ts[0]

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
        Return a 2D numpy array containing the values of the
        spatially resolved magnetization sampled at the time-
        steps during the simulation. The time dimension is
        along the first axis (i.e., `m[:, j]` is the time
        series of the magnetisation at the j-th grid point).
        """
        filename = os.path.join(self.data_dir, 'm{}s.npy'.format(component))
        return np.load(filename)
