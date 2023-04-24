import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Animator:
    def __init__(self, history_, nrow, ncol, fps, figure_size):
        self.history = history_
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
                                 self.update,
                                 frames=self.history,
                                 init_func=self.init_plot,
                                 interval=self.interval,
                                 repeat=False)
        plt.show()
        return

    def init_plot(self):
        return self.plot

    def update(self, frame):
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
