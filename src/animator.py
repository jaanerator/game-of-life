import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class GolAnimator:

    """Game-Of-Life Animation-Maker

    Parameters
    ----------
    history : list
        A list of alives at each step
    nrow : int
        A height of the gridworld
    ncol : int
        A width of the gridworld
    fps : int
        Frame-per-second value of animation, by default 24
    figure_size : tuple(int)
        Figure size of animation and plot
    
    Attributes
    ----------
    show : None
        Show an animation
    save : None
        Save an animation
    """
    
    def __init__(self, history, nrow, ncol, fps=24, figure_size=(7, 7)):
        self.history = history
        self.nrow = nrow
        self.ncol = ncol
        self.interval = 1 / fps * 1000
        self.i = 0
        self.ani = None

        self.fig, _ = plt.subplots(figsize=figure_size)
        self.plot = plt.imshow(make_grid([(0, 0)], self.nrow, self.ncol), cmap='gray_r')
        self.plot.set_data([[]])
        return

    def show(self):
        self.ani = FuncAnimation(self.fig,
                                 self._update,
                                 frames=self.history,
                                 init_func=self._init_plot,
                                 interval=self.interval,
                                 repeat=False)
        plt.show()
        return

    def _init_plot(self):
        return self.plot

    def _update(self, frame):
        self.i += 1
        grid = make_grid(frame, self.nrow, self.ncol)
        self.plot.set_data(grid)
        plt.title(str(self.i))
        return self.plot

    def save(self, file_dir):
        assert self.ani is not None, 'Error : You must run show before saving.'
        self.ani.save(file_dir)
        return


def make_grid(alives_list, nrow, ncol):
    grid = np.zeros((nrow, ncol))
    for alive_row, alive_col in alives_list:
        grid[alive_row][alive_col] = 1
    return grid
