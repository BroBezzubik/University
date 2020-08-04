# Барсуков Никита Михайлович ИУ7-66Б
# Лабораторная работа №1

# Для уравнения
# u'[k] = f[k] (x, u1, u2, ..., un), k = [1; n]
# u' = f(x, u) = x*x + u*u
# u(0) = 0
# получить хотя бы следующее (4ое) приближение [лучше n]

# Построить таблицу для каждого уравнения в отдельной таблице:
# x | Метод Пикара | Явный метод Эйлера | Неявный метод Эйлера | \
# Метод 2ого порядка Рунге-Кутта | Метод 4ого порядка Рунге-Кутта

# Применяем на промежутке x0, x1 с шагом h

# Пикар:
# u(кси) = ню
# u(x) = ню + интеграл от 0 до x от f(t, u) по dt - формальное решение
# В методе Пикара строится итерационный процесс:
# y [для итерации (s + 1)] (x) = ню + интеграл от 0 до x от f(t, y[s]) по dt
# y [0] = ню
# Явный:
# y[n+1] = y[n] + h * f(x[n], y[n]) 
# Неявный: 
# y[n+1] = y[n] + h * f(x[n+1], y[n+1])
# y[n+1] = y[n] + h * (x[n+1] ^ 2 + y[n+1] ^ 2)
# y[n+1] = y[n] + h * (x[n] + h) ^ 2 + h * y[n+1] ^ 2
# Рунге-Кутт:
# y[n+1] = y[n] + h*((1 - alpha) * f(x[n], y[n]) + alpha * f(x[n] + h/(2 * alpha),
# y[n] + h/(2 * alpha) * f(x[n], y[n])))
# alpha = 1
# aplha = 1/2


def next_y(prev):
    new_p = []
    new_z = []

    for i in range(len(prev[0])):
        for j in range(len(prev[0])):
            new_p.append(prev[0][i] + prev[0][j] + 1)
            new_z.append(prev[1][i] * prev[1][j] * new_p[-1])

    return [3] + new_p, [3] + new_z


def picar(x, n=1):
    y = 0

    coefs = ([], [])
    for i in range(n):
        coefs = next_y(coefs)


    for i in range(len(coefs[0])):
        y += (x ** coefs[0][i]) / coefs[1][i]

    return y
                             
def eiler(x0, x):
    y = 0
    
    while x0 <= x:
        y += h * (y * y + x0 * x0)
    
        x0 += h

    return y

def eiler_no(x0, x, n):
    y = 0

    while x0 <= x:
        yn = y

        for i in range(n):
            yn = y + 0.5 * h * (x0 ** 2 + y ** 2 + (x0 + h) ** 2 + yn)

        y = yn
        x0 += h

    return y

def eiler_alt(x0, x):
    y = 0

    while x0 <= x:
        x0 += h

        D = 1 - 4 * h * (y + h * x0 * x0)

        if D < 0:
            print("OH, NO!")
        elif D == 0:
            y = 0.5 / h
        else:
            y1 = (1 + D ** 0.5) / (2 * h)
            y2 = (1 - D ** 0.5) / (2 * h)
    ##        print(y1, y2)

            y += min(y1, y2)

    return y

def runge_kutt_2(x0, x, alpha=1):
    y = 0

    while x0 <= x:
        y += h * ((1 - alpha) * (x0 ** 2 + y ** 2) +
                  alpha * ((x0 + h / (2 * alpha)) ** 2 +
                           (y + (h / (2 * alpha)) * (x0 ** 2 + y ** 2)) ** 2))
        x0 += h

    return y

def runge_kutt_4(x0, x):
    y = 0

    while x0 <= x:
        k1 = x0 ** 2 + y ** 2
        k2 = (x0 + h / 2) ** 2 + (y + h / 2 * k1) ** 2
        k3 = (x0 + h / 2) ** 2 + (y + h / 2 * k2) ** 2
        k4 = (x0 + h) ** 2 + (y + h * k3) ** 2

        y += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        x0 += h

    return y


x0 = 0
x1 = 1
h = 0.01
n = 3
nk = 1
x = x0
alpha = 0.5

print("\n\n")
cnt = 0
while x <= x1:
    if cnt % 20 == 0:
        print("|--------+--------+--------+--------+--------+--------|")
        print("|   X    | Пикар  | Прямой |Неявный |Рун.-К.2|Рун.-К.4|")
        print("|--------+--------+--------+--------+--------+--------|")
    cnt += 1

    print("|{:<8.4f}|{:<8.4f}|{:<8.4f}|{:<8.4f}|{:<8.4f}|{:<8.4f}|".format(
          x, picar(x, n), eiler(0, x), eiler_alt(0, x),
          runge_kutt_2(0, x, alpha), runge_kutt_4(0, x)).replace(".", ","))

    x += h

if (cnt - 1) % 20:
    print("|--------+--------+--------+--------+--------+--------|")
    print("|   X    | Пикар  | Прямой |Неявный |Рун.-К.2|Рун.-К.4|")
    print("|--------+--------+--------+--------+--------+--------|")


