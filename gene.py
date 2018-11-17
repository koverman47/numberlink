#!/usr/bin/env python3


class Gene():

    def __init__(self, value, invariant = False):
        self.value = value # char
        self.invariant = invariant # True if terminal
        self.fitness = 0 # float
