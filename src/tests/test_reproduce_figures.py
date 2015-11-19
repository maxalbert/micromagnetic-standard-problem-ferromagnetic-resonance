import sys; sys.path.insert(0, '..')
from matplotlib.testing.decorators import image_comparison
from postprocessing import make_figure2, make_figure3, make_figure4_and_5


@image_comparison(baseline_images=['figure2_OOMMF'], extensions=['png', 'pdf'])
def test_reproduce_figure_2():
    make_figure2("../../data/oommf/dynamic_txyz.txt", software='OOMMF')


@image_comparison(baseline_images=['figure3_OOMMF'], extensions=['png', 'pdf'])
def test_reproduce_figure_3():
    make_figure3("../../data/oommf/dynamic_txyz.txt", "../../data/oommf/mys_ft_abs.npy", software='OOMMF')


@image_comparison(baseline_images=['figure4_OOMMF', 'figure5_OOMMF'], extensions=['png', 'pdf'])
def test_reproduce_figure_4_and_5():
    make_figure4_and_5("../../data/oommf/dynamic_txyz.txt",
                       "../../data/oommf/mxs_ft_abs.npy",
                       "../../data/oommf/mys_ft_abs.npy",
                       "../../data/oommf/mzs_ft_abs.npy",
                       "../../data/oommf/mxs_ft_phase.npy",
                       "../../data/oommf/mys_ft_phase.npy",
                       "../../data/oommf/mzs_ft_phase.npy",
                       software='OOMMF')
