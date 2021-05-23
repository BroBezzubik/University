from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QHeaderView
from matplotlib import pyplot
from PartialPlanTableWidget import *
from FullPlanTableWidget import *
from experiment_math import *
from model import *
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.show()
        self.almost_zero = 1e-10
        self.table_custom_full.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_custom_partial.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.full_plan = matrix_full_plan()
        self.partial_plan = matrix_partial_plan()
        self.custom_plan = [list(), list()]
        self.table_full = FullPlanTableWidget()
        self.table_partial = PartialPlanTableWidget()

        self.btn_do_plan.clicked.connect(self.do_plan)
        self.btn_set1.clicked.connect(self.set_full)
        self.btn_set2.clicked.connect(self.set_partial)
        self.btn_full.clicked.connect(self.show_table_full)
        self.btn_partial.clicked.connect(self.show_table_partial)
        self.btn_chart.clicked.connect(self.show_chart)

    def get_factor(self, entry):
        try:
            res = float(entry.text())
        except ValueError:
            entry.setStyleSheet("background:#f88;")
            raise ValueError()

        entry.setStyleSheet("background:#fff;")

        if abs(res) < self.almost_zero:
            res = self.almost_zero

        return res

    @staticmethod
    def get_custom_factor(entry):
        try:
            res = float(entry.text())
            if not -1 <= res <= 1:
                raise ValueError()
            if res.is_integer():
                res = int(res)
        except ValueError:
            entry.setStyleSheet("background:#f88;")
            raise ValueError()

        entry.setStyleSheet("background:#fff;")
        return res

    def do_plan(self):
        self.full_plan = matrix_full_plan()
        self.partial_plan = matrix_partial_plan()
        total_apps = 10000
        try:
            gen1_int_min = self.get_factor(self.entry_gen1_int_min)
            gen1_int_max = self.get_factor(self.entry_gen1_int_max)
            gen2_int_min = self.get_factor(self.entry_gen2_int_min)
            gen2_int_max = self.get_factor(self.entry_gen2_int_max)
            proc_int_min = self.get_factor(self.entry_proc_int_min)
            proc_int_max = self.get_factor(self.entry_proc_int_max)
            proc_dev_min = self.get_factor(self.entry_proc_dev_min)
            proc_dev_max = self.get_factor(self.entry_proc_dev_max)
        except ValueError:
            pass
        else:
            y = list()
            # for each experiment
            for exp in self.full_plan:
                gen_int1 = scale_factor(exp[1], gen1_int_min, gen1_int_max)
                gen_int2 = scale_factor(exp[2], gen2_int_min, gen2_int_max)
                proc_int = scale_factor(exp[3], proc_int_min, proc_int_max)
                proc_dev = scale_factor(exp[4], proc_dev_min, proc_dev_max)

                gens = [Generator(exp_by_intensity, (gen_int1,)), Generator(exp_by_intensity, (gen_int2,))]
                proc = Generator(norm_by_intensity, (proc_int, proc_dev))
                model = EventModel(gens, proc, total_apps)

                y.append(model.proceed() / total_apps)

            for exp in self.custom_plan:
                if len(exp) > 0:
                    gen_int1 = scale_factor(exp[1], gen1_int_min, gen1_int_max)
                    gen_int2 = scale_factor(exp[2], gen2_int_min, gen2_int_max)
                    proc_int = scale_factor(exp[3], proc_int_min, proc_int_max)
                    proc_dev = scale_factor(exp[4], proc_dev_min, proc_dev_max)

                    gens = [Generator(exp_by_intensity, (gen_int1,)), Generator(exp_by_intensity, (gen_int2,))]
                    proc = Generator(norm_by_intensity, (proc_int, proc_dev))
                    model = EventModel(gens, proc, total_apps)

                    y.append(model.proceed() / total_apps)

                else:
                    y.append(None)

            bfull = expand_full_plan(self.full_plan, self.custom_plan[:1], y)
            bpart = expand_partial_plan(self.partial_plan, self.custom_plan[1:], y)

            self.set_equasions(bfull, bpart)

    def set_equasions(self, bfull, bpart, accuracy=3):
        yl = str(round(bfull[0], accuracy)) + " + " + str(round(bfull[1], accuracy)) + "x1 + " + str(
            round(bfull[2], accuracy)) + "x2 + " + str(round(bfull[3], accuracy)) + "x3 + " + str(
            round(bfull[4], accuracy)) + "x4"
        yl = yl.replace("+ -", "- ")
        ynl = yl + " + " + str(round(bfull[5], accuracy)) + "x1x2 + " + str(
            round(bfull[6], accuracy)) + "x1x3 + " + str(
            round(bfull[7], accuracy)) + "x1x4 + " + str(round(bfull[8], accuracy)) + "x2x3 + " + str(
            round(bfull[9], accuracy)) + "x2x4 + " + str(round(bfull[10], accuracy)) + "x3x4 + \n" + str(
            round(bfull[11], accuracy)) + "x1x2x3 + " + str(round(bfull[12], accuracy)) + "x1x2x4 + " + str(
            round(bfull[13], accuracy)) + "x1x3x4 + " + str(round(bfull[14], accuracy)) + "x2x3x4 + " + str(
            round(bfull[15], accuracy)) + "x1x2x3x4"
        ynl = ynl.replace("+ -", "- ")
        ynl = ynl.replace("+ \n-", "-\n")
        self.label_yfl.setText(yl)
        self.label_yfnl.setText(ynl)

        yl = str(round(bpart[0], accuracy)) + " + " + str(round(bpart[1], accuracy)) + "x1 + " + str(
            round(bpart[2], accuracy)) + "x2 + " + str(round(bpart[3], accuracy)) + "x3 + " + str(
            round(bpart[4], accuracy)) + "x4"
        yl = yl.replace("+ -", "- ")
        ynl = yl + " + " + str(round(bpart[5], accuracy)) + "x1x2 + " + str(
            round(bpart[6], accuracy)) + "x1x3 + " + str(round(bpart[7], accuracy)) + "x2x3 + " + str(
            round(bpart[8], accuracy)) + "x1x4 + " + str(round(bpart[9], accuracy)) + "x2x4 + " + str(
            round(bpart[10], accuracy)) + "x3x4"
        ynl = ynl.replace("+ -", "- ")
        self.label_ypl.setText(yl)
        self.label_ypnl.setText(ynl)

    def set_full(self):
        try:
            x1 = self.get_custom_factor(self.entry_x1_1)
            x2 = self.get_custom_factor(self.entry_x2_1)
            x3 = self.get_custom_factor(self.entry_x3_1)
            x4 = self.get_custom_factor(self.entry_x4_1)
        except ValueError:
            pass
        else:
            self.custom_plan[0] = [1, x1, x2, x3, x4, x1 * x2, x1 * x3, x1 * x4, x2 * x3, x2 * x4, x3 * x4,
                                   x1 * x2 * x3, x1 * x2 * x4, x1 * x3 * x4, x2 * x3 * x4, x1 * x2 * x3 * x4]
            for i in range(len(self.custom_plan[0])):
                self.table_custom_full.setItem(1, i + 1, QTableWidgetItem(str(self.custom_plan[0][i])))

    def set_partial(self):
        try:
            x1 = self.get_custom_factor(self.entry_x1_2)
            x2 = self.get_custom_factor(self.entry_x2_2)
            x3 = self.get_custom_factor(self.entry_x3_2)
            x4 = self.get_custom_factor(self.entry_x4_2)
        except ValueError:
            pass
        else:
            self.custom_plan[1] = [1, x1, x2, x3, x4, x1 * x2, x1 * x3, x2 * x3, x1 * x4, x2 * x4, x3 * x4]
            for i in range(len(self.custom_plan[1])):
                self.table_custom_partial.setItem(1, i + 1, QTableWidgetItem(str(self.custom_plan[1][i])))

    @staticmethod
    def show_chart():
        max_int = 100
        total_apps = 10000
        proc_dev = 100000
        proc = Generator(exp_by_intensity, (max_int, proc_dev))
        Xdata = list()
        Ydata = list()

        for intensity in range(1, max_int + 1):
            gen = Generator(exp_by_intensity, (intensity,))
            model = EventModel([gen], proc, total_apps)
            Xdata.append(intensity / max_int)
            Ydata.append(model.proceed() / total_apps)

        pyplot.title('Average awaiting time')
        pyplot.grid(True)
        pyplot.plot(Xdata, Ydata)
        pyplot.xlabel("Strain (p)")
        pyplot.ylabel("Average time")
        pyplot.show()

    def show_table_full(self):
        self.table_full.show(self.full_plan, self.custom_plan[0])

    def show_table_partial(self):
        self.table_partial.show(self.partial_plan, self.custom_plan[1])
