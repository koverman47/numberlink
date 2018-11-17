#!/usr/bin/env python3

from chromosome import Chromosome
from copy import deepcopy
from random import random, shuffle


class GeneticAlgorithm():

    def __init__(self, maze, colors):
        self.maze = maze
        self.colors = colors
        self.chromosomes = []
        self.rate = 0.5
        self.MAX_EPOCHS = 10000
        self.POP_SIZE = 50
        self.KEYS = [k for k in colors]
        self.MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.FITNESS_MIDDLE = [0., 0.5, 1., 0.25, 0.]
        self.FITNESS_TERMINAL = [0., 1., 0.25, 0., 0.]


    '''
    ' Search for a solution
    ' @args: No
    ' @return: None
    '''
    def solve(self):
        assert len(self.chromosomes) > 1
        top_candidate = self.chromosomes[0]
        epoch = 1
        while epoch < self.MAX_EPOCHS:
            if epoch == 1000:
                self.rate = 0.25
            if epoch == 5000: 
                self.rate = 1./float(len(self.maze))
            if epoch == 7500:
                self.rate = 1./float(len(self.maze)**2)
            candidates = []
            for c in range(len(self.chromosomes)):
                temp = deepcopy(self.chromosomes[c])
                temp.mutate(self.MOVES, self.rate)
                temp.compute_fitness(self.FITNESS_MIDDLE, self.FITNESS_TERMINAL, self.MOVES)
                candidates.append(temp)
            index_list = []
            for c in range(len(self.chromosomes)):
                index_list.append(c)
            shuffle(index_list)
            for i in range(0, len(self.chromosomes), 2):
                temp1, temp2 = self.crossover(self.chromosomes[i], self.chromosomes[i + 1])
                temp1.compute_fitness(self.FITNESS_MIDDLE, self.FITNESS_TERMINAL, self.MOVES)
                temp2.compute_fitness(self.FITNESS_MIDDLE, self.FITNESS_TERMINAL, self.MOVES)
                candidates.append(temp1)
                candidates.append(temp2)
            self.chromosomes += candidates
            top_candidate = self.selection()
            if top_candidate.fitness == 1.:
                for x in range(len(self.maze)):
                    for y in range(len(self.maze)):
                        self.maze[x][y] = top_candidate.maze[x][y].value
                print("A solution has been found")
                return
            else:
                print("Top Fitness at Epoch %d: %f" % (epoch, top_candidate.fitness))
            epoch += 1
        assert top_candidate.fitness < 1.0
        for x in range(len(self.maze)):
            for y in range(len(self.maze)):
                self.maze[x][y] = top_candidate.maze[x][y].value
        print("No solution has been found")


    '''
    ' Probabilistic multipoint cross over between terminal genes
    ' @args:
    '   c1: Chromosome
    '   c2: Chromosome
    ' @constraints: c1 != c2
    ' @return tuple( Chromosome, Chromosome )
    '''
    def crossover(self, c1, c2):
        temp1 = deepcopy(c1)
        temp2 = deepcopy(c2)

        swap = (random() > 0.5)
        for x in range(len(self.maze)):
            for y in range(len(self.maze)):
                if c1.maze[x][y].invariant:
                    swap = (random() > 0.5)
                elif swap and not c1.maze[x][y].invariant:
                    temp = temp1.maze[x][y]
                    temp1.maze[x][y] = deepcopy(temp2.maze[x][y])
                    temp2.maze[x][y] = deepcopy(temp)
                else:
                    continue
        return (temp1, temp2)
        

    '''
    ' Randomly genereate the chromosome genes
    ' @args: No
    ' @return: None
    '''
    def init_population(self):
        assert len(self.chromosomes) == 0
        for k in range(self.POP_SIZE):
            self.chromosomes.append(Chromosome(deepcopy(self.maze), self.KEYS))
        assert len(self.chromosomes) == self.POP_SIZE


    '''
    ' Tournament Selection
    ' @args: No
    ' @return Chromosome
    '''
    def selection(self):
        assert len(self.chromosomes) > self.POP_SIZE
        index_list = []
        for c in range(len(self.chromosomes)):
            index_list.append(c)
        shuffle(index_list)
        
        winners = []
        for p in range(0, len(self.chromosomes), 3):
            winners.append(max([self.chromosomes[p], self.chromosomes[p + 1], self.chromosomes[p + 2]]))
        self.chromosomes = deepcopy(winners)
        assert len(self.chromosomes) == self.POP_SIZE

        return max(self.chromosomes)
            







