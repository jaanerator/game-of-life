from collections import defaultdict

import numpy as np
from tqdm import trange

# import os
# from datetime import datetime
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation


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


if __name__ == '__main__':
    # pre-defined settings
    NROW = 100
    NCOL = 100
    MAX_ITERATION = 1000
    ALIVES = None
    NUM_ALIVES = 1000
    SHUTDOWN_WAIT = 20

    # FIGURE_SIZE = (6, 6)
    # FPS = 30
    # SAVE_MODE = True
    # SAVE_DIR = 'output'

    gol = GameOfLife(NROW, NCOL)
    gol.run(MAX_ITERATION, alives=ALIVES, num_alives=NUM_ALIVES, shutdown_wait=SHUTDOWN_WAIT)
    exit()

    # pop-up animation
    animator = Animator(history, NROW, NCOL, FPS, FIGURE_SIZE)
    try:
        animator.show()
        print('Animation is closed safely.')
    except Exception as e:
        print(f'Animation is closed with unexpected error: {e}')

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

        print('Process finished WITH SAVE successfully.')
    else:
        print('Process finished successfully.')
