import numpy as np


def fft(mx, dt=5e-12):
    """ FFT of the data at dt """
    n = len(mx)
    freq = np.fft.fftfreq(n, dt)

    ft_mx = np.fft.fft(mx)

    ft_abs = np.abs(ft_mx)
    ft_phase = np.angle(ft_mx)

    return freq, ft_abs, ft_phase


def spatial_fft(dataname):
    """ Spatially averaged FFT as defined in Eqn. (5) """
    ft_abs = []
    ft_phase = []

    mys = np.load(dataname)
    m, n = mys.shape

    for i in range(n):
        f, ft_a, ft_p = fft(mys[:, i])
        ft_abs.append(ft_a)
        ft_phase.append(ft_p)

    np.save(dataname[:-4] + '_ft_abs.npy', np.array(ft_abs))
    np.save(dataname[:-4] + '_ft_phase.npy', np.array(ft_phase))


def transform_data():
    """ Helper function to spatially transform data for each direction"""
    for direction in ["x", "y", "z"]:
        source = 'm{}s.npy'.format(direction)
        targetA = 'm{}s_ft_abs.npy'.format(direction)
        targetB = 'm{}s_ft_phase.npy'.format(direction)

        if not os.path.isfile(source):
            raise IOError("Source file {} does not exist in the current "
                " directory. Try running the Makefile".format(source))
        if not os.path.isfile(targetA) or not os.path.isfile(targetB):
            spatial_fft(source)


if __name__ == '__main__':
    transform_data()