from math import pi, sqrt, log10, floor
import matplotlib.pyplot as plt

def delta(f, p=7.5e-08, nu=0.001):
    return sqrt( p / (pi * f * nu) )


def Eff(delta, d, p=7.5e-08):
    return 36 + 20 * log10(delta / p) + 8.7 * (d / delta)

def main():
    gz_array = range(30, 3000, 10)  # Килогерцы
    d_array = [4e-4, 4e-3]          # Метры

    fig, ax = plt.subplots()
    
    for d in d_array:
        eff_arra = []
        for gz in gz_array:
            delta_var = delta(gz)
            eff_arra.append(floor(Eff(delta_var, d)))
        ax.plot(gz_array, eff_arra, label="{}м".format(d))
        print(eff_arra)
    ax.set_xlabel('f')
    # ax.set_ylabel('Э')
    ax.set_title("График эффективности")
    ax.legend()
    ax.grid()
    plt.show()


main()