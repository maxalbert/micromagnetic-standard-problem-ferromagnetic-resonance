import sys; sys.path.insert(0, '..')

import numpy as np
import os
from data_reader import DataReader

here = os.path.abspath(os.path.dirname(__file__))


class TestCompareData(object):
    @classmethod
    def setup_class(cls):
        data_dir_ref = os.path.join(here, '..', '..', 'data', 'oommf')
        data_dir_comp = os.path.join(here, '..', '..', 'data-generated', 'oommf')
        cls.d1 = DataReader(data_dir=data_dir_ref, software='OOMMF')
        cls.d2 = DataReader(data_dir=data_dir_comp, software='OOMMF')

    def test_compare_average_magnetisation(self):
        for component in ['x', 'y', 'z']:
            m1_avg = self.d1.get_average_magnetisation(component)
            m2_avg = self.d2.get_average_magnetisation(component)
            diff = abs(m1_avg - m2_avg)
            print("Diff norm: {}, m1_avg norm: {}, m2_avg norm: {}".format(
                  np.linalg.norm(diff),
                  np.linalg.norm(m1_avg),
                  np.linalg.norm(m2_avg)))
            assert np.allclose(m1_avg, m2_avg, atol=1e-7, rtol=0)


    def test_compare_spatially_resolved_magnetisation(self):
        for component in ['x', 'y', 'z']:
            m1_full = self.d1.get_average_magnetisation(component)
            m2_full = self.d2.get_average_magnetisation(component)
            diff = abs(m1_full - m2_full)
            print("Diff norm: {}, m1_full norm: {}, m2_full norm: {}".format(
                  np.linalg.norm(diff),
                  np.linalg.norm(m1_full),
                  np.linalg.norm(m2_full)))
            assert np.allclose(m1_full, m2_full, atol=1e-4, rtol=0)
