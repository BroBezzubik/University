from scipy.stats import norm, poisson
import matplotlib.pyplot as plt
from math import sqrt, e, factorial
import numpy as np

def poisson_function(x, lam):
    return ( pow(e, -lam) * pow(lam, x) ) / factorial(x)


def poisson_density(x, lam):
    sum = 0
    for i in range(x):
        sum += ( pow(e, -lam) * pow(lam, i) ) / factorial(i)

    return sum


def ud_function(a, b, x):
    return (x - a) / (b - a) if a <= x < b else 0 if x < a else 1


def ud_density(a, b, x):
    return 1 / (b - a) if a <= x <= b else 0


def draw_graphics(x, y_function, y_density, name):
    fig, axs = plt.subplots(2, figsize=(6, 7))

    fig.suptitle(name)
    axs[0].plot(x, y_function, color='purple')
    axs[1].plot(x, y_density, color='purple')

    axs[0].set_xlabel('x')
    axs[0].set_ylabel('F(x)')

    axs[1].set_xlabel('x')
    axs[1].set_ylabel('f(x)')

    axs[0].grid(True)
    axs[1].grid(True)
    plt.show()


def main():
    a = 0
    b = 60
    delta = b - a
    x = np.arange(a - delta / 2, b + delta / 2, 0.001)
    y_function = [ud_function(a, b, _x) for _x in x]
    y_density = [ud_density(a, b, _x) for _x in x]
    draw_graphics(x, y_function, y_density, 'Равномерное распределение')

    lam = 36
    x = range(a, b, 1)
    poisson_dist = [poisson_function(_x, lam) for _x in x]
    poisson_den = [poisson_density(_x, lam) for _x in x]

    draw_graphics(x, poisson_den, poisson_dist, "Распределение паусона")


if __name__ == '__main__':
    main()