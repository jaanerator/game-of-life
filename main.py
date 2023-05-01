import os
import argparse
from datetime import datetime
from collections import defaultdict

import matplotlib.pyplot as plt

from src.game_of_life import GameOfLife
from src.animator import GolAnimator


def parse_argument():
    p = argparse.ArgumentParser(prog='game-of-life', add_help=True)
    p.add_argument('--nrow', type=int, default=30, required=False, metavar='', help='Height of gridworld')
    p.add_argument('--ncol', type=int, default=30, required=False, metavar='', help='Width of gridworld')
    p.add_argument('--max_iteration', type=int, default=1000, required=False, metavar='', help='Maximal number of steps')
    p.add_argument('--alives', type=parse_alives, default=None, required=False, metavar='', help='Coordinates of initial alives', nargs='+')
    p.add_argument('--num_alives', type=int, default=100, required=False, metavar='', help='The number of initial alives')
    p.add_argument('--shutdown_wait', type=int, default=20, required=False, metavar='', help='The number of steps to wait stopping rule')
    p.add_argument('--fps', type=int, default=30, required=False, metavar='', help='Frame-per-second option for animation')
    p.add_argument('--figure_size', type=int, default=6, required=False, metavar='', help='Size of animation')
    p.add_argument('--save_mode', action='store_true', help='Save the results')

    config = p.parse_args()
    return config


def parse_alives(s):
    try:
        row, col = map(int, s.split(','))
        return row, col
    except:
        raise argparse.ArgumentTypeError('Invalid format')


def main(config):
    # Run Algorithm
    gol = GameOfLife(nrow=config.nrow,
                     ncol=config.ncol)
    gol.run(max_iteration=config.max_iteration,
            alives=config.alives,
            num_alives=config.num_alives,
            shutdown_wait=config.shutdown_wait)

    # Make Animation
    animator = GolAnimator(history=gol.history,
                           nrow=config.nrow,
                           ncol=config.ncol,
                           fps=config.fps,
                           figure_size=(config.figure_size, config.figure_size))
    try:
        animator.show()
        print('Animation is closed safely.')
    except Exception as e:
        print(f'Animation is closed with unexpected error: {e}')

    # Save Results
    if config.save_mode:
        folder_dir = datetime.now().strftime('output/%Y%m%d%H%M%S')
        os.mkdir(folder_dir)

        # animation
        animator.save('{}/animation.gif'.format(folder_dir))

        # potential
        plt.plot(gol.potential)
        plt.savefig('{}/potential.png'.format(forder_dir))
        plt.close()

        print('Process is finished WITH SAVING successfully.')
    else:
        print('Process is finished successfully.')
    return


if __name__ == '__main__':
    config = parse_argument()
    main(config)
