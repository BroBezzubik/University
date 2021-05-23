import numpy as np


def matrix_full_plan():
    res = [[1 for i in range(16)] for j in range(16)]
    step = 1
    for j in range(4):
        sign = -1
        for i in range(16):
            res[i][j + 1] = sign
            if (i + 1) % step == 0:
                sign *= -1
        step *= 2
    for i in range(16):
        res[i][5] = res[i][1] * res[i][2]
        res[i][6] = res[i][1] * res[i][3]
        res[i][7] = res[i][1] * res[i][4]
        res[i][8] = res[i][2] * res[i][3]
        res[i][9] = res[i][2] * res[i][4]
        res[i][10] = res[i][3] * res[i][4]
        res[i][11] = res[i][1] * res[i][2] * res[i][3]
        res[i][12] = res[i][1] * res[i][2] * res[i][4]
        res[i][13] = res[i][1] * res[i][3] * res[i][4]
        res[i][14] = res[i][2] * res[i][3] * res[i][4]
        res[i][15] = res[i][1] * res[i][2] * res[i][3] * res[i][4]
    return res


def matrix_partial_plan():
    res = [[1 for i in range(11)] for j in range(8)]
    step = 1
    for j in range(3):
        sign = -1
        for i in range(8):
            res[i][j + 1] = sign
            if (i + 1) % step == 0:
                sign *= -1
        step *= 2
    for i in range(8):
        res[i][4] = res[i][1] * res[i][2] * res[i][3]
        res[i][5] = res[i][1] * res[i][2]
        res[i][6] = res[i][1] * res[i][3]
        res[i][7] = res[i][2] * res[i][3]
        res[i][8] = res[i][1] * res[i][4]
        res[i][9] = res[i][2] * res[i][4]
        res[i][10] = res[i][3] * res[i][4]
    return res


def calc_b_full(plan, y):
    b = list()
    for i in range(len(plan[0])):
        b_cur = 0
        for j in range(len(plan)):
            b_cur += plan[j][i] * y[j]
        b.append(b_cur / len(plan))
    return b


def calc_b_partial(plan, y):
    b = list()
    for i in range(int(np.log2(len(plan))) + 2):
        b_cur = 0
        for j in range(len(plan)):
            b_cur += plan[j][i] * y[j]
        b.append(b_cur / len(plan))
    for i in range(int(np.log2(len(plan))) + 2, len(plan[0])):
        b_cur = 0
        for j in range(len(plan)):
            b_cur += plan[j][i] * y[j]
        b.append(b_cur / len(plan) / 2)
    return b


def calc_y(b, x):
    res = 0
    for i in range(len(b)):
        res += b[i] * x[i]
    return res


def fill_y(plan, b1, b2):
    ylin = list()
    ynlin = list()
    for i in range(len(plan)):
        if len(plan[i]):
            ylin.append(calc_y(b1, plan[i]))
            ynlin.append(calc_y(b2, plan[i]))
    return ylin, ynlin


def fill_plan(plan, y, ylin, ynlin):
    for i in range(len(plan)):
        if len(plan[i]):
            plan[i].append(y[i])
            plan[i].append(ylin[i])
            plan[i].append(ynlin[i])
            plan[i].append(abs(y[i] - ylin[i]))
            plan[i].append(abs(y[i] - ynlin[i]))


def expand_full_plan(plan, custom_plan, y):
    b = calc_b_full(plan, y)

    ylin, ynlin = fill_y(plan, b[:int(np.log2(len(b))) + 1], b)
    fill_plan(plan, y, ylin, ynlin)
    ylin, ynlin = fill_y(custom_plan, b[:int(np.log2(len(b))) + 1], b)
    if len(custom_plan) > 0:
        fill_plan(custom_plan, y[len(plan):], ylin, ynlin)

    return b


def expand_partial_plan(plan, custom_plan, y):
    b = calc_b_partial(plan, y)

    ylin, ynlin = fill_y(plan, b[:int(np.log2(len(b))) + 1], b)
    fill_plan(plan, y, ylin, ynlin)
    ylin, ynlin = fill_y(custom_plan, b[:int(np.log2(len(b))) + 1], b)
    if len(custom_plan) > 0:
        fill_plan(custom_plan, y[len(plan):], ylin, ynlin)

    return b


def scale_factor(x, realmin, realmax, xmin=-1, xmax=1):
    return realmin + (realmax - realmin) * (x - xmin) / (xmax - xmin)
