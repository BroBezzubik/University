from math import *
import matplotlib.pyplot as plt

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
    dsp = [0.01, 0.09, 0.09, 0.08, 0.09, 0.14, 0.16]
    p = 850
    h = 0.0033
    L_array = []
    for index, f  in enumerate([125, 250, 500, 1000, 2000, 4000, 8000]):
        R = 20 * log10(f * p * h) - 60
        L = R + 10 * log10(dsp[index])
        L_array.append(L)
        print(L)
    print ("#" * 10)


def peregorodkaGKL():
    gips = [0.29, 0.1, 0.05, 0.04, 0.07, 0.09, 0.11]
    p = 1100
    h = 0.038
    L_array = []
    for index, f  in enumerate([125, 250, 500, 1000, 2000, 4000, 8000]):
        R = 20 * log10(f * p * h) - 60
        L = R + 10 * log10(gips[index])
        print(L)
    print ("#" * 10)


def oblicovka():
    dsp = [0.01, 0.09, 0.09, 0.08, 0.09, 0.14, 0.16]
    vata = [0.15, 0.36, 0.6, 0.78, 0.88, 0.9, 0.9]
    A_array = []
    B0 = []
    for index, dsp_val in enumerate(dsp):
        A = dsp_val * 3.6
        A_array.append(A)
        asr = A / 3.6
        B = A / (1 - asr)
        B0.append(B)

    B1 = []
    A1_array = []
    for index, vata_val in enumerate(vata):
        A = vata_val * 3.6
        A1_array.append(A)
        asr = A / 3.6
        B = A / (1 - asr)
        B1.append(B)

    for i, b0_item in enumerate(B0):
        L = 10 * log10(B1[index] / b0_item)
        print(L)
            
    
plt.plot([125, 250, 500, 1000, 2000, 4000, 8000], [7, 5, 2, 0, 10, 10, 14], label="Lтреб")
plt.plot([125, 250, 500, 1000, 2000, 4000, 8000], [0, 0, 6, 13, 20, 26, 32], label="Lкожух")
plt.plot([125, 250, 500, 1000, 2000, 4000, 8000], [8, 10, 13, 18, 26, 34, 40], label="Lгкл")
plt.plot([125, 250, 500, 1000, 2000, 4000, 8000], [0, 0, 0, 0, 4, 12, 19], label="Lдсп")
plt.plot([125, 250, 500, 1000, 2000, 4000, 8000], [29, 19, 19, 20, 19, 17, 16], label="Lзпм")
plt.legend()

plt.show()

Kozux()
peregorodkaGKL()
peregorodkaDSP()
oblicovka()


