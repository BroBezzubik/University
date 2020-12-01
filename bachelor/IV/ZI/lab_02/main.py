from enigma import *
from roter import *
import collections


def main():
    key = 0
    if key == 1:
        enigma = Enigma("abcdefghijklmnopqrstuvwxyz")
        enigma.vocabulary = Enigma.generate_vocabulary("abcdefghijklmnopqrstuvwxyz")
        enigma.vocabulary_back = Enigma.generate_vocabulary_back("abcdefghijklmnopqrstuvwxyz")
        enigma.count = len("abcdefghijklmnopqrstuvwxyz")

        roters = []
        letter_count = enigma.count

        rot_count = int(input("Количество роторов (последний считает рефлектором у него смещение 0): "))
        for i in range(rot_count):
            offset = int(input("Введите начальное положение ротера: "))
            roters.append(Roter.generate_roter(letter_count, offset))

        enigma.roters = roters
        enigma.process()

    else:
        enigma = Enigma("abcdefghijklmnopqrstuvwxyz")
        enigma.vocabulary = Enigma.generate_vocabulary("abcdefghijklmnopqrstuvwxyz")
        enigma.vocabulary_back = Enigma.generate_vocabulary_back("abcdefghijklmnopqrstuvwxyz")
        enigma.count = len("abcdefghijklmnopqrstuvwxyz")

        roters = []
        offset = 0

        roter1 = Roter()
        roter1.count = enigma.count
        roter1.shema = {7: 21, 21: 7, 14: 8, 8: 14, 1: 5, 5: 1, 24: 20, 20: 24, 22: 10, 10: 22, 6: 4, 4: 6, 0: 3, 3: 0,
                        23: 25, 25: 23, 11: 9, 9: 11, 12: 18, 18: 12, 2: 19, 19: 2, 15: 17, 17: 15, 13: 16, 16: 13}
        roter1.offset = offset
        roter1.offset_current = offset

        roter2 = Roter()
        roter2.count = enigma.count
        roter2.shema = {22: 13, 13: 22, 1: 9, 9: 1, 8: 18, 18: 8, 7: 4, 4: 7, 21: 17, 17: 21, 20: 25, 25: 20, 16: 12,
                        12: 16, 24: 14, 14: 24, 23: 2, 2: 23, 6: 0, 0: 6, 3: 11, 11: 3, 5: 19, 19: 5, 15: 10, 10: 15}
        roter2.offset = offset
        roter2.offset_current = offset

        roter3 = Roter()
        roter3.count = enigma.count
        roter3.shema = {25: 8, 8: 25, 1: 21, 21: 1, 19: 9, 9: 19, 3: 15, 15: 3, 17: 18, 18: 17, 12: 16, 16: 12, 0: 4,
                        4: 0, 7: 5, 5: 7, 22: 14, 14: 22, 6: 20, 20: 6, 24: 11, 11: 24, 10: 23, 23: 10, 13: 2, 2: 13}
        roter3.offset = offset
        roter3.offset_current = offset

        roters.append(roter1)
        roters.append(roter2)
        roters.append(roter3)
        enigma.roters = roters
        enigma.process()


if __name__ == '__main__':
    main()
