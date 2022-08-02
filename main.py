import time

import cv2
import numpy as np

from model.board import Board


# GAME SETTING
BOARD_SIZE_W, BOARD_SIZE_H = BOARD_SIZE = (5, 5)

# SCREEN SETTING
BLOCK_SIZE_W, BLOCK_SIZE_H = BLOCK_SIZE = (80, 80)
PADDING_X, PADDING_Y = PADDING = (24, 24)
WINDOW_SIZE_W, WINDOW_SIZE_H = WINDOW_SIZE = (PADDING_X * 2 + BOARD_SIZE_W * BLOCK_SIZE_W, PADDING_Y * 2 + BOARD_SIZE_H * BLOCK_SIZE_H)

board = Board(WINDOW_SIZE, PADDING, BOARD_SIZE, BLOCK_SIZE)


def main():
    time_start = time.time()
    solution_paths = board.solve()
    time_end = time.time()
    print(f'Solved in {(time_end - time_start):.03f} s')

    i = 0
    while True:
        if i >= len(solution_paths):
            break

        # img = board.draw_board()
        img = board.draw_path(solution_paths[i])

        cv2.imshow('Flow Free', img)
        key = cv2.waitKey(0)
        if key == ord('q'):
            break

        i += 1

    pass


if __name__ == '__main__':
    main()

