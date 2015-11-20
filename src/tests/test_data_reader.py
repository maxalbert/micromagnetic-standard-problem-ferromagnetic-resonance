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

    def test_get_dt(self):
        dt = self.data_reader.get_dt()
        assert dt == 5e-12

    def test_get_average_magnetisation(self):
        mys = self.data_reader.get_average_magnetisation(component='y')
        mzs = self.data_reader.get_average_magnetisation(component='z')

        mys_expected = [0, -0.1, -0.2, -0.3, -0.4, -0.5]
        mzs_expected = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]

        assert np.allclose(mys, mys_expected)
        assert np.allclose(mzs, mzs_expected)

    def test_get_spatially_resolved_magnetisation(self):
        mys = self.data_reader.get_spatially_resolved_magnetisation(component='y')
        mzs = self.data_reader.get_spatially_resolved_magnetisation(component='z')

        mys_expected = np.array([[ 0.   , -0.1  , -0.2  , -0.3  , -0.4  , -0.5  ],
                                 [ 0.372,  0.272,  0.172,  0.072, -0.028, -0.128]]).transpose()
        mzs_expected = np.array([[ 1.   ,  0.9  ,  0.8  ,  0.7  ,  0.6  ,  0.5  ],
                                 [ 0.554,  0.454,  0.354,  0.254,  0.154,  0.054]]).transpose()

        assert np.allclose(mys, mys_expected)
        assert np.allclose(mzs, mzs_expected)
