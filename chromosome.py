#!/usr/bin/env/python3

from random import random, randint
from gene import Gene


class Chromosome():


    def __init__(self, maze, keys):
        self.maze = maze
        self.init_genes(keys)
        self.fitness = 0


    def compute_fitness(self, fit_mid, fit_term, moves):
        sigma = 0
        for x in range(len(self.maze)):
            for y in range(len(self.maze)):
                counter = 0
                for m in moves:
                    if x + m[0] >= 0 and x + m[0] < len(self.maze) and y + m[1] >= 0 and y + m[1] < len(self.maze):
                        if(self.maze[x + m[0]][y + m[1]]).value == self.maze[x][y].value:
                            counter += 1
                if self.maze[x][y].invariant:
                    self.maze[x][y].fitness = fit_term[counter]
                else:
                    self.maze[x][y].fitness = fit_mid[counter]
                sigma += self.maze[x][y].fitness
        self.fitness = sigma / (len(self.maze)**2)
                        


    def mutate(self, moves, rate):
        for x in range(len(self.maze)):
            for y in range(len(self.maze)):
                neighbors = dict()
                if not self.maze[x][y].invariant:
                    for m in moves:
                        if x + m[0] >= 0 and x + m[0] < len(self.maze) and y + m[1] >= 0 and y + m[1] < len(self.maze):
                            if not neighbors.get(self.maze[x + m[0]][y + m[1]].value):
                                neighbors[self.maze[x + m[0]][y + m[1]].value] = 1
                            else:
                                neighbors[self.maze[x + m[0]][y + m[1]].value] += 1
                    rand_val = random()
                    sigma = 0
                    for k, v in neighbors.items():
                        sigma += v
                        if random() < rate:
                            if sigma / 4 > rand_val:
                                self.maze[x][y].value = k
                                break


    '''
    ' Randomly create maze
    ' @args:
    '   keys: list[ { character } ]
    ' @return: None
    '''
    def init_genes(self, keys):
        for x in range(len(self.maze)):
            for y in range(len(self.maze)):
                if self.maze[x][y] != "_":
                    self.maze[x][y] = Gene(self.maze[x][y], True)
                else:
                    self.maze[x][y] = Gene(keys[randint(0, len(keys) - 1)])


    def __lt__(self, other):
        return self.fitness < other.fitness









