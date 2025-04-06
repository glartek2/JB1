import sys
from collections import deque
from enum import Enum


class Direction(Enum):
    P = (0, 1)
    G = (-1, 0)
    L = (0, -1)
    D = (1, 0)


def move(board, occupied, x, y, direction):
    dx, dy = direction.value
    path = ""
    collected = 0

    while True:
        nx, ny = x + dx, y + dy
        if board[nx][ny] == '#' or (nx, ny) in occupied:
            break
        if board[nx][ny] == '*':
            collected += 1

        occupied.add((nx, ny))
        path += direction.name
        x, y = nx, ny

    return x, y, collected, path, occupied


def solve(board, S, start_x, start_y):
    queue = deque([(start_x, start_y, 0, "", {(start_x, start_y)})])
    visited = set()

    while queue:
        x, y, eaten, path, occupied = queue.popleft()

        if eaten >= S:
            return path

        state = (x, y, eaten, tuple(sorted(occupied)))
        if state in visited:
            continue
        visited.add(state)

        for direction in Direction:
            nx, ny, new_eaten, new_path, new_occupied = move(board, occupied.copy(), x, y, direction)
            queue.append((nx, ny, eaten + new_eaten, path + new_path, new_occupied))

    return None


def main():
    W, H, S = map(int, sys.stdin.readline().split())
    board = [list(sys.stdin.readline().strip()) for _ in range(H)]

    start_x = start_y = -1
    for i in range(H):
        for j in range(W):
            if board[i][j] == 'O':
                start_x, start_y = i, j
                break
        if start_x != -1:
            break

    result = solve(board, S, start_x, start_y)
    print(result)


if __name__ == "__main__":
    main()