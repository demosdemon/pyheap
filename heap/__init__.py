# coding=utf-8

import heapq
from collections import MutableSet, Callable

REMOVED = (object(), )
__version__ = '0.1.6'
__all__ = ['Heap']


class Heap(MutableSet):
    def __init__(self, sequence=None, key=None):
        self.__heap = []
        self.key = key or (lambda x: x)
        self.extend(sequence)

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        if not isinstance(value, Callable):
            raise TypeError('key must be callable, got %s' % type(value).__name__)
        self.__key = value

        tmp = list(self)
        self.clear()
        self.extend(tmp)

    def __pair(self, value):
        return self.key(value), value

    def __contains__(self, item):
        for key, value in self.__heap:
            if item == value:
                return True
        return False

    def __iter__(self):
        return (value for (key, value) in self.__heap if value != REMOVED)

    def __nonzero__(self):
        for key, value in self.__heap:
            if value != REMOVED:
                return True
        return False

    def __len__(self):
        return sum([1 for item in self])

    def add(self, item):
        pair = (self.key(item), item)
        heapq.heappush(self.__heap, pair)

    push = add

    def discard(self, item):
        for idx, (key, value) in enumerate(self.__heap):
            if value == item:
                self.__heap[idx] = REMOVED

    def pop(self):
        while self.__heap:
            (key, value) = heapq.heappop(self.__heap)
            if value != REMOVED:
                return value
        raise KeyError

    def clear(self):
        self.__heap = []

    def peek(self):
        while self.__heap and self.__heap[0][1] == REMOVED:
            heapq.heappop(self.__heap)

        if self.__heap:
            return self.__heap[0][1]
        else:
            raise KeyError

    def extend(self, iterable):
        if iterable:
            self |= iterable

    def __ior__(self, iterable):
        self.__heap.extend(self.__pair(value) for value in iterable)
        heapq.heapify(self.__heap)
