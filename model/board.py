import cv2
import numpy as np

import itertools
from itertools import combinations


class Board:

    IDS = [None, 'red', 'green', 'blue', 'yellow', 'orange']
    VALUES = {
        'red': 1,
        'green': 2,
        'blue': 3,
        'yellow': 4,
        'orange': 5,
    }
    COLORS = [
        (0, 0, 0),
        (0, 21, 255),  # RED
        (0, 149, 24),  # GREEN
        (230, 58, 35),  # BLUE
        (0, 224, 236),  # YELLOW
        (0, 145, 251),  # ORANGE
    ]
    # COLORS = {
    #     'red': (0, 21, 255),  # RED
    #     'green': (0, 149, 24),  # GREEN
    #     'blue': (230, 58, 35),  # BLUE
    #     'yellow': (0, 224, 236),  # YELLOW
    #     'orange': (0, 145, 251),  # ORANGE
    # }

    def __init__(self, window_size, padding, board_size, block_size):
        self.window_w, self.window_h = window_size
        self.padding_w, self.padding_h = padding
        self.board_w, self.board_h = board_size
        self.block_w, self.block_h = block_size

        self.background = self.create_background()
        self.value = self.create_board()
        self.paths = self.create_paths()
        self.shape = self.value.shape

    def create_board(self):
        value = np.zeros((self.board_h, self.board_w), dtype=np.uint8)

        value[0][0] = self.VALUES['red']
        value[4][1] = self.VALUES['red']

        value[0][2] = self.VALUES['green']
        value[3][1] = self.VALUES['green']

        value[1][2] = self.VALUES['blue']
        value[4][2] = self.VALUES['blue']

        value[0][4] = self.VALUES['yellow']
        value[3][3] = self.VALUES['yellow']

        value[1][4] = self.VALUES['orange']
        value[4][3] = self.VALUES['orange']

        return value

    def create_paths(self):
        # 'red': 1,
        # 'green': 2,
        # 'blue': 3,
        # 'yellow': 4,
        # 'orange': 5,
        return [
            [],
            [],
            [],
            # [(2, 4), (2, 3), (2, 2), (2, 1)],
            [],
            [],
            [],
        ]

    def create_background(self):
        img = np.zeros((self.window_h, self.window_w, 3), dtype=np.uint8)

        x1, y1 = self.padding_w, self.padding_h
        x2, y2 = self.window_w - self.padding_w, self.window_h - self.padding_h

        # img = cv2.rectangle(img, (x1, y1), (x2, y2), (145, 249, 130), -1)
        img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), -1)

        for x in range(self.padding_w, self.window_w , self.block_w):
            img = cv2.line(img, (x, y1), (x, y2), (255, 255, 255), 1, cv2.LINE_AA)

        for y in range(self.padding_h, self.window_h, self.block_h):
            img = cv2.line(img, (x1, y), (x2, y), (255, 255, 255), 1, cv2.LINE_AA)

        return img

    def draw_dots(self, img):
        return img

    def draw_board(self):
        img = self.background.copy()

        # Draw the dots
        for x in range(self.board_w):
            for y in range(self.board_h):
                val = self.value[y][x]
                if val != 0:
                    xc = self.padding_w + x * self.block_w + self.block_w // 2
                    yc = self.padding_h + y * self.block_h + self.block_h // 2
                    img = cv2.circle(img, (xc, yc), 30, self.COLORS[val], -1)

        return img

    def draw_path(self, paths):
        img = self.draw_board()

        # Draw the paths
        for id, path in enumerate(paths):
            if id != 0:
                for i in range(len(path) - 1):
                    x0, y0 = path[i + 0]
                    x1, y1 = path[i + 1]
                    x0, y0 = self.padding_w + x0 * self.block_w + self.block_w // 2, self.padding_h + y0 * self.block_h + self.block_h // 2
                    x1, y1 = self.padding_w + x1 * self.block_w + self.block_w // 2, self.padding_h + y1 * self.block_h + self.block_h // 2
                    img = cv2.line(img, (x0, y0), (x1, y1), self.COLORS[id], 25, cv2.LINE_AA)
        return img

    def draw_path_id(self, path, id):
        img = self.draw_board()

        # Draw the paths
        for i, position in enumerate(path[:-1]):
            x0, y0 = path[i + 0]
            x1, y1 = path[i + 1]
            x0, y0 = self.padding_w + x0 * self.block_w + self.block_w // 2, self.padding_h + y0 * self.block_h + self.block_h // 2
            x1, y1 = self.padding_w + x1 * self.block_w + self.block_w // 2, self.padding_h + y1 * self.block_h + self.block_h // 2
            img = cv2.line(img, (x0, y0), (x1, y1), self.COLORS[id], 25, cv2.LINE_AA)

        return img

    def find_position(self, id):
        positions = []
        for y in range(self.board_h):
            for x in range(self.board_w):
                if self.value[y][x] == id:
                    positions.append((x, y))
        return positions

    def solve(self):
        solution_paths = []
        for id in range(len(self.COLORS)):
            if id == 0:
                continue
            self.find_possible_path(id)
            # print(f'Final path {id}: {self.paths[id]}')

        # Do a combination
        # print(f'Possible paths:')
        # for id, color in enumerate(self.paths):
            # print(f'\t{id}: {self.paths[id]}')

        combination_paths = list(itertools.product(
            self.paths[1], self.paths[2],
            self.paths[3], self.paths[4], self.paths[5],
        ))
        print(f'Found {len(combination_paths)} total combinations')

        for i, colors in enumerate(combination_paths):
            value = np.zeros((self.board_h, self.board_w), dtype=np.uint8)
            for id, color in enumerate(colors):
                for x, y in color:
                    value[y][x] += 1

            if np.sum(value) == self.board_h * self.board_w:
                path = list(colors)
                path.insert(0, [])
                solution_paths.append(path)
                print(f'Solution #{len(solution_paths)}: {path}')

        print(f'Found {len(solution_paths)} total solution(s)')
        return solution_paths

    def find_possible_path(self, id):
        positions = self.find_position(id)
        if len(positions) == 2:
            x, y = positions[0]
            self.search_paths(id, (x, y), [(x, y)])
            # print(f'ID: {id} at {(x, y)}: {self.paths[id]}')

    def search_paths(self, id, position, path_search, prefix=''):
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            x, y = position[0] + dx, position[1] + dy
            # print(f'{prefix}{position} -> {(x, y)}')

            # Check if inside the board
            if (0 <= x < self.board_w) and (0 <= y < self.board_h):
                # Check if collision with the current path
                if (x, y) in path_search:
                    # print(f'{prefix}\tCollision')
                    continue

                # Check if other dots
                player = self.value[y][x]
                if player != id and player != 0:
                    # print(f'{prefix}\tOther')
                    continue

                # Check if connected
                if player == id:
                    p = path_search.copy()
                    p.append((x, y))
                    # print(f'{prefix}\tConnected')
                    # print(f'{prefix}\tPath: {p}')
                    self.paths[id].append(p)

                else:
                    # Search
                    p = path_search.copy()
                    p.append((x, y))
                    # print(f'{prefix}\tSearch')
                    self.search_paths(id, (x, y), p, prefix=f'{prefix}\t')

            else:
                # print(f'{prefix}\tOutside the board')
                pass
