from math import sin, cos, e, pi, asin
from copy import deepcopy


def f(x):
    return sin(pi * x / 6)


def sort_tabs(tab_sort, tab_2):
    # для сортировки таблицы по возрастанию х
    t = 1
    while t == 1:
        t = 0
        for i in range(len(tab_sort) - 1):
            if tab_sort[i] > tab_sort[i + 1]:
                t = 1
                tab_sort[i], tab_sort[i + 1] = tab_sort[i + 1], tab_sort[i]
                tab_2[i], tab_2[i + 1] = tab_2[i + 1], tab_2[i]


def choose_conf(tab_x, x, n):
    # выбор фрагмента таблицы (конфигурации) 
    LEN = len(tab_x)
    n += 1
    if n >= LEN:  # не крашим прогу, а делаем более надежной
        begin, end = 0, LEN
    elif x < tab_x[n // 2]:  # допускаем экстраполяцию
        begin, end = 0, n
    elif x > tab_x[LEN - n // 2 - 1]:
        begin, end = LEN - n, LEN
    else:
        pos = n // 2
        while x > tab_x[pos]:
            pos += 1
        begin, end = pos - n // 2, pos - n // 2 + n
    return (begin, end)


def sep_df(conf_x, conf_y):
    # таблица разделенных разностей
    # создается нерекурсивно
    LEN = len(conf_x)
    df = [[0 for k in range(LEN - i)] for i in range(LEN)]
    for i in range(LEN):
        for j in range(LEN - i):
            if i == 0:
                df[i][j] = conf_y[j]
            else:
                df[i][j] = (df[i - 1][j] - df[i - 1][j + 1]) / (conf_x[j] - conf_x[j + i])
    return df


def calc(x, conf_x, df):
    # вычисление конечного результата
    y = df[0][0]
    LEN = len(df)
    for i in range(1, LEN):
        temp = df[i][0]
        for j in range(i):
            temp *= x - conf_x[j]
        y += temp
    return y


def interpolation(tab_x, tab_y, x, n, flag='notdebug'):
    # собираем все в одну функцию
    # будем сортировать и удалять элементы, поэтому создаем копии столбцов
    copy_x = deepcopy(tab_x)
    copy_y = deepcopy(tab_y)
    # сначала сортируем
    sort_tabs(copy_x, copy_y)
    # потом удаляем одинаковые элементы из copy_x и соответствующие им в copy_y
    i = 0
    while i < len(copy_x) - 1:
        if abs(copy_x[i] - copy_x[i + 1]) < 1e-7:
            copy_x.remove(copy_x[i + 1])
            copy_y.remove(copy_y[i + 1])
            i -= 1
        i += 1
    begin, end = choose_conf(copy_x, x, n)
    conf_x, conf_y = copy_x[begin:end], copy_y[begin:end]

    df = sep_df(conf_x, conf_y)
    y = calc(x, conf_x, df)
    return y


if __name__ == '__main__':
    x1 = float(input('введите начальную границу таблицы х '))
    x2 = float(input('введите конечную границу таблицы х '))
    LEN = 0
    while LEN < 2:
        LEN = int(input('введите количество точек в таблице >= 2 '))

    tab_x = [x1 + k * (x2 - x1) / (LEN - 1) for k in range(LEN)]
    tab_y = [f(x) for x in tab_x]

    # print('таблица:')
    # for k in range(LEN) :
    #    print(tab_x[k], tab_y[k])

    print('введите х:')
    x = float(input())
    if x < min(tab_x) or x > max(tab_x):
        print('экстраполяция возможна, но результат может Вас удивить!')  # lol
    n = 0
    while n < 1:
        n = int(input('введите степень полинома: '))

    y = interpolation(tab_x, tab_y, x, n)
    print('результат интерполяции : ', y)
    print('точное значение : ', f(x))
