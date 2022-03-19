# Genetic labyrinth

This project solves a maze game without seeing the maze but knowing the distance to the exit. A genetic algorithm is used to solve it.

![An illustration of the game](https://github.com/clementw168/Genetic-Maze/blob/main/illustration.png)

## Why genetic algorithm ? 

Solving a maze is easy using known algorithms such as depth first search or A*. However, I wanted to see if I could do it with a genetic algorithm. To get it harder, I wanted to see if I could solve it with a genetic algorithm without knowing where the walls are. 

## Motivations

I did that project just to remind me what a genetic algorithm is and have a clean implementation. The implementation is reusable for any project that needs a genetic algorithm. Here is the French description of the project [there](https://github.com/clementw168/Genetic-Maze/blob/main/fiche_laby.pdf).

## Generating the maze 

I used a [recursive algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_division_method) to generate the maze. 

