import pygame
from gen_algo import *


########### What to show each generation

### four ways to show :
# 1) only the final position of all the elite
# 2) the path taken by the best one with arrows to make it clear
# 3) animation of the path taken by the best one
# 4) leaderboard with 10 elites on another window

# I implemented #2


def draw_maze(window, maze, square_size, maze_color):

    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 1:
                pygame.draw.rect(
                    window,
                    maze_color,
                    (j * square_size, i * square_size, square_size, square_size),
                )
    pygame.display.update()


def clear_maze(window, maze, square_size, back_ground_color):
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] != 1:
                pygame.draw.rect(
                    window,
                    back_ground_color,
                    (j * square_size, i * square_size, square_size, square_size),
                )
    pygame.display.update()


def show_path(window, game, sample, square_size, show_path_color):
    memo = game.play(sample, record=True)[2]
    for pos in memo:
        pygame.draw.rect(
            window,
            show_path_color,
            (pos[1] * square_size, pos[0] * square_size, square_size, square_size),
        )
    pygame.display.update()


def show_gen(gen, algo, game, time=None):
    print("--------------------------------------------")
    print("benchmark of generation", gen)
    if time is not None:
        print("time (s) :", time)
    print("best score :", algo.pop[0].score)
    print("Manhattan distance :", manh_dist(algo.pop[0].end_position, game.exit))
    print("--------------------------------------------")
