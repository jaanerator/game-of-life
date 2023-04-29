# game-of-life

This module is a program that implements John Conway's *Game of Life*, under Python 3 environment.

## 1. What is *Game of Life*?<sup>[1](#footnote_1)</sup>

![](./docs/sources/Gospers_glider_gun.gif)

The *Game of Life* is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves.

### 1-1) Rule

The *Game of Life* starts at two-dimensional GridWorld. Each cell is in one of two possible states, live or dead. Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

## 2. Features

1. **Provision of preset values** : This module provides pre-defined settings such as maximal number of iterations, coordinates of initial alives, fps for animation, etc. See [here] for detailed.
2. **Automatic Stop Rule** : This module gets **potential** at each step to determine whether to end the simulation. See [here] for detailed.
3. **Animation** : This module shows animation in forms of gif.

## 3. Installation

```
git clone https://github.com/jaanerator/game-of-life.git
cd game-of-life
python install .
```

## 4. Usage

Run a CLI-based execution code, main.py.

<!--
```
python main.py --p_straight=1.0 --p_wall=0.5 --n_range 2 4 --n_boxes=1 --annealing_steps=80000 --nb_steps=100000
```

Belows are total arguments can be customized.

#### Required

* ```--p_straight=1.0``` : Samplers argument (Box's straight probability in random walk)

#### Optional

* ```--scope 5 5``` : Grid range near player to be used as input image
-->

## 5. License

Comply with MIT licenses and check the LICENSE file for details.

<!--
TODO
    - title 실시간 변경 (저장 파일에서는 잘 안됨.)
    - shutdown 조건 추가 (스케일이 너무 크면 potential 자체가 커져서 셧다운이 잘 안 됨.)
    - MovieWriter ffmpeg unavailable; using Pillow instead.
    - potential plot 꾸미기
    - axis-off
-->

---

<a name="footnote_1">1</a>: Source from Wikipedia, https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
