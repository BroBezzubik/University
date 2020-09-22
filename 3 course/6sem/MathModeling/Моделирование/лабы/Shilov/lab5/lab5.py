import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from interpolation import interpolation

alpha0 = 0.01
alphaN = 0.009
teta = 293
Tos = 300
T0 = 300
F0 = 100
h = 0.1
l = L = 10
lambda0 = 0.1
R = 0.5
tau = 5

b = l * alphaN / (alphaN - alpha0)
a = -alpha0 * b

eps = 1e-3

# материал - вольфрам

T_table = [300 + h for h in range(0, 700 + 1, 100)] + \
          [1200 + h for h in range(0, 1800 + 1, 200)]

C_table = [
    2.544,
    2.615,
    2.656,
    2.689,
    2.717,
    2.748,
    2.783,
    2.817,
    2.893,
    2.977,
    3.070,
    3.124,
    3.270,
    3.381,
    3.502,
    3.640,
    3.792,
    3.968,
]

k_table = [
    0.163,
    0.156,
    0.146,
    0.137,
    0.130,
    0.124,
    0.120,
    0.117,
    0.114,
    0.111,
    0.110,
    0.109,
    0.108,
    0.107,
    0.107,
    0.107,
    0.109,
    0.108,
]


def C(T):
    return interpolation(T_table, C_table, T, 1)


def C12(T1, T2):
    return C((T1 + T2) / 2)


def k(T):
    return interpolation(T_table, k_table, T, 1)


def k12(T1, T2):
    return k((T1 + T2) / 2)


def alpha(x):
    return a / (x - b)


def p(x):
    return 2 * alpha(x) / R


def p12(x1, x2):
    return p((x1 + x2) / 2)


def f(x):
    return -2 * alpha(x) / R * Tos


def f12(x1, x2):
    return f((x1 + x2) / 2)


def lambda_(T):
    return k(T)


def xi12(T1, T2):
    return 2 * lambda_(T2) * lambda_(T1) / (lambda_(T2) + lambda_(T1))


p1_2 = p12
f1_2 = f12
xi1_2 = xi12


def checkIter(arrX, arrXNext):
    iterEps = 1e-3
    size = min(len(arrX), len(arrXNext))
    max = abs((arrX[0] - arrXNext[0]) / arrX[0])
    for i in range(1, size):
        d = abs((arrX[i] - arrXNext[i]) / arrX[i])
        if d > max:
            max = d
    return max >= iterEps


def need_next_iter(a, b):
    for i in range(len(a)):
        if abs((a[i][1] - b[i][1]) / b[i][1]) > eps:
            return True
    return False


def progonka(coefs):
    n = len(coefs)

    b1 = coefs[0][0]
    c1 = coefs[0][1]
    d1 = coefs[0][2]

    ksi = [0] * n
    ita = [0] * n

    g = b1
    ksi[0] = -c1 / g
    ita[0] = d1 / g

    for i in range(1, n - 1):
        ai = coefs[i][0]
        bi = coefs[i][1]
        ci = coefs[i][2]
        di = coefs[i][3]

        g = bi + ai * ksi[i - 1]
        ksi[i] = -ci / g
        ita[i] = (di - ai * ita[i - 1]) / g

    am = coefs[n - 1][0]
    bm = coefs[n - 1][1]
    dm = coefs[n - 1][2]

    res = [0] * n
    res[n - 1] = (dm - am * ita[n - 2]) / (bm + am * ksi[n - 2])

    for i in range(n - 2, -1, -1):
        res[i] = ksi[i] * res[i + 1] + ita[i]

    return res


def solve():
    k = 0
    n = int(L / h + 0.5)
    h2 = h * h

    ans = [0] * (n + 1)
    for i in range(n + 1):
        ans[i] = [0, 0]

    arrT = [T0 for i in range(n + 1)]
    arrTPrev = [0 for i in range(n + 1)]

    coefs = [[0, 0, 0, 0] for i in range(n + 1)]

    while True:
        coefs[0][0] = xi1_2(arrT[0], arrT[1]) + h2 / 8 * p1_2(0, h) + h2 / 4 * p(0)
        coefs[0][1] = -(xi1_2(arrT[0], arrT[1]) - h2 / 8 * p1_2(0, h))
        coefs[0][2] = h * F0 - h2 / 4 * (f1_2(0, h) + f(0))

        for i in range(1, n):
            coefs[i][0] = xi1_2(arrT[i], arrT[i - 1])
            coefs[i][1] = -(xi1_2(arrT[i], arrT[i - 1]) + xi1_2(arrT[i], arrT[i + 1]) + p(i * h) * h2)
            coefs[i][2] = xi1_2(arrT[i], arrT[i + 1])
            coefs[i][3] = f(i * h) * h2

        coefs[n][0] = xi1_2(arrT[n], arrT[n - 1]) - h2 / 8 * p1_2(L, L - h)
        coefs[n][1] = -(xi1_2(arrT[n], arrT[n - 1]) + h2 / 4 * p(L) + h2 / 8 * p1_2(L, L - h) + alpha(l) * h)
        coefs[n][2] = -h * alpha(L) * Tos + h2 / 8 * (3 * f(l) + f(l - h))

        arrTPrev = arrT
        arrT = progonka(coefs)

        k += 1

        if not (checkIter(arrTPrev, arrT) and k <= 100):
            break

    for i in range(n + 1):
        ans[i][0] = round(h * i, 3)
        ans[i][1] = round(arrT[i], 3)

    return ans


def solve2(res_step):
    res = []
    res_ans = []
    res_i = 0

    n = int(L / h + 0.5)
    h2 = h * h
    ans = []
    for i in range(n + 1):
        ans.append([h * i, T0])
    prev = [[0, 0] for i in range(n + 1)]

    res.append(ans)
    while need_next_iter(prev, ans):
        k = 0

        arrT = [ans[i][1] for i in range(n + 1)]
        arrTPrev = [0 for i in range(n + 1)]

        coefs = [[0, 0, 0, 0] for i in range(n + 1)]

        while True:
            coefs[0][0] = (xi1_2(arrT[0], arrT[1]) + h2 / 8 * p1_2(0, h) + h2 / 4 * p(0)) * tau + \
                          h2 / 4 * C(arrT[0]) + h2 / 8 * C12(arrT[0], arrT[1])  # K0
            coefs[0][1] = (h2 / 8 * p1_2(0, h) - xi1_2(arrT[0], arrT[1])) * tau + \
                          h2 / 8 * C12(arrT[0], arrT[1])  # M0
            coefs[0][2] = (h * F0 - h2 / 8 * (f(h) + 3 * f(0))) * tau + \
                          h2 / 4 * C(arrT[0]) * ans[0][1] + h2 / 8 * C12(arrT[0], arrT[1]) * (
                                      ans[0][1] + ans[1][1])  # P0

            for i in range(1, n):
                coefs[i][0] = xi1_2(arrT[i], arrT[i - 1]) * tau  # An
                coefs[i][2] = xi1_2(arrT[i], arrT[i + 1]) * tau  # Dn
                coefs[i][1] = -(coefs[i][0] + coefs[i][2] + p(i * h) * h2 * tau + C(arrT[i]) * h2)  # Bn
                coefs[i][3] = f(i * h) * h2 * tau - C(arrT[i]) * h2 * ans[i][1]  # Fn

            coefs[n][0] = (xi1_2(arrT[n], arrT[n - 1]) - h2 / 8 * p1_2(L, L - h)) * tau + \
                          h2 / 8 * C12(arrT[n], arrT[n - 1])  # KN
            coefs[n][1] = -(
                        xi1_2(arrT[n], arrT[n - 1]) + h2 / 4 * p(L) + h2 / 8 * p1_2(L, L - h) + alpha(l) * h) * tau + \
                          h2 / 4 * C(arrT[n]) + h2 / 8 * C12(arrT[n], arrT[n - 1])  # MN
            coefs[n][2] = -(h * alpha(L) * Tos - h2 / 8 * (3 * f(l) + f(l - h))) * tau + \
                          h2 / 4 * C(arrT[n]) * ans[n][1] + h2 / 8 * C12(arrT[n], arrT[n - 1]) * (
                                      ans[n][1] + ans[n - 1][1])  # PN

            arrTPrev = arrT
            arrT = progonka(coefs)

            k += 1

            if not (checkIter(arrTPrev, arrT) and k <= 100):
                break

        prev = ans
        ans = [[h * i, arrT[i]] for i in range(n + 1)]

        if res_i % res_step == 0:
            res.append(ans)
        res_i += 1

    return res


answ = solve2(1)

for i in range(len(answ)):
    X = [a[0] for a in answ[i]]
    T = [a[1] for a in answ[i]]
    plt.plot(X, T, color='red')

answ = solve()

X = [a[0] for a in answ]
T = [a[1] for a in answ]

plt.plot(X, T, color='green')

plt.grid(True)
plt.show()
