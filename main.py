"""
Conway's Game Of Life in Python with animation.
Initially taken from: https://www.geeksforgeeks.org/conways-game-life-python-implementation/
Modernized to reduce CPU usage while computing Moore neighborhood
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 1


def add_glider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, ON],
                       [ON, 0, ON],
                       [0, ON, ON]])
    grid[i:i + 3, j:j + 3] = glider


def add_gosper_glider_gun(i, j, grid):
    """adds a Gosper Glider Gun with top left
       cell at (i, j)"""
    gun = np.zeros(11 * 38).reshape(11, 38)

    gun[5][1] = gun[5][2] = ON
    gun[6][1] = gun[6][2] = ON

    gun[3][13] = gun[3][14] = ON
    gun[4][12] = gun[4][16] = ON
    gun[5][11] = gun[5][17] = ON
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = ON
    gun[7][11] = gun[7][17] = ON
    gun[8][12] = gun[8][16] = ON
    gun[9][13] = gun[9][14] = ON

    gun[1][25] = ON
    gun[2][23] = gun[2][25] = ON
    gun[3][21] = gun[3][22] = ON
    gun[4][21] = gun[4][22] = ON
    gun[5][21] = gun[5][22] = ON
    gun[6][23] = gun[6][25] = ON
    gun[7][25] = ON

    gun[3][35] = gun[3][36] = ON
    gun[4][35] = gun[4][36] = ON

    grid[i:i + 11, j:j + 38] = gun


def step(frameNum, img, board):
    board2 = board.copy()

    moore_sum = np.roll(board, (-1, -1), (0, 1)) + \
                np.roll(board, (-1, 0), (0, 1)) + \
                np.roll(board, (-1, 1), (0, 1)) + \
                np.roll(board, (0, -1), (0, 1)) + \
                np.roll(board, (0, 1), (0, 1)) + \
                np.roll(board, (1, -1), (0, 1)) + \
                np.roll(board, (1, 0), (0, 1)) + \
                np.roll(board, (1, 1), (0, 1))

    to_kill = (board > 0) & ((moore_sum < 2) | (moore_sum > 3))
    to_resurrect = (board == 0) & (moore_sum == 3)
    board2[to_kill] = 0
    board2[to_resurrect] = ON

    board[:] = board2
    img.set_data(board2)
    return img,


size = 150
update_interval = 50
board = np.zeros((size, size))

add_gosper_glider_gun(50, 50, board)

fig, ax = plt.subplots()
img = ax.imshow(board)

ani = animation.FuncAnimation(fig, step, fargs=(img, board),
                              frames=10,
                              interval=update_interval)

plt.show()
