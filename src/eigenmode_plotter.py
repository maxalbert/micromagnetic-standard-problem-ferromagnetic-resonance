import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib import cm


class EigenmodePlotter(object):
    def __init__(self, data_reader, cmap_amplitude, cmap_phase):
        self.data_reader = data_reader
        self.cmap_amplitude = cmap_amplitude
        self.cmap_phase = cmap_phase
        self.shape = (24, 24)  # FIXME: this class should not need to know about this

    @staticmethod
    def plot_mode_component(fig, gs, data, label, vmin, vmax, cmap):
        ax = fig.add_subplot(gs)
        ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, origin='lower')
        ax.set_title(label)
        ax.set_xticks([])
        ax.set_yticks([])

    @staticmethod
    def plot_colorbar(fig, gs, label, cmap, vmin, vmax, num_ticks, ticklabels=None):
        ax = fig.add_subplot(gs)
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        ticks = np.linspace(vmin, vmax, num_ticks)
        cbar = mpl.colorbar.ColorbarBase(
                   ax, cmap, norm=norm, orientation='vertical', ticks=ticks)
        cbar.set_label(label)
        if ticklabels:
            cbar.ax.set_yticklabels(ticklabels)

    def plot_mode(self, freq):
        """
        Return matplotlib figure with six panels containing the amplitudes
        and phases.
        """
        fig = plt.figure(figsize=(8, 6))
        gs = gridspec.GridSpec(2, 4,
                          width_ratios=[4, 4, 4, 0.5], height_ratios=[4, 4])

        components = ['x', 'y', 'z']

        amp_x = self.data_reader.get_mode_amplitudes(freq, 'x').reshape(self.shape)
        amp_y = self.data_reader.get_mode_amplitudes(freq, 'y').reshape(self.shape)
        amp_z = self.data_reader.get_mode_amplitudes(freq, 'z').reshape(self.shape)

        phase_x = self.data_reader.get_mode_phases(freq, 'x').reshape(self.shape)
        phase_y = self.data_reader.get_mode_phases(freq, 'y').reshape(self.shape)
        phase_z = self.data_reader.get_mode_phases(freq, 'z').reshape(self.shape)

        # Ensure that all three amplitude plots are on the same scale:
        minVal = np.min([amp_x, amp_y, amp_z])
        maxVal = np.max([amp_x, amp_y, amp_z])

        self.plot_mode_component(fig, gs[0], amp_x, 'x', cmap=self.cmap_amplitude, vmin=minVal, vmax=maxVal)
        self.plot_mode_component(fig, gs[1], amp_y, 'y', cmap=self.cmap_amplitude, vmin=minVal, vmax=maxVal)
        self.plot_mode_component(fig, gs[2], amp_z, 'z', cmap=self.cmap_amplitude, vmin=minVal, vmax=maxVal)
        self.plot_colorbar(fig, gs[3], 'Amplitude', self.cmap_amplitude, vmin=0, vmax=maxVal, num_ticks=5)

        self.plot_mode_component(fig, gs[4], phase_x, 'x', cmap=self.cmap_phase, vmin=-np.pi, vmax=+np.pi)
        self.plot_mode_component(fig, gs[5], phase_y, 'y', cmap=self.cmap_phase, vmin=-np.pi, vmax=+np.pi)
        self.plot_mode_component(fig, gs[6], phase_z, 'z', cmap=self.cmap_phase, vmin=-np.pi, vmax=+np.pi)
        self.plot_colorbar(fig, gs[7], 'Phase', self.cmap_phase, vmin=-np.pi, vmax=np.pi, num_ticks=3, ticklabels=['-3.14', '0', '-3.14'])

        fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, wspace=0.1)
        fig.suptitle('{:.2f} GHz'.format(freq * 1e-9), fontsize=20)
        fig.tight_layout()

        return fig
