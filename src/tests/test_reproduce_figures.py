import sys; sys.path.insert(0, '..')
from matplotlib.testing.decorators import image_comparison
from postprocessing import figure2


@image_comparison(baseline_images=['figure2_OOMMF'], extensions=['png', 'pdf'])
def test_reproduce_figure_2():
    figure2("../../data/oommf/dynamic_txyz.txt", software='OOMMF')
