import sys; sys.path.insert(0, '..')
import numpy as np
from data_reader import DataReader


class TestDataReader(object):
    @classmethod
    def setup_class(cls):
        cls.data_reader = DataReader('./sample_data/oommf', software='OOMMF')

    def test_get_timesteps(self):
        ts = self.data_reader.get_timesteps()
        ts_expected = [0, 5e-12, 1e-11, 1.5e-11, 2e-11, 2.5e-11]
        assert np.allclose(ts, ts_expected)

    def test_get_average_magnetisation(self):
        mys = self.data_reader.get_average_magnetisation(component='y')
        mzs = self.data_reader.get_average_magnetisation(component='z')

        mys_expected = [0, -0.1, -0.2, -0.3, -0.4, -0.5]
        mzs_expected = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]

        np.allclose(mys, mys_expected)
        np.allclose(mzs, mzs_expected)
