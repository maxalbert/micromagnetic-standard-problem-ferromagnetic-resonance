import sys; sys.path.insert(0, '..')
import numpy as np
import os
from data_reader import DataReader

here = os.path.abspath(os.path.dirname(__file__))

class TestDataReader(object):
    @classmethod
    def setup_class(cls):
        datafile = os.path.join(here, 'sample_data', 'oommf')
        cls.data_reader = DataReader(datafile, software='OOMMF')

    def test_get_timesteps(self):
        ts = self.data_reader.get_timesteps()
        ts_expected = [0, 5e-12, 1e-11, 1.5e-11, 2e-11, 2.5e-11]

        ts_ns = self.data_reader.get_timesteps(unit='ns')
        ts_ns_expected = [0, 0.005, 0.01, 0.015, 0.02, 0.025]
        assert np.allclose(ts, ts_expected)
        assert np.allclose(ts_ns, ts_ns_expected)

    def test_get_num_timesteps(self):
        n = self.data_reader.get_num_timesteps()
        assert n == 6

    def test_get_dt(self):
        dt = self.data_reader.get_dt()
        dt_ns = self.data_reader.get_dt(unit='ns')
        assert dt == 5e-12
        assert dt_ns == 0.005

    def test_get_average_magnetisation(self):
        mys = self.data_reader.get_average_magnetisation(component='y')
        mzs = self.data_reader.get_average_magnetisation(component='z')

        mys_expected = [0, -0.1, -0.2, -0.3, -0.4, -0.5]
        mzs_expected = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]

        assert np.allclose(mys, mys_expected)
        assert np.allclose(mzs, mzs_expected)

    def test_get_spatially_resolved_magnetisation(self):
        mxs = self.data_reader.get_spatially_resolved_magnetisation(component='x')
        mys = self.data_reader.get_spatially_resolved_magnetisation(component='y')
        mzs = self.data_reader.get_spatially_resolved_magnetisation(component='z')

        mxs_expected = np.array([[ 0.   , +0.1  , +0.2  , +0.3  , +0.4  , +0.5  ],
                                 [ 0.372,  0.472,  0.572,  0.672,  0.772,  0.872]]).transpose()
        mys_expected = np.array([[ 0.   , -0.1  , -0.2  , -0.3  , -0.4  , -0.5  ],
                                 [ 0.372,  0.272,  0.172,  0.072, -0.028, -0.128]]).transpose()
        mzs_expected = np.array([[ 1.   ,  0.9  ,  0.8  ,  0.7  ,  0.6  ,  0.5  ],
                                 [ 0.554,  0.454,  0.354,  0.254,  0.154,  0.054]]).transpose()

        assert np.allclose(mxs, mxs_expected)
        assert np.allclose(mys, mys_expected)
        assert np.allclose(mzs, mzs_expected)

    def test_get_fft_frequencies(self):
        dt = self.data_reader.get_dt()
        n= self.data_reader.get_num_timesteps()
        freqs_Hz = self.data_reader.get_fft_frequencies(unit='Hz')
        freqs_GHz = self.data_reader.get_fft_frequencies(unit='GHz')
        freqs_Hz_expected = np.arange(n//2 + 1) / (n*dt)
        freqs_GHz_expected = freqs_Hz_expected / 1e9
        assert np.allclose(freqs_Hz, freqs_Hz_expected[:-1])
        assert np.allclose(freqs_GHz, freqs_GHz_expected[:-1])
