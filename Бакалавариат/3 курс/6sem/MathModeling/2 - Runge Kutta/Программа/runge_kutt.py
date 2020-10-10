# получить следующие узлы сетки для системы из двух уравнений
def runge_kutt(h, func1, func2, x, y, z):
    k1 = func1(x, y, z)
    q1 = func2(x, y, z)

    k2 = func1(x + h/2, y + k1 * h/2, z + q1 * h/2)
    q2 = func2(x + h/2, y + k1 * h/2, z + q1 * h/2)

    k3 = func1(x + h/2, y + k2 * h/2, z + q2 * h/2)
    q3 = func2(x + h/2, y + k2 * h/2, z + q2 * h/2)

    k4 = func1(x + h, y + k3 * h, z + q3 * h)
    q4 = func2(x + h, y + k3 * h, z + q3 * h)

    y_next = y + h/6 * (k1 + 2*k2 + 2*k3 + k4)
    z_next = z + h/6 * (q1 + 2*q2 + 2*q3 + q4)

    return y_next, z_next
