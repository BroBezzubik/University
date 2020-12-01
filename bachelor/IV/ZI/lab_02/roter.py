import numpy as np
from random import choice


class Roter(object):
    def __init__(self):
        self._shema = None
        self._offset = None
        self._offset_current = None
        self._count = None

    @property
    def shema(self):
        return self._shema

    @shema.setter
    def shema(self, shema):
        self._shema = shema

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, new_count):
        self._count = new_count

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset

    @property
    def offset_current(self):
        return self._offset_current

    @offset_current.setter
    def offset_current(self, new_offset):
        self._offset_current = new_offset

    def increment_offset(self):
        zefo_flag = 0
        self._offset_current += 1
        if self._offset_current >= self._count:
            self._offset_current = 0
            zefo_flag = 1
        return zefo_flag

    def generate_shema(self):
        list1 = list(range(self._count))
        list2 = list(range(self._count))

        shema = {}
        while len(list1) > 0 and len(list2) > 0:
            element1 = choice(list1)
            list1.remove(element1)
            list2.remove(element1)
            element2 = choice(list2)
            list1.remove(element2)
            list2.remove(element2)
            shema[element1] = element2
            shema[element2] = element1


        self._shema = shema

    def reset(self):
        self._offset_current = self.offset

    def proceed(self, key):
            key_shema = (key + self._offset_current) % self._count
            return self._shema[key_shema]


    @staticmethod
    def generate_roter(count, offset):
        roter = Roter()
        roter.count = count
        roter.offset = offset
        roter.offset_current = offset
        roter.generate_shema()
        return roter

