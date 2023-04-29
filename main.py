import os
from datetime import datetime
from collections import defaultdict

import matplotlib.pyplot as plt

from src.game_of_life import GameOfLife
from src.animator import GolAnimator


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
