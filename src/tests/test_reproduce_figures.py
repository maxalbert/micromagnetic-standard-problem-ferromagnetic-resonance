import sys; sys.path.insert(0, '..')
from matplotlib.testing.decorators import image_comparison
from postprocessing import make_figure2, make_figure3, make_figure4_and_5
from data_reader import DataReader

TOL = 0.  # we expect exact equality in the image comparison


@image_comparison(baseline_images=['figure2_OOMMF'], extensions=['png', 'pdf'], tol=TOL)
def test_reproduce_figure_2():
    data_reader = DataReader(data_dir="../../data/oommf/", software='OOMMF')
    make_figure2(data_reader)


@image_comparison(baseline_images=['figure3_OOMMF'], extensions=['png', 'pdf'], tol=TOL)
def test_reproduce_figure_3():
    data_reader = DataReader(data_dir="../../data/oommf/", software='OOMMF')
    make_figure3(data_reader)


@image_comparison(baseline_images=['figure4_OOMMF', 'figure5_OOMMF'], extensions=['png', 'pdf'], tol=TOL)
def test_reproduce_figure_4_and_5():
    data_reader = DataReader(data_dir="../../data/oommf/", software='OOMMF')
    make_figure4_and_5(data_reader,
                       "../../data/oommf/dynamic_txyz.txt",
                       "../../data/oommf/mxs_ft_abs.npy",
                       "../../data/oommf/mys_ft_abs.npy",
                       "../../data/oommf/mzs_ft_abs.npy",
                       "../../data/oommf/mxs_ft_phase.npy",
                       "../../data/oommf/mys_ft_phase.npy",
                       "../../data/oommf/mzs_ft_phase.npy",
                       software='OOMMF')
