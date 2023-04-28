import os
from datetime import datetime
from collections import defaultdict

import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt

from src.game_of_life import GameOfLife
from src.animator import GolAnimator


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
    - title 실시간 변경 (저장 파일에서는 잘 안됨.)
    - shutdown 조건 추가 (스케일이 너무 크면 potential 자체가 커져서 셧다운이 잘 안 됨.)
    - MovieWriter ffmpeg unavailable; using Pillow instead.
    - potential plot 꾸미기
    - axis-off
"""


if __name__ == '__main__':
    # Settings
    NROW = 30
    NCOL = 30
    MAX_ITERATION = 1000
    ALIVES = None
    NUM_ALIVES = 100
    SHUTDOWN_WAIT = 20
    FPS = 30
    FIGURE_SIZE = (6, 6)
    SAVE_MODE = True
    SAVE_DIR = 'output'

    # Run Algorithm
    gol = GameOfLife(NROW, NCOL)
    gol.run(MAX_ITERATION, alives=ALIVES, num_alives=NUM_ALIVES, shutdown_wait=SHUTDOWN_WAIT)

    # Make Animation
    animator = GolAnimator(gol.history, NROW, NCOL, FPS, FIGURE_SIZE)
    try:
        animator.show()
        print('Animation is closed safely.')
    except Exception as e:
        print(f'Animation is closed with unexpected error: {e}')

    # Save Results
    if SAVE_MODE:
        folder_dir = os.path.join(SAVE_DIR, datetime.now().strftime('%Y%m%d%H%M%S'))
        os.mkdir(folder_dir)

        # animation
        animator.save(os.path.join(folder_dir, 'animation.gif'))

        # potential
        plt.plot(gol.potential)
        plt.savefig(os.path.join(folder_dir, 'potential.png'))
        plt.close()

        print('Process is finished WITH SAVING successfully.')
    else:
        print('Process is finished successfully.')
