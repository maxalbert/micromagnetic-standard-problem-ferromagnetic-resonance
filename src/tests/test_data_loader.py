import sys; sys.path.insert(0, '..')
import numpy as np
from data_loader import DataLoader


class TestDataLoader(object):
    @classmethod
    def setup_class(cls):
        cls.data_loader = DataLoader('../../data/oommf', software='OOMMF')

    def test_get_timesteps(self):
        ts = self.data_loader.get_timesteps()
        ts_expected = np.linspace(0, 20e-9, 4000)
        assert np.allclose(ts, ts_expected)
