import numpy as np
from roter import *


class Enigma(object):
    def __init__(self, letters):
        self.letters = letters
        self._vocabulary = letters
        self._vocabulary_back = None
        self._count = None
        self._roters = None

    @property
    def roters(self):
        return self._roters

    @roters.setter
    def roters(self, new_roters):
        self._roters = new_roters

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, new_count):
        self._count = new_count

    @property
    def vocabulary(self):
        return self._vocabulary

    @vocabulary.setter
    def vocabulary(self, new_vocabulary):
        self._vocabulary = new_vocabulary

    @property
    def vocabulary_back(self):
        return self._vocabulary_back

    @vocabulary_back.setter
    def vocabulary_back(self, new_vocabulary):
        self._vocabulary_back = new_vocabulary

    @property
    def reflector(self):
        return self._reflector

    @reflector.setter
    def reflector(self, reflector):
        self._reflector = reflector

    @staticmethod
    def generate_vocabulary(string):
        return {char: index for index, char in enumerate(string)}

    @staticmethod
    def generate_vocabulary_back(string):
        return {index : str(char) for index, char in enumerate(string)}

    def encoding(self, input_string):
        encoded_string = ""
        for char in input_string:
            char_key = self._vocabulary[char]

            for roter in self._roters:

                char_key = roter.proceed(char_key, "front")
                print(char_key)

            revesersed_roters = self._roters[len(self._roters) - 2::-1]
            for roter in revesersed_roters:

                char_key = roter.proceed(char_key, "back")
                print(char_key)

            self.rotate_roters()
            encoded_string += self._vocabulary_back[char_key]
            print("||")

        return encoded_string

    def rotate_roters(self):
        for roter in self._roters[:-1]:
            flag = roter.increment_offset()
            if flag == 0:
                break

    def reset(self):
        for item in self._roters[:-1]:
            item.reset()

    def process(self):
        while True:
            clear_text = str(input("Введите строку: "))
            crypted_text = self.encoding(clear_text)
            self.reset()
            uncrypted_text = self.encoding(crypted_text)
            print(clear_text, crypted_text, uncrypted_text, sep='\n')
            break