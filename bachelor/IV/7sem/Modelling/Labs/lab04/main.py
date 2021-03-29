import mainwindow
from PyQt5.QtWidgets import *
from random import random,seed
from Queue import *
from scipy.stats import poisson


class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.process_btn.clicked.connect(self.process)

    def show_warning(self, txt=""):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Некорректные данные: " + txt)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def generate_mean(self):
        a = abs(float(self.a_value.text()))
        b = abs(float(self.b_value.text()))
        if a > b:
            a, b = b, a
        return a + random()*(b - a)

    def generate_norm(self):
        x = float(self.x_value.text())
        lam = float(self.x_value.text())
        result = poisson.cdf(x, lam)
        return result

        # sum = 0
        # for i in range(12):
        #     sum += random()
        # x = float(self.x_value.text())
        # if x < 0:
        #     x = abs(x)
        # lam = float(self.lam_value.text())
        # if lam < 0:
        #     return abs(abs(x) + abs(lam) * (sum - 6))
        # return abs(x + lam * (sum - 6))

    def dt_principle(self):
        current_time = 0
        dt = float(self.dt_value.text())
        if dt < 0:
            self.show_warning("Delta t")
            return
        time_scale = 0
        process_time_scale = 0
        requests_time = float(self.request_value.text())
        if requests_time < 0:
            self.show_warning("Количество заявок")
            return

        current_request_time = self.generate_mean()
        current_process_time = self.generate_norm()
        my_queue = Queue(start_size = 10)
        while current_time <= requests_time:
            if time_scale >= current_request_time:
                time_scale = 0
                current_request_time = self.generate_mean()
                # собрать статистику
                # проверка на увеличение очереди

                my_queue.add_request()

            if process_time_scale >= current_process_time:
                process_time_scale = 0
                current_process_time = self.generate_norm()
                # собрать статистику

            current_time += dt
            time_scale += dt
            process_time_scale += dt
        self.dt_principle_line.setText(str(my_queue.size))

    def event_principle(self):
        current_time = 0
        requests = int(self.request_value.text())
        if requests < 0:
            self.show_warning("Количество заявок")
            return
        my_queue = Queue(start_size=10)
        current_request_time = self.generate_mean()
        current_process_time = self.generate_norm()
        sbs = [current_request_time, current_process_time, requests]

        while True:
            sbs_min, i_min = min(sbs), sbs.index(min(sbs))
            if i_min == 0:
                current_time = sbs[i_min]
                sbs[i_min] = current_time + self.generate_mean()
                my_queue.add_request()
            elif i_min == 1:
                current_time = sbs[i_min]
                sbs[i_min] = current_time + self.generate_norm()
                # сбор статистики
            else:
                self.event_principle_line.setText(str(my_queue.size))
                return

    def process(self):
        self.dt_principle()
        self.event_principle()

seed()
if __name__ == "__main__":

    import sys
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

