from math import exp, tan, pi, atan
import sys
from Thomas_algorithm import thomas_algorithm
from save_result import save_into_file
import matplotlib.pyplot as plt

# Input data:
p = 10
T_zero = 9000
T_w = 2000
R = 0.35
k_zero = 4e6  # 0.04
c = 300e6
nu = 0.6
alpha = pi / 2 - 0.1  # pi / 2 - delta
y_max = tan(alpha)
m = 0.786

n = 1000

h = 1 / n
x = [i * h for i in range(n + 1)]

z = [atan(y_max * i) / alpha for i in x]


def get_T(z):
    return T_zero + (T_w - T_zero) * (z ** p)


def get_k(T):
    return k_zero * (T / 2000) ** 2


def get_U_p(T, nu):
    return (6.1679e-19 * nu ** 3) / (exp(4.799e4 * nu / T) - 1)


def calculate_upper(z, h):
    if mode != 0:
        z_one_half = (z[1] + z[0]) / 2
        k_one_half = get_k(get_T(z_one_half))
        answer = [c * h * k_one_half * z_one_half * (z[0] - z_one_half) / 4 + z_one_half * c / (
                3 * R * R * k_one_half * (z[1] - z[0]))]
    else:
        answer = [1.0]

    for i in range(1, len(z) - 1):
        z_one_half = (z[i + 1] + z[i]) / 2
        k_one_half = get_k(get_T(z_one_half))
        answer.append(z_one_half / k_one_half / (z[i + 1] - z[i]))

    return answer


def calculate_middle(z, h, upper, lower):
    if mode != 0:
        z_one_half = (z[1] + z[0]) / 2
        k_one_half = get_k(get_T(z_one_half))
        answer = [-c * h * (z_one_half - z[0]) / 2 * (get_k(z[0]) * z[0] + k_one_half * z_one_half / 2) -
                  z_one_half * c / (3 * R * R * k_one_half * (z[1] - z[0]))]
    else:
        answer = [-1.0]

    for i in range(1, len(z) - 1):
        z_one_half = (z[i + 1] + z[i]) / 2
        zm_one_half = (z[i] + z[i - 1]) / 2
        v = z[i] * (z_one_half - zm_one_half)
        answer.append(lower[i - 1] * upper[i] + 3 * R * R * get_k(get_T(z[i])) * v)

    if mode != 0:
        z_one_half = (z[-1] + z[-2]) / 2
        k_one_half = get_k(get_T(z_one_half))
        answer.append(-c * h * (z[-1] - z_one_half) / 2 * (get_k(z[-1]) * z[-1] + k_one_half * z_one_half / 2) -
                      z[-1] * c / R * (m / 2 + 1 / (3 * R * k_one_half * (z[-1] - z[-2]))))
    else:
        p_with_tilda = alpha * (1 + x[-1] * x[-1] * y_max * y_max) / y_max
        mnozh = p_with_tilda / (3 * R * get_k(get_T(z[-1])) * h)
        answer.append(-m / 2 - mnozh)

    return answer


def calculate_lower(z, h):
    answer = []

    for i in range(1, len(z) - 1):
        z_one_half = (z[i - 1] + z[i]) / 2
        k_one_half = get_k(get_T(z_one_half))
        answer.append(z_one_half / k_one_half / (z[i] - z[i - 1]))

    if mode != 0:
        z_one_half = (z[-1] + z[-2]) / 2
        k_one_half = get_k(get_T(z_one_half))
        answer.append((c * h * k_one_half * z_one_half * (z_one_half - z[-1])) / 4 +
                      z_one_half * c / (3 * R * R * k_one_half * (z[-1] - z[-2])))
    else:
        pTilda = alpha * (1 + x[-1] * x[-1] * y_max * y_max) / y_max
        mnozh = pTilda / (3 * R * get_k(get_T(z[-1])) * h)
        answer.append(-mnozh)

    return answer


def calculate_right(z, h):
    if mode != 0:
        z_one_half = (z[1] + z[0]) / 2
        k_one_half = get_k(get_T(z_one_half))
        answer = [c * h * (z[0] - z_one_half) / 2 * (get_k(get_T(z[0])) * z[0] * get_U_p(get_T(z[0]), nu) +
                                                     k_one_half * z_one_half * get_U_p(get_T(z_one_half), nu))]
    else:
        answer = [0.0]

    for i in range(1, len(z) - 1):
        z_one_half = (z[i + 1] + z[i]) / 2
        zm_one_half = (z[i] + z[i - 1]) / 2
        V = z[i] * (z_one_half - zm_one_half)
        answer.append(3 * R * R * get_k(get_T(z[i])) * V * get_U_p(get_T(z[i]), nu))

    if mode != 0:
        z_one_half = (z[-1] + z[-2]) / 2
        k_one_half = get_k(get_T(z_one_half))
        answer.append(c * h * (z_one_half - z[-1]) / 2 * (get_k(get_T(z[-1])) * z[-1] * get_U_p(get_T(z[-1]), nu) +
                                                          k_one_half * z_one_half * get_U_p(get_T(z_one_half), nu)))
    else:
        answer.append(0.0)

    return answer


def calculate_all(z, h):
    low = calculate_lower(z, h)
    up = calculate_upper(z, h)
    mid = calculate_middle(z, h, up, low)
    right = calculate_right(z, h)

    answer = thomas_algorithm(low, mid, up, right)

    return answer


if __name__ == '__main__':
    if len(sys.argv) == 1:
        while True:
            try:
                mode = int(input('Enter 0 for short boundary condition\nEnter 1 for long boundary condition \n'
                                 'Enter 2 for both plots on one window\n(0 / 1 / 2): '))
                break
            except ValueError:
                print('Wrong input, try again!\n--')
    else:
        try:
            mode = int(sys.argv[1])
            if mode > 2 or mode < 0:
                raise ValueError('Mode must be between 0..2!')
        except ValueError as err:
            print(err.__str__())
            exit(1)

    u_equation = calculate_all(z, h)
    save_into_file([z, u_equation], ['z', 'u'], pts=6)
    plt.plot(z, u_equation)

    if mode == 2:
        mode = 0
        u_first = calculate_all(z, h)


    # Analytics part, comment all outer plt.plot, and uncomment inner plt.plot
    def derivative_for_k(z):
        answer = p * k_zero * T_zero * (T_w - T_zero) / 2e6 * z ** (p - 1) + p * k_zero * (T_w - T_zero) * (
                T_w - T_zero) / 2e6 * z ** (2 * p - 1)
        return answer


    def second_derivative_for_k(z):
        answer = k_zero * p * (p - 1) * T_zero * (T_w - T_zero) / 2e6 * z ** (p - 2) + k_zero * p * (2 * p - 1) * (
                T_w - T_zero) * (T_w - T_zero) / 2e6 * z ** (2 * p - 2)
        return answer


    def function_for_a(z):
        k = get_k(get_T(z))
        k_derivative = derivative_for_k(z)
        k_second_derivative = second_derivative_for_k(z)

        answer = 27 * k * R * z + 21 * k_derivative * R * z ** 2 + 3 * k_second_derivative * R * z ** 3 - \
              12 * k * R - 15 * k_derivative * R * z - 3 * k_second_derivative * R * z ** 2 + \
              6 * R ** 2 * k ** 2 / m - 9 * k ** 3 * R ** 3 * z ** 3 + 9 * k ** 3 * R ** 3 * z ** 2
        return answer


    def function_for_b(z):
        k = get_k(get_T(z))
        k_derivative = derivative_for_k(z)
        k_second_derivative = second_derivative_for_k(z)

        answer = 48 * k * R * z ** 2 + 27 * k_derivative * R * z ** 3 + 3 * k_second_derivative * R * z ** 4 - \
              27 * k * R * z - 21 * k_derivative * R * z ** 2 - 3 * k_second_derivative * R * z ** 3 + \
              6 * R ** 2 * k ** 2 / m - 9 * k ** 3 * R ** 3 * z ** 4 + 9 * k ** 3 * R ** 3 * z ** 3
        return answer


    def for_finding_u_equation(C1, C2, z):
        k = get_k(get_T(z))
        answer = C1 * (-2 / m + 3 * k * R * z ** 3 - 3 * k * R * z ** 2) + C2 * (
                -2 / m + 3 * k * R * z ** 4 - 3 * k * R * z ** 3)
        return answer


    z1, z3 = 0.25, 0.75
    k1, k3 = get_k(get_T(z1)), get_k(get_T(z3))

    a1 = function_for_a(z1)
    b1 = function_for_b(z1)
    d1 = 3 * R ** 2 * k1 ** 2 * get_U_p(get_T(z1), nu)

    a3 = function_for_a(z3)
    b3 = function_for_b(z3)
    d3 = 3 * R ** 2 * k3 ** 2 * get_U_p(get_T(z3), nu)

    C2 = (d1 * a3 / a1 - d3) / (b3 - b1 * a3 / a1)
    C1 = (-d1 - b1 * C2) / a1

    result = [for_finding_u_equation(C1, C2, i) for i in z]
    plt.plot(z, result)

    plt.xlabel('z')
    plt.ylabel('u')
    plt.show()
