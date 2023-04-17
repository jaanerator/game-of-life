import os
from datetime import datetime
import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import logging


"""
Conway's Game of Life

    This module is a program implements Conway's game of life.
    It shows an animated time-lapse, which is saved as a gif file immediately after execution.
    Unlike other programs, it contains additional rules as follows.
    
        1. Initial states are randomly extracted. Users can set probability which determines the state of each cell.
        2. There is a separate rule to stop the simulation.
            - TBA
    
    For further descriptions and rules of the game, visit:
        https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

TODO
    - title 실시간 변경
    - MovieWriter ffmpeg unavailable; using Pillow instead.
    - Process finished with exit code -1073741819 (0xC0000005)
    - 간헐적 응답없음 현상
    - 셧다운조건에 비율도 추가. 5%
    - potential plot 꾸미기
"""


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


def get_logger(use_stream=True, use_file=True, directory=None, level=None):
    formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(filename)s:%(lineno)s\t%(message)s')
    log_obj = logging.getLogger()
    if use_stream:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        log_obj.addHandler(stream_handler)
    if use_file:
        directory = directory if directory is not None else ''
        file_handler = logging.FileHandler(os.path.join(directory, datetime.now().strftime('%Y-%m-%d.log')))
        file_handler.setFormatter(formatter)
        log_obj.addHandler(file_handler)
    level = level if level is not None else logging.INFO
    log_obj.setLevel(level=level)
    return log_obj


def get_folder_name(base_dir):
    folder_name = datetime.now().strftime('simulated data %Y-%m-%d %H%M%S')
    folder_full_name = folder_name
    i = 0
    while folder_name in os.listdir('./outputs'):
        i += 1
        folder_full_name = folder_name + ' (%d)' % i
        if folder_full_name not in os.listdir(base_dir):
            break
    return folder_full_name


def make_grid(alives_list, nrow, ncol):
    grid = np.zeros((nrow, ncol))
    for alive_row, alive_col in alives_list:
        grid[alive_row][alive_col] = 1
    return grid


class GameOfLife:
    def __init__(self, nrow, ncol):
        self.nrow = nrow
        self.ncol = ncol
        self.alives = None
        return
    
    def set_initial(self, alives=None, num_alives=None):
        if alives is not None:
            self.alives = alives
        else:
            sampled_rows = np.random.choice(self.nrow, num_alives)
            sampled_cols = np.random.choice(self.ncol, num_alives)
            self.alives = list(zip(sampled_rows, sampled_cols))
        return
    
    def run(self):
        return

class GetNextAlives:
    def __init__(self, row_lim, col_lim):
        self.counter = {}
        self.row_lower, self.row_upper = row_lim
        self.col_lower, self.col_upper = col_lim
        return

    def get(self, alives_list):
        for alive in alives_list:
            self.cast_vote(alive)

        result = []
        for neighbor_key, counts in self.counter.items():
            neighbor = tuple([int(idx) for idx in neighbor_key.split('_')])
            if counts == 3 or (neighbor in alives_list and counts == 2):
                result.append(neighbor)
        return result

    def cast_vote(self, alive):
        row_idx, col_idx = alive
        row_search_min = max(row_idx - 1, self.row_lower)
        row_search_max = min(row_idx + 2, self.row_upper)
        col_search_min = max(col_idx - 1, self.col_lower)
        col_search_max = min(col_idx + 2, self.col_upper)
        for neighbor_row in range(row_search_min, row_search_max):
            for neighbor_col in range(col_search_min, col_search_max):
                if neighbor_row != row_idx or neighbor_col != col_idx:
                    neighbor_key = '%d_%d' % (neighbor_row, neighbor_col)
                    if neighbor_key in self.counter.keys():
                        self.counter[neighbor_key] += 1
                    else:
                        self.counter[neighbor_key] = 1
        return


if __name__ == '__main__':
    # Do not run this code
    exit()

    # pre-defined settings
    MAX_ITER = 1000
    SHUTDOWN_WAIT = 20
    FIGURE_SIZE = (6, 6)
    FPS = 30
    SAVE_MODE = True
    SAVE_DIR = 'output'
    LOG_DIR = 'log'
    DELETE_OLD_LOGS = False

    # set logger
    if DELETE_OLD_LOGS:
        for file in os.listdir(LOG_DIR):
            os.remove(os.path.join(LOG_DIR, file))
    logger = get_logger(use_stream=True, use_file=True, directory=LOG_DIR, level=logging.INFO)
    logger.info('START')

    # initial dataset
    logger.info('Sampling was successfully finished.')

    # main algorithm
    history = [alives[:]]
    before_grid = make_grid(alives, NROW, NCOL)
    potential = [np.inf]
    shutdown_count = 0
    for _ in trange(MAX_ITER - 1, desc='Simulation - '):
        # get next alives
        alives = GetNextAlives((0, NROW), (0, NCOL)).get(alives)
        history.append(alives[:])

        # make potential statistic
        now_grid = make_grid(alives, NROW, NCOL)
        potential.append((now_grid != before_grid).sum())
        before_grid = now_grid

        # shutdown rule
        if potential[-1] == potential[-2]:
            shutdown_count += 1
            if shutdown_count >= SHUTDOWN_WAIT:
                logger.info('Simulation was terminated earlier than scheduled by the shutdown rule.')
                break
    if shutdown_count < SHUTDOWN_WAIT:
        logger.info('Simulation was terminated as expected (FULL RUNNING)')

    # pop-up animation
    animator = Animator(history, NROW, NCOL, FPS, FIGURE_SIZE)
    try:
        animator.show()
        logger.info('Animation is closed safely.')
    except Exception as e:
        logger.error(f'Animation is closed with unexpected error: {e}')

    # save results
    if SAVE_MODE:
        folder_dir = os.path.join(SAVE_DIR, get_folder_name(SAVE_DIR))
        os.mkdir(folder_dir)

        # history
        history_file = open(os.path.join(folder_dir, 'history.txt'), 'w')
        for alives in history:
            history_file.write(str(alives) + '\n')
        history_file.close()

        # potential
        plt.plot(potential)
        plt.savefig(os.path.join(folder_dir, 'potential.png'))
        plt.close()

        # animation
        animator.save(os.path.join(folder_dir, 'animation.gif'))

        logger.info('Process finished WITH SAVE successfully.')
    else:
        logger.info('Process finished successfully.')
