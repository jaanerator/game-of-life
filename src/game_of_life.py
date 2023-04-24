from collections import defaultdict

import numpy as np
from tqdm import trange


class GameOfLife:
    def __init__(self, nrow, ncol):
        self.nrow = nrow
        self.ncol = ncol
        self.history = []
        self.potential = []
        self._alives = None
        return
    
    def run(self, max_iteration, alives=None, num_alives=None, shutdown_wait=20):
        self._set_initial(alives, num_alives)
        self.history.append(self._alives[:])
        self.potential.append(float('inf'))
        shutdown_count = 0
        for _ in trange(max_iteration):
            self._step()
            self.history.append(self._alives[:])
            pot = self._get_potential(self.history[-1], self.history[-2])
            self.potential.append(pot)

            if self.potential[-1] == self.potential[-2]:
                shutdown_count += 1
                if shutdown_count >= shutdown_wait:
                    break
        if shutdown_count >= shutdown_wait:
            print('Early-stopped by the shutdown rule.')
        else:
            print('Successfully finished.')
        return
    
    def _set_initial(self, alives=None, num_alives=None):
        if alives is not None:
            self._alives = alives
        else:
            sampled_rows = np.random.choice(self.nrow, num_alives)
            sampled_cols = np.random.choice(self.ncol, num_alives)
            self._alives = list(zip(sampled_rows, sampled_cols))
        return
        
    def _step(self):
        counter = defaultdict(int)
        for alive in self._alives:
            row_idx, col_idx = alive
            row_search_min = max(row_idx - 1, 0)
            row_search_max = min(row_idx + 2, self.nrow)
            col_search_min = max(col_idx - 1, 0)
            col_search_max = min(col_idx + 2, self.ncol)
            for neighbor_row in range(row_search_min, row_search_max):
                for neighbor_col in range(col_search_min, col_search_max):
                    if neighbor_row != row_idx or neighbor_col != col_idx:
                        counter[(neighbor_row, neighbor_col)] += 1
        
        next_alives = []
        for neighbor, counts in counter.items():
            if counts == 3 or (neighbor in self._alives and counts == 2):
                next_alives.append(neighbor)
        self._alives = next_alives
        return
    
    @staticmethod
    def _get_potential(arr1, arr2):
        arr1_set = set(arr1)
        arr2_set = set(arr2)
        return len(arr1_set - arr2_set) + len(arr2_set - arr1_set)
