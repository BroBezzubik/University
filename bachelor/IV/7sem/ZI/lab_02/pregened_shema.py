
from roter import *
from enigma import *

def prepared_shema():
    vocabuary = "abcdefghijklmnopqrstuvwxyz"
    vocabuary_len = len(vocabuary)

    enigma = Enigma(vocabuary)
    enigma.vocabulary = {letter: index for index, letter in enumerate(vocabuary)}
    enigma.vocabulary_back = {index : letter for index, letter in enumerate(vocabuary)}

    roter1 = Roter()
    roter1.shema_left_side = {9: 10, 4: 17, 12: 0, 14: 19, 18: 22, 13: 20, 6: 25, 21: 12, 0: 23, 24: 5, 17: 21, 15: 14,
                              20: 11, 8: 8, 22: 3, 5: 16, 3: 4, 25: 1, 16: 15, 23: 7, 10: 6, 11: 2, 2: 18, 19: 13,
                              1: 24, 7: 9}
    roter1.shema_rigth_side = {10: 9, 17: 4, 0: 12, 19: 14, 22: 18, 20: 13, 25: 6, 12: 21,
                               23: 0, 5: 24, 21: 17, 14: 15, 11: 20, 8: 8, 3: 22, 16: 5, 4: 3, 1: 25, 15: 16,
                               7: 23, 6: 10, 2: 11, 18: 2, 13: 19, 24: 1, 9: 7}
    roter1.offset = 0
    roter1.offset_current = 0
    roter1.count = vocabuary_len

    roter2 = Roter()
    roter2.shema_left_side = {13: 9, 4: 21, 9: 8, 21: 1, 16: 12, 24: 10, 7: 22, 8: 25, 20: 13, 2: 23, 19: 19,
                              11: 18, 0: 11, 3: 14, 5: 17, 15: 20, 10: 16, 6: 6, 23: 5, 14: 24, 1: 2, 12: 4, 22: 0, 25: 3, 17: 15, 18: 7}
    roter2.shema_rigth_side = {9: 13, 21: 4, 8: 9, 1: 21, 12: 16, 10: 24, 22: 7, 25: 8, 13: 20, 23: 2, 19: 19, 18: 11,
                               11: 0, 14: 3, 17: 5, 20: 15, 16: 10, 6: 6, 5: 23, 24: 14, 2: 1, 4: 12, 0: 22, 3: 25, 15: 17, 7: 18}

    roter2.offset = 0
    roter2.offset_current = 0
    roter2.count = vocabuary_len

    roter3 = Roter()
    roter3.shema_left_side = {15: 6, 25: 15, 22: 3, 19: 20, 10: 11, 17: 7, 7: 8, 1: 14, 5: 19, 8: 0, 21: 4, 23: 1, 3: 25,
                              12: 24, 0: 9, 9: 22, 13: 5, 6: 23, 4: 16, 24: 13, 11: 2, 2: 21, 18: 10, 16: 18, 14: 12, 20: 17}
    roter3.shema_rigth_side = {6: 15, 15: 25, 3: 22, 20: 19, 11: 10, 7: 17, 8: 7, 14: 1, 19: 5, 0: 8, 4: 21, 1: 23,
                               25: 3, 24: 12, 9: 0, 22: 9, 5: 13, 23: 6, 16: 4, 13: 24, 2: 11, 21: 2, 10: 18, 18: 16, 12: 14, 17: 20}

    roter3.offset = 0
    roter3.offset_current = 0
    roter3.count = vocabuary_len

    roters = []
    roters.append(roter1)
    roters.append(roter2)
    roters.append(roter3)

    enigma.roters = roters

    enigma.process()
