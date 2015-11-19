import sys; sys.path.insert(0, '..')
import numpy as np
from data_loader import DataLoader


class TestDataLoader(object):
    @classmethod
    def setup_class(cls):
        cls.data_loader = DataLoader('./sample_data/oommf', software='OOMMF')

    def test_get_timesteps(self):
        ts = self.data_loader.get_timesteps()
        ts_expected = [0, 5e-12, 1e-11, 1.5e-11, 2e-11, 2.5e-11]
        assert np.allclose(ts, ts_expected)
