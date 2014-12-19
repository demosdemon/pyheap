# coding=utf-8

import heapq
from itertools import count
from collections import MutableSet, Callable

REMOVED = (object(), )
__version__ = '0.1.12'
__all__ = ['Heap']


class Heap(MutableSet):
    def __init__(self, sequence=None, key=None):
        self.clear()
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
        return self.key(value), next(self.__sequence), value

    def __contains__(self, item):
        for key, _, value in self.__heap:
            if item == value:
                return True
        return False

    def __iter__(self):
        return (value for (key, _, value) in self.__heap if value is not REMOVED)

    def __nonzero__(self):
        try:
            self.peek()
            return True
        except (IndexError, KeyError):
            return False

    def __len__(self):
        return len(self.__heap)

    def add(self, item):
        heapq.heappush(self.__heap, self.__pair(item))

    push = add

    def discard(self, item):
        cmpkey = self.key(item)

        for idx, (key, _, value) in enumerate(self.__heap):
            if key == cmpkey:
                self.__heap[idx][-1] = REMOVED

    def pop(self):
        while self.__heap:
            (key, _, value) = heapq.heappop(self.__heap)
            if value is not REMOVED:
                return value
        raise KeyError

    def clear(self):
        self.__sequence = count()
        self.__heap = []

    def peek(self):
        while self.__heap and self.__heap[0][-1] is REMOVED:
            heapq.heappop(self.__heap)

        if self.__heap:
            return self.__heap[0][-1]
        else:
            raise KeyError

    def extend(self, iterable):
        if iterable:
            self |= iterable

    def __ior__(self, iterable):
        self.__heap.extend(map(self.__pair, iterable))
        heapq.heapify(self.__heap)
