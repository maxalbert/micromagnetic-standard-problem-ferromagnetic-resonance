import sys; sys.path.insert(0, '..')
import os
from matplotlib.testing.decorators import image_comparison
from postprocessing import make_figure2, make_figure3, make_figure4_and_5
from data_reader import DataReader

TOL = 0.  # we expect exact equality in the image comparison

here = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(here, '..', '..', 'data', 'oommf')

@image_comparison(baseline_images=['figure2_OOMMF'], extensions=['png', 'pdf'], tol=TOL)
def test_reproduce_figure_2():
    data_reader = DataReader(data_dir=data_dir, software='OOMMF')
    fig = make_figure2(data_reader)


@image_comparison(baseline_images=['figure3_OOMMF'], extensions=['png', 'pdf'], tol=TOL)
def test_reproduce_figure_3():
    data_reader = DataReader(data_dir=data_dir, software='OOMMF')
    make_figure3(data_reader)


@image_comparison(baseline_images=['figure4_OOMMF', 'figure5_OOMMF'], extensions=['png', 'pdf'], tol=TOL)
def test_reproduce_figure_4_and_5():
    data_reader = DataReader(data_dir=data_dir, software='OOMMF')
    make_figure4_and_5(data_reader, software='OOMMF')
