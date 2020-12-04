from bbs import *
import prettytable
import scipy.stats as stats
import random
from itertools import islice


def get_table_numbers():
    numbers = set()
    with open('digits.txt') as file:
        lines = islice(file, 10, None)
        for l in lines:
            numbers.update(set(l.split(" ")[1:-1]))
            if len(numbers) >= 3001:
                break
        numbers.remove("")
        numbers = list(numbers)[:3000]
    return numbers


def separate_numbers(numbers, limits, count):
    numbers_new = []
    count_num = 0
    for num in numbers:
        if  limits[0] <= num <= limits[1]:
            count_num += 1
            numbers_new.append(num)
        if count_num >= count:
            break

    return numbers_new


def k_stat(arr):
    n = len(arr) - 1
    h = 0
    l = 0

    for i in range(1, len(arr)):
        if (arr[i] - arr[i - 1]) > 0:
            h += 1
        else:
            l += 1

    h /= n
    l /= n

    return abs(h - l)


def main():
    bbs = Bbs()
    bit_array = bbs.generate_bit_array(1000000)

    table_BBS = prettytable.PrettyTable()

    numbers09 = bbs.generate_numbers(bit_array, 3)[:10]
    table_BBS.add_column("0-9", numbers09)

    numbers10_99 = bbs.generate_numbers(bit_array, 7)
    numbers10_99 = separate_numbers(numbers10_99, (10, 99), 10)
    table_BBS.add_column("10-99", numbers10_99)

    numbers100_999 = bbs.generate_numbers(bit_array, 10)
    numbers100_999 = separate_numbers(numbers100_999, (100, 999), 10)
    table_BBS.add_column("100-999", numbers100_999)



    numbers = get_table_numbers()

    table_Table = prettytable.PrettyTable()

    one_digit = [int(i) % 9 + 1 for i in numbers[:1000]]
    table_Table.add_column("0-9", one_digit[:10])

    two_digits = [int(i) % 90 + 10 for i in numbers[1000:2000]]
    table_Table.add_column("10-99", two_digits[:10])

    three_digits = [int(i) % 900 + 100 for i in numbers[2000:3000]]
    table_Table.add_column("100-999", three_digits[:10])

    print("### BBS ###")
    print(table_BBS)
    print("### Мера случайности BSS ###")
    print("0-9: {:.0f}%".format(k_stat(numbers09) * 100))
    print("10-99: {:.0f}%".format(k_stat(numbers10_99) * 100))
    print("100-999: {:.0f}%".format(k_stat(numbers100_999) * 100))

    print("\n"*3)

    print("### TABLE ###")
    print(table_Table)
    print("### Мера случайности Табличной ###")
    print("0-9: {:.0f}%".format(k_stat(one_digit) * 100))
    print("10-99: {:.0f}%".format(k_stat(two_digits) * 100))
    print("100-999: {:.0f}%".format(k_stat(three_digits) * 100))

    print("### Проверка критерия ###")
    count = int(input("Введите количество символов: "))
    user_numbers = list(map(int, input("\nEnter the numbers : ").strip().split()))[:count]
    print("Мера случайности: {:.0f}%".format(k_stat(user_numbers) * 100))


if __name__ == '__main__':
    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
