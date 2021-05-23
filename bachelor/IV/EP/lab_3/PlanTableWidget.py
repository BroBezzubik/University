from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem


class PlanTableWidget(QDialog):
    def __init__(self, ui):
        super().__init__()
        uic.loadUi(ui, self)

        self.btn_close.clicked.connect(self.close)

    def show(self, plan, custom):
        for i in range(len(plan)):
            for j in range(len(plan[i])):
                self.table_plan.setItem(i + 1, j + 1, QTableWidgetItem(str(round(plan[i][j], 3))))

        for j in range(len(custom)):
            self.table_plan.setItem(len(plan) + 1, j + 1, QTableWidgetItem(str(round(custom[j], 3))))
        super().show()
