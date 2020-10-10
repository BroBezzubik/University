from math import log


def get_table_i_t_m():
    table = [[0.5, 6400, 0.4],
             [1, 6790, 0.55],
             [5, 7150, 1.7],
             [10, 7270, 3],
             [50, 8010, 11],
             [200, 9185, 32],
             [400, 10010, 40],
             [800, 11140, 41],
             [1200, 12010, 39]]

    return table


def get_table_t_sigma():
    table = [[4000, 0.031],
             [5000, 0.27],
             [6000, 2.05],
             [7000, 6.06],
             [8000, 12.0],
             [9000, 19.9],
             [10000, 29.6],
             [11000, 41.1],
             [12000, 54.1],
             [13000, 67.7],
             [14000, 81.5]]

    return table


def get_i():
    return [elem[0] for elem in get_table_i_t_m()]


def get_t0():
    return [elem[1] for elem in get_table_i_t_m()]


def get_m():
    return [elem[2] for elem in get_table_i_t_m()]


def get_t():
    return [elem[0] for elem in get_table_t_sigma()]


def get_sigma():
    return [elem[1] for elem in get_table_t_sigma()]


def get_log_t():
    return [log(elem[0]) for elem in get_table_t_sigma()]


def get_log_sigma():
    return [log(elem[1]) for elem in get_table_t_sigma()]
