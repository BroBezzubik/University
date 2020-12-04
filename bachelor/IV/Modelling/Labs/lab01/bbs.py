import numpy as np
import bitarray
class Bbs(object):
    def __init__(self, x=41, p=3559, q=3571):
        self.p = p
        self.q = q
        self.M = p * q
        self.x0 = pow(x, 2) % self.M


    def generate_bit_array(self, bits_count):
        bitearray = bitarray.bitarray()
        x_n = self.x0
        for i in range(bits_count):
            x_n_1 = pow(x_n, 2) % self.M
            x_n = x_n_1
            bitearray.append(True) if ((1 | x_n_1) == x_n_1) else bitearray.append(False)
        return bitearray


    def generate_numbers(self, bits_array, bits_in_value=5, numbers_max=100):
        numbers = []
        count = 0
        for i in range(0, bits_array.length(), bits_in_value):
            number = int(bits_array[i : i+bits_in_value].to01(), 2)
            numbers.append(number)
            count += 1
            if count >= numbers_max:
                break
        return numbers




