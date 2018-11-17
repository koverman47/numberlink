#!/usr/bin/env python3

from evolution import GeneticAlgorithm as GA
import time
import sys


class Client():

    def __init__(self):
        self.maze = None
        self.colors = None


    def read_maze(self, path):
        f = open(path, 'r')
        self.maze = []
        self.colors = dict()

        x = 0
        for line in f:
            self.maze.append([])
            for y in range(len(line)):
                if line[y] == "\n":
                    continue

                self.maze[x].append(line[y])

                if line[y] != "_":
                    if line[y] not in self.colors:
                        self.colors[line[y]] = [(x, y)]
                    elif len(self.colors[line[y]]) < 2:
                        self.colors[line[y]].append((x, y))
                    else:
                        pass
            x += 1
        f.close()


    def write_maze(self, path, data):
        output = open(path, 'w')

        for x in data:
            for y in x:
                output.write(y)
            output.write("\n")

        output.close()


if __name__ == "__main__":
    client = Client()

    board = sys.argv[1] + ".txt"
    client.read_maze(board)
    ga = GA(client.maze, client.colors)
    start = time.time()
    ga.init_population()
    ga.solve()
    end = time.time()
    client.write_maze("output_" + board, ga.maze)
    print("Time to solution: %s" % str(end - start))


