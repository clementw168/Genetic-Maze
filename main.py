import pygame
from pygame.locals import *
from gen_algo import *
from graph import *
import time

###### Parameters

#### Graphism
window_length = 640
window_width = 480
maze_color = (255, 0, 0)
backgroud_color = (255, 255, 255)
entrance_color = (0, 255, 0)
exit_color = (0, 0, 255)

show_path_color = (160, 225, 55)

#### Back
shape = (10, 10)
holes = 5
number_of_generations = 1000
pop_card = 3000
elite = 0.01
mortality = 0.4
mutation_rate = 0.4
max_moves = 100


################### Inititialisation of pygame
pygame.init()


# Init game
t0 = time.time()

game = Game(shape=shape, holes=holes)
algo = GA(
    game,
    genome_length=max_moves,
    pop_card=pop_card,
    elite=elite,
    mortality=mortality,
    mutation_rate=mutation_rate,
)
square_size = min(
    window_length // game.maze.shape[1], window_width // game.maze.shape[0]
)

window = pygame.display.set_mode(
    (square_size * game.maze.shape[1], square_size * game.maze.shape[0])
)

window.fill(backgroud_color)


draw_maze(window, game.maze, square_size, maze_color)
game.print_maze()


print("Initialisation took ", time.time() - t0)
t0 = time.time()


show_gen(0, algo, game)
show_path(window, game, algo.pop[0], square_size, show_path_color)

for gen in range(1, number_of_generations):
    print("starting generation", gen)
    algo.do_gen()
    clear_maze(window, game.maze, square_size, backgroud_color)
    show_path(window, game, algo.pop[0], square_size, show_path_color)
    show_gen(gen, algo, game, time=time.time() - t0)
    t0 = time.time()


flag = 1
while flag:
    for event in pygame.event.pump():
        if event.type == QUIT:
            flag = 0
