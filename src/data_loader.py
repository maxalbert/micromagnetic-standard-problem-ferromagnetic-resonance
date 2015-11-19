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

    def get_timesteps(self):
        """
        Return a 1D numpy array containing the timesteps at which
        which the magnetisation was saved during the simulation.
        """
        filename = os.path.join(self.data_dir, 'dynamic_txyz.txt')
        data_avg = np.loadtxt(filename)
        ts = data_avg[:, 0]
        return ts
