import numpy as np
from random import choice


class Roter(object):
    def __init__(self):
        self._shema_left_side = None
        self._shema_right_side = None
        self._offset = None
        self._offset_current = None
        self._count = None

    @property
    def shema_left_side(self):
        return self._shema_left_side

    @shema_left_side.setter
    def shema_left_side(self, shema):
        self._shema_left_side = shema

    @property
    def shema_rigth_side(self):
        return self._shema_right_side

    @shema_rigth_side.setter
    def shema_rigth_side(self, new_shema):
        self._shema_right_side = new_shema

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

    def reset(self):
        self._offset_current = self.offset

    def proceed(self, key, direction="front"):
        if direction == "front":
            return self._shema_left_side[(key + self._offset_current) % self._count]
        elif direction == "back":
            return self._shema_right_side[(key + self._offset_current) % self._count]

    @staticmethod
    def generate_shema(count):
        list1 = list(range(count))
        list2 = list(range(count))

        shema_left_side = {}
        shema_right_side = {}
        while len(list1) > 0 and len(list2) > 0:
            connector1 = choice(list1)
            connector2 = choice(list2)
            list1.remove(connector1)
            list2.remove(connector2)
            shema_left_side[connector1] = connector2
            shema_right_side[connector2] = connector1

        return shema_left_side, shema_right_side

    @staticmethod
    def generate_roter(count, offset):
        roter = Roter()
        roter.count = count
        roter.offset = offset
        roter.offset_current = offset
        roter.generate_shema()
        return roter

