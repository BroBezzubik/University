from math import *

def Kozux():
    oblic = [0.02, 0.03, 0.03, 0.04, 0.05, 0.05, 0.05]
    p = 7800
    h = 0.003
    for index, f  in enumerate([125, 250, 500, 1000, 2000, 4000, 8000]):
        R = 20 * log10(f * p * h) - 60
        L = R + 10 * log10(oblic[index])
        print (L)
    print ("#" * 10)


def peregorodkaDSP():
    gips = [0.29, 0.1, 0.05, 0.04, 0.07, 0.09, 0.11]
    p = 1100
    h = 0.038
    for index, f  in enumerate([125, 250, 500, 1000, 2000, 4000, 8000]):
        R = 20 * log10(f * p * h) - 60
        L = R + 10 * log10(gips[index])
        #L = R + 10 * log10((A / (1 - a_sr) * S))
        print(L)


def peregorodkaGKL():
    pass


def oblicovka():
    pass


Kozux()
peregorodkaGKL()
peregorodkaDSP()
oblicovka()


