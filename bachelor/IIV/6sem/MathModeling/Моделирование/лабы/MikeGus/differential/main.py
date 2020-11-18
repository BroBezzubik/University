import prettytable
import math


class Element:
    def __init__(self, power, coefficient):
        self.power = power
        self.coefficient = coefficient

    def multiply(self, other):
        result = Element(0, 0)
        result.power = self.power + other.power
        result.coefficient = self.coefficient * other.coefficient

        return result

    def add(self, other):
        if self.power != other.power:
            return None
        else:
            self.coefficient += other.coefficient
            return self

    def take_integral(self):
        self.power += 1
        self.coefficient /= self.power

    def __str__(self):
        return str(self.coefficient) + "x^" + str(self.power)


def f(x, y):
    return x**2 + y**2


def contains_power(array, value):
    for elem in array:
        if elem.power == value.power:
            return elem
    return None


def add_similar(array):
    result = []
    for elem in array:
        addition_elem = contains_power(result, elem)
        if addition_elem is not None:
            addition_elem.add(elem)
        else:
            result.append(elem)

    return result


def find_coefficients_for_power_of_2(array):
    result = []
    for elem1 in array:
        for elem2 in array:
            result.append(elem1.multiply(elem2))
    result = add_similar(result)

    return result


def take_integral(array):
    for elem in array:
        elem.take_integral()


def find_coefficients_for_level(level):
    if level < 1:
        return None

    array = [Element(3, 1/3)]
    for i in range(1, level):
        array = find_coefficients_for_power_of_2(array)
        array.append(Element(2, 1))
        take_integral(array)
    return array


def runge_2_next(runge_current, x_current, h, func):
    f_current = func(x_current, runge_current)
    return runge_current + h / 2 * (f_current + func(x_current + h, runge_current + h * f_current))


def runge_4_next(runge_current, x_current, h, func):
    f1 = func(x_current, runge_current)
    f2 = func(x_current + h / 3, runge_current + h / 3 * f1)
    f3 = func(x_current + h / 2, runge_current + h / 2 * f2)
    f4 = func(x_current + h, runge_current + h * f3)

    return runge_current + h / 6 * (f1 + 2 * f2 + 2 * f3 + f4)


def main():
    min_level = 3
    max_level = 9

    min_x = 0.0
    max_x = 2.0

    h = 1e-2

    steps = int((max_x - min_x) / h) + 1

    coefficients = []

    for i in range(min_level, max_level):
        coefficients.append(find_coefficients_for_level(i))

    x_current = min_x
    x = []

    # non_explicit_current = 0

    pikar = [[] for c in coefficients]

    explicit = []
    explicit_current = 0
    # non_explicit = []
    runge_2 = []
    runge_2_current = 0

    runge_4 = []
    runge_4_current = 0

    for i in range(steps):
        x.append(x_current)
        for i in range(len(coefficients)):
            value = 0
            for elem in coefficients[i]:
                value += elem.coefficient * x_current ** elem.power
            pikar[i].append(value)

        explicit.append(explicit_current)
        runge_2.append(runge_2_current)
        runge_4.append(runge_4_current)
        # non_explicit.append(non_explicit_current)

        explicit_current += h * (x_current ** 2 + explicit_current ** 2)
        runge_2_current = runge_2_next(runge_2_current, x_current, h, f)
        runge_4_current = runge_4_next(runge_4_current, x_current, h, f)

        x_current += h

        # if non_explicit_current is not None:
        #     D = 1 - 4 * h * (non_explicit_current + h * current_x**2)
        #     if D < 0:
        #         non_explicit_current = None
        #     else:
        #         non_explicit_current = 1 - math.sqrt(D)
        #         non_explicit_current /= 2 * h

    table = prettytable.PrettyTable()
    table.add_column("x", x)
    for i in range(len(pikar)):
        table.add_column("Пикар " + str(i + min_level) + "-ое", pikar[i])
    table.add_column("Лом. явный", explicit)
    table.add_column("Рунге-Кутты 2-ой", runge_2)
    table.add_column("Рунге-Кутты 4-ой", runge_4)
    # table.add_column("Лом. неявный", non_explicit)
    table.float_format = "6.5"

    # print(explicit_current)
    print(table)


if __name__ == "__main__":
    main()