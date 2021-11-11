import numpy as np
import random


def manh_dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Game(object):
    # nothing : 0
    # wall : 1
    # entrance : 2
    # exit : 3

    def __init__(self, shape=(3, 7), holes=0):

        self.dist_factor = 5
        self.exploration_factor = 6

        self.wall_penality = 2
        self.entrance_penality = 50
        self.exit_reward = 100

        self.entrance = (1 + 2 * random.randint(0, shape[0] - 1), 0)
        self.exit = (1 + 2 * random.randint(0, shape[0] - 1), shape[1] * 2)

        self.maze = np.zeros((shape[0] * 2 + 1, shape[1] * 2 + 1))

        # recursive generation with queue

        # delimitations :

        self.maze[0] = 1
        self.maze[-1] = 1
        self.maze[:, 0] = 1
        self.maze[:, -1] = 1

        # generation :

        def recursive_maze(maze):
            if maze.shape[0] <= 1 and maze.shape[1] <= 1:
                return []

            if maze.shape[0] < maze.shape[1]:
                verti = (
                    2 * random.randint(0, maze.shape[1] // 2 - 1) + 1
                )  # odd between 0 and shape[1]-1
                hori = 2 * random.randint(0, maze.shape[0] // 2)

                maze[:, verti] = 1
                maze[hori, verti] = 0

                return [maze[:, :verti], maze[:, verti + 1 :]]
            else:
                hori = 2 * random.randint(0, maze.shape[0] // 2 - 1) + 1
                verti = 2 * random.randint(0, maze.shape[1] // 2)
                maze[hori] = 1
                maze[hori, verti] = 0
                return [maze[:hori, :], maze[hori + 1 :, :]]

        queue = [self.maze[1:-1, 1:-1]]
        while len(queue) != 0:
            sub = queue.pop(0)
            temp = recursive_maze(sub)
            for i in temp:
                queue.append(i)

        for _ in range(holes):
            if random.random() < 0.5:
                verti = 2 * random.randint(
                    1, self.maze.shape[1] // 2 - 1
                )  # odd between 0 and shape[1]-1
                hori = 2 * random.randint(0, self.maze.shape[0] // 2 - 1) + 1
            else:
                hori = 2 * random.randint(1, self.maze.shape[0] // 2 - 1)
                verti = 2 * random.randint(0, self.maze.shape[1] // 2 - 1) + 1

            if self.maze[hori, verti] == 1:
                self.maze[hori, verti] = 0

        self.maze[self.entrance] = 2
        self.maze[self.exit] = 3

    def play(self, player, record=False):
        """
        argument :
            - player, a Sample class object
        return :
            - list with score and end position
        """
        position = self.entrance
        score = 0

        memo = [position]
        for i in player.genome:

            if i == 0:
                temp = (position[0], position[1] + 1)
            if i == 1:
                temp = (position[0] + 1, position[1])
            if i == 2:
                temp = (position[0], position[1] - 1)
            if i == 3:
                temp = (position[0] - 1, position[1])
            if i == 4:
                temp = (position[0], position[1])

            if temp[1] >= 0 and temp[1] < self.maze.shape[1]:
                # this can occur at the entrance and at the exit
                if self.maze[temp] == 1:
                    score -= self.wall_penality
                if self.maze[temp] == 0:
                    position = temp
                if self.maze[temp] == 2:
                    position = temp
                    score -= self.entrance_penality
                if self.maze[temp] == 3:
                    # this makes it go for exit faster and staying there
                    score += self.exit_reward
                    position = temp

                memo.append(position)
            else:
                score -= self.wall_penality

        ### push the exploration :
        score += self.exploration_factor * len(set(memo))

        ### push the way toward the exit :
        score -= self.dist_factor * manh_dist(position, self.exit)
        if record:
            return score, position, memo
        return score, position

    @property
    def entrance(self):
        return self._entrance

    @entrance.setter
    def entrance(self, new):
        self._entrance = new

    @property
    def exit(self):
        return self._exit

    @exit.setter
    def exit(self, new):
        self._exit = new

    @property
    def maze(self):
        return self._maze

    @maze.setter
    def maze(self, new):
        self._maze = new

    def print_maze(self):
        print(self.maze)


class Sample(object):
    """
    genome : list of integers between 0 and 4
    0 : up
    1 : right
    2 : down
    3 : left
    4 : stay still -> this is usefull to lessen the number
                    of moves without changing the length of the list

    Some tweaks were done to adapt to the particular genome
    """

    def __init__(
        self, creation="random", max_length=30, genome=[], parent1=None, parent2=None,
    ):
        """
        creation = "random" : random, be carefull to set the length
                    "cross over" : do a cross over between 2 samples
                                    be carefull to set parent1 and parent2
        """
        self.score = None
        self.end_position = None
        if creation == "random":
            self.genome = [random.randint(0, 4) for l in range(max_length)]
        elif creation == "genome":
            self.genome = genome
        elif creation == "cross over":
            if parent1 is None or parent2 is None:
                raise NameError("Parents are not defined")
            # we want to keep the beginning of the best parent
            if parent1.score > parent2.score:
                begin = parent1
                end = parent2
            else:
                begin = parent2
                end = parent1
            cross_point = random.randint(0, len(parent1.genome))
            self.genome = begin.genome[:cross_point] + end.genome[cross_point:]

        else:
            raise NameError("Mode of creation not defined")

    def mutate(self):
        """
        That mutation tries to favour straight lines to get out of local minimum
        """
        x1 = random.randint(0, len(self.genome))
        x2 = random.randint(0, (len(self.genome) - x1))

        for k in range(x1, x1 + x2):
            temp = random.randint(0, 6)
            if temp < 5:
                self.genome[k] = temp
            else:
                if k > 0:
                    self.genome[k] = self.genome[k - 1]

    @property
    def genome(self):
        return self._genome

    @genome.setter
    def genome(self, new):
        self._genome = new

    @property
    def score(self):
        if self._score is None:
            raise NameError("Score is None")
        return self._score

    @score.setter
    def score(self, new):
        self._score = new

    @property
    def end_position(self):
        if self._end_position is None:
            raise NameError("End position is None")
        return self._end_position

    @end_position.setter
    def end_position(self, new):
        self._end_position = new


class GA(object):
    """
    Attributes :
    pop_card : cardinal of population
    pop : list of people which compose the population
    elite_card : cardinal of the elite
                    the elite corresponds to pop[:elite_card]
    death_card : cardinal of the deaths in each generation
                they correspond to pop[mortality_card:]
    mutation_rate
    max_length

    This class tries to be as general as it can to solve a game
    The only thing you have to change in it is the maxlength parameter
    it is only used during the initialisation

    """

    def __init__(
        self,
        game,
        genome_length=None,
        pop_card=5000,
        elite=0.01,
        mortality=0.4,
        mutation_rate=0.2,
    ):
        self.game = game
        self.mutation_rate = mutation_rate
        self.pop_card = pop_card
        self.elite_card = int(elite * pop_card)
        self.death_card = int(mortality * pop_card)
        self.pop = [
            Sample(creation="random", max_length=genome_length) for _ in range(pop_card)
        ]
        for sample in self.pop:
            temp = game.play(sample)
            sample.score = temp[0]
            sample.end_position = temp[1]
        self.pop.sort(key=lambda sample: sample.score, reverse=True)

    def cross_over_step(self, number):
        """
        self.pop[number] is replaced by a new sample obtained by a cross over
        between 2 random samples
        """
        parent1 = random.randint(0, self.pop_card - 1)

        parent2 = random.randint(0, self.pop_card - 1)
        self.pop[number] = Sample(
            creation="cross over", parent1=self.pop[parent1], parent2=self.pop[parent2],
        )
        temp = self.game.play(self.pop[number])
        self.pop[number].score = temp[0]
        self.pop[number].end_position = temp[1]

    def cross_over(self):
        """
        the elite won't be changed at all
        the worst pop will get replaced by offspring
        we allow new offspring to reproduce at the moment they are created
            in order not to complexify too much the implementation
        to do this, we have to calculate the score at the same time because
        it is useful to do the cross over

        """
        for k in range(self.pop_card - self.death_card, self.pop_card):
            self.cross_over_step(k)

    def mutation_step(self, number):
        """
        mutation of self.pop[number]
        """
        if random.random() < self.mutation_rate:
            self.pop[number].mutate()
            temp = self.game.play(self.pop[number])
            self.pop[number].score = temp[0]
            self.pop[number].end_position = temp[1]

    def mutation(self):
        """we will mutate all the population that is not the elite"""
        for k in range(self.elite_card, self.pop_card):
            self.mutation_step(k)

    def do_gen(self):
        self.cross_over()
        self.mutation()
        self.pop.sort(key=lambda sample: sample.score, reverse=True)

