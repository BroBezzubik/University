from numpy import arange
import matplotlib.pyplot as plt

class Data:
    x0 = -5
    l = 10           # Длина стержня (cm)
    R = 0.5          # Радиус стержня (cm)
    Tenv = 0       # Температура окружающей среды (K)
    F0 = 50        # Плотность теплового потока (W / (cm^2 * K))
    k0 = 0.1         # Коэффициент теплопроводности в начале стержня (W / (cm * K))
    kN = 0.2         # Коэффициент теплопроводности в конце стержня (W / (cm * K))
    alpha0 = 1e-2    # Коэффициент теплоотдачи в начале стержня (W / (cm^2 * K))
    alphaN = 9e-2  # Коэффициент теплоотдачи в конце стержня (W / (cm^2 * K))
    h = 0.0001
    bk = (kN * l) / (kN - k0)
    ak = - k0 * bk
    b_alpha = (alphaN * l) / (alphaN - alpha0)
    a_alpha = - alpha0 * b_alpha


    @staticmethod
    def k(x):
        return Data.ak / (x - Data.bk)

    @staticmethod
    def alpha(x):
        return Data.a_alpha / (x - Data.b_alpha)

    @staticmethod
    def Xn_plus_half(x):
        return (2 * Data.k(x) * Data.k(x + Data.h)) / \
               (Data.k(x) + Data.k(x + Data.h))

    @staticmethod
    def Xn_minus_half(x):
        return (2 * Data.k(x) * Data.k(x - Data.h)) / \
               (Data.k(x) + Data.k(x - Data.h))

    @staticmethod
    def p(x):
        return 2 * Data.alpha(x) / Data.R

    @staticmethod
    def f(x):
        return 2 * Data.alpha(x) / Data.R * Data.Tenv


def thomas_algorithm(A, B, C, D, K0, M0, P0, KN, MN, PN):  # Tridiagonal matrix algorithm
    # Initial values
    xi = [None, - M0 / K0]
    eta = [None, P0 / K0]

    # Straight running
    for i in range(1, len(A)):
        x = C[i] / (B[i] - A[i] * xi[i])
        e = (D[i] + A[i] * eta[i]) / (B[i] - A[i] * xi[i])

        xi.append(x)
        eta.append(e)

    # print(xi)
    # print(eta)

    # Reverse running
    y = [(PN - MN * eta[-1]) / (KN + MN * xi[-1])]

    for i in range(len(A) - 2, -1, -1):
        y_i = xi[i + 1] *  y[0] + eta[i + 1]

        y.insert(0, y_i)

    return y





def left_boundary_conditions():
    X_half = Data.Xn_plus_half(Data.x0)
    p1 = Data.p(Data.x0 + Data.h)
    f1 = Data.f(Data.x0 + Data.h)

    p0 = Data.p(Data.x0)
    f0 = Data.f(Data.x0)

    p_half = (p0 + p1) / 2

    K0 = X_half + Data.h * Data.h * p_half / 8 + Data.h * Data.h * p0 / 4
    M0 = Data.h * Data.h * p_half / 8 - X_half
    P0 = Data.h * Data.F0 + Data.h * Data.h * (3 * f0 + f1) / 4

    return K0, M0, P0


def right__boundary_conditions():
    X_half = Data.Xn_minus_half(Data.l)

    pN = Data.p(Data.l)
    pN1 = Data.p(Data.l - Data.h)
    fN = Data.f(Data.l)
    fN1 = (2 * Data.alpha(Data.l - Data.h)) / Data.R * Data.Tenv

    KN = - (X_half + Data.alphaN * Data.h) / Data.h - Data.h * (5 * pN + pN1) / 16
    MN = X_half / Data.h - Data.h * (pN + pN1) / 16
    PN = - Data.alphaN * Data.Tenv - Data.h * (3 * fN + fN1) / 8

    return KN, MN, PN


def calc_coefficients():
    A = []
    B = []
    C = []
    D = []

    for i in arange(Data.x0, Data.l, Data.h):
        An = Data.Xn_minus_half(i) / Data.h
        Cn = Data.Xn_plus_half(i) / Data.h
        Bn = An + Cn + Data.p(i) * Data.h
        Dn = Data.f(i) * Data.h

        A.append(An)
        B.append(Bn)
        C.append(Cn)
        D.append(Dn)

    return A, B, C, D


if __name__ == "__main__":
    a, b, c, d = calc_coefficients()
    # print(a)
    # print(b)
    # print(c)
    # print(d)

    k0, m0, p0 = left_boundary_conditions()
    # print(k0)
    # print(m0)
    # print(p0)

    kN, mN, pN = right__boundary_conditions()
    # print(kN)
    # print(mN)
    # print(pN)

    T = thomas_algorithm(a, b, c, d, k0, m0, p0, kN, mN, pN)
##    print(T)
    x = arange(Data.x0, Data.l, Data.h)
##    print(x)
    plt.title('Нагревание стержня')
    plt.grid(True)
    plt.plot(x, T, 'r', linewidth=0.5)
    plt.xlabel("Длина (cм)")
    plt.ylabel("Температура (K)")

    plt.savefig("plot.png")

    plt.show()
