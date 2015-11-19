import numpy as np
import os


class DataLoader(object):
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

    def get_timesteps(self):
        """
        Return a 1D numpy array containing the timesteps at which
        which the magnetisation was saved during the simulation.
        """
        # Timestamps are contained in the first column of the averaged data
        return self.data_avg[:, 0]

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
