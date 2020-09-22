from copy import copy


class Polynomial:
    def __init__(self, power: int = 0, values: list = [1]):
        power += 1
        self.coefficients = []
        for i in range(power):
            self.coefficients.append(float(values[i]))


    def __str__(self):
        answer = '{:.2f}'.format(self.coefficients[0])
        for i in range(1, len(self.coefficients)):
            if abs(self.coefficients[i]) <= 1e-6:
                continue
            pl_mn = '+' if self.coefficients[i] >= 0 else '-'
            answer += ' {:s} {:.2f}x^{:d}'.format(pl_mn, self.coefficients[i], i)
        return answer

    def __getitem__(self, item: int):
        if item < 0 and item > len(self.coefficients):
            raise ValueError('No item by this index was found!')
        return self.coefficients[item]

    def __setitem__(self, key: int, value):
        if key < 0:
            raise ValueError('No item by this index was found!')
        if key > len(self.coefficients):
            for i in range(self.power(), key):
                self.coefficients.append(0)
        self.coefficients[key] = value

    def __add__(self, other):
        max_pol = self
        min_pol = other
        if max_pol.power() < min_pol.power():
            max_pol, min_pol = min_pol, max_pol
        answer = copy(max_pol)
        for i in range(0, min_pol.power() + 1):
            answer[i] += min_pol[i]
        return answer

    def __mul__(self, other):
        answer = Polynomial(power=self.power() + other.power(), values=[0] * (self.power() + other.power() + 1))
        for i in range(0, len(self.coefficients)):
            for j in range(0, len(other.coefficients)):
                answer[i + j] += self[i] * other[j]
        return answer
