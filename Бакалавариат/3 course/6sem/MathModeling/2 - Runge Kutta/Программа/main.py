from math import pi, exp, log
from numpy import arange

import pylab

from runge_kutt import runge_kutt
from get_data import get_init
from interpolation import interpolation
from tables import *


def solve_system():
    res_uc = [Uc0]
    res_i = [I0]
    res_rp = [calc_rp(I0)]

    for j in range(1, len(time)):
        uc, i = runge_kutt(t_step, duc_dt, di_dt, time[j - 1], res_uc[j - 1], res_i[j - 1])
        rp = calc_rp(i)

        res_uc.append(uc)
        res_i.append(i)
        res_rp.append(rp)

    return res_uc, res_i, res_rp


if __name__ == '__main__':
    Tw = 2000
    R, Ck, Lk, Rk, Uc0, I0, Le, t_stop, t_step, newton_pow = get_init()

    time = arange(0, t_stop, t_step)
    array_Uc, array_I, array_Rp = solve_system()
    array_Up = [array_I[i] * array_Rp[i] for i in range(len(time))]

    pylab.subplot(2, 2, 1)
    pylab.plot(time, array_Rp)
    pylab.title('Rp(t)')

    pylab.subplot(2, 2, 2)
    pylab.plot(time, array_Uc)
    pylab.title('Uc(t)')

    pylab.subplot(2, 2, 3)
    pylab.plot(time, array_I)
    pylab.title('I(t)')

    pylab.subplot(2, 2, 4)
    pylab.plot(time, array_Up)
    pylab.title('Up(t)')

    pylab.show()
