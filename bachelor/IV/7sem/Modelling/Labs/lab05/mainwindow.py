# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(504, 366)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.label_op1 = QtWidgets.QLabel(Form)
        self.label_op1.setGeometry(QtCore.QRect(366, 97, 16, 16))
        self.label_op1.setObjectName("label_op1")
        self.label_op0 = QtWidgets.QLabel(Form)
        self.label_op0.setGeometry(QtCore.QRect(366, 69, 16, 16))
        self.label_op0.setObjectName("label_op0")
        self.label_comp_title = QtWidgets.QLabel(Form)
        self.label_comp_title.setGeometry(QtCore.QRect(40, 180, 147, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label_comp_title.setFont(font)
        self.label_comp_title.setObjectName("label_comp_title")
        self.label_comp0 = QtWidgets.QLabel(Form)
        self.label_comp0.setGeometry(QtCore.QRect(366, 171, 16, 16))
        self.label_comp0.setObjectName("label_comp0")
        self.label_op2 = QtWidgets.QLabel(Form)
        self.label_op2.setGeometry(QtCore.QRect(366, 125, 16, 16))
        self.label_op2.setObjectName("label_op2")
        self.label_comp1 = QtWidgets.QLabel(Form)
        self.label_comp1.setGeometry(QtCore.QRect(366, 199, 16, 16))
        self.label_comp1.setObjectName("label_comp1")
        self.label_lost_clients_title = QtWidgets.QLabel(Form)
        self.label_lost_clients_title.setGeometry(QtCore.QRect(10, 300, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label_lost_clients_title.setFont(font)
        self.label_lost_clients_title.setObjectName("label_lost_clients_title")
        self.label_clients_title = QtWidgets.QLabel(Form)
        self.label_clients_title.setGeometry(QtCore.QRect(40, 20, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label_clients_title.setFont(font)
        self.label_clients_title.setObjectName("label_clients_title")
        self.label_op_title = QtWidgets.QLabel(Form)
        self.label_op_title.setGeometry(QtCore.QRect(40, 90, 138, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label_op_title.setFont(font)
        self.label_op_title.setObjectName("label_op_title")
        self.pushButton_model = QtWidgets.QPushButton(Form)
        self.pushButton_model.setGeometry(QtCore.QRect(350, 300, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.pushButton_model.setFont(font)
        self.pushButton_model.setObjectName("pushButton_model")
        self.le_lost_clients = QtWidgets.QLineEdit(Form)
        self.le_lost_clients.setGeometry(QtCore.QRect(230, 310, 91, 21))
        self.le_lost_clients.setReadOnly(True)
        self.le_lost_clients.setObjectName("le_lost_clients")
        self.le_op1_m = QtWidgets.QLineEdit(Form)
        self.le_op1_m.setGeometry(QtCore.QRect(380, 98, 41, 20))
        self.le_op1_m.setObjectName("le_op1_m")
        self.le_op1_d = QtWidgets.QLineEdit(Form)
        self.le_op1_d.setGeometry(QtCore.QRect(450, 98, 41, 20))
        self.le_op1_d.setObjectName("le_op1_d")
        self.le_op2_d = QtWidgets.QLineEdit(Form)
        self.le_op2_d.setGeometry(QtCore.QRect(450, 126, 41, 20))
        self.le_op2_d.setObjectName("le_op2_d")
        self.le_op2_m = QtWidgets.QLineEdit(Form)
        self.le_op2_m.setGeometry(QtCore.QRect(380, 126, 41, 21))
        self.le_op2_m.setObjectName("le_op2_m")
        self.label_client_pm = QtWidgets.QLabel(Form)
        self.label_client_pm.setGeometry(QtCore.QRect(450, 0, 41, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_client_pm.setFont(font)
        self.label_client_pm.setObjectName("label_client_pm")
        self.le_client_m = QtWidgets.QLineEdit(Form)
        self.le_client_m.setGeometry(QtCore.QRect(380, 30, 41, 20))
        self.le_client_m.setObjectName("le_client_m")
        self.le_client_d = QtWidgets.QLineEdit(Form)
        self.le_client_d.setGeometry(QtCore.QRect(450, 30, 41, 20))
        self.le_client_d.setObjectName("le_client_d")
        self.le_op0_m = QtWidgets.QLineEdit(Form)
        self.le_op0_m.setGeometry(QtCore.QRect(380, 70, 41, 20))
        self.le_op0_m.setObjectName("le_op0_m")
        self.label_op0_pm = QtWidgets.QLabel(Form)
        self.label_op0_pm.setGeometry(QtCore.QRect(380, 0, 41, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_op0_pm.setFont(font)
        self.label_op0_pm.setObjectName("label_op0_pm")
        self.le_op0_d = QtWidgets.QLineEdit(Form)
        self.le_op0_d.setGeometry(QtCore.QRect(450, 70, 41, 20))
        self.le_op0_d.setObjectName("le_op0_d")
        self.label_client_count_title = QtWidgets.QLabel(Form)
        self.label_client_count_title.setGeometry(QtCore.QRect(40, 250, 131, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label_client_count_title.setFont(font)
        self.label_client_count_title.setObjectName("label_client_count_title")
        self.le_client_count = QtWidgets.QLineEdit(Form)
        self.le_client_count.setGeometry(QtCore.QRect(372, 250, 121, 20))
        self.le_client_count.setObjectName("le_client_count")
        self.le_comp0_m = QtWidgets.QLineEdit(Form)
        self.le_comp0_m.setGeometry(QtCore.QRect(380, 172, 41, 21))
        self.le_comp0_m.setObjectName("le_comp0_m")
        self.le_comp1_m = QtWidgets.QLineEdit(Form)
        self.le_comp1_m.setGeometry(QtCore.QRect(380, 200, 41, 21))
        self.le_comp1_m.setObjectName("le_comp1_m")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 50, 501, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(0, 150, 501, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setGeometry(QtCore.QRect(430, 0, 20, 241))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(Form)
        self.line_4.setGeometry(QtCore.QRect(353, 0, 20, 241))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(Form)
        self.line_5.setGeometry(QtCore.QRect(0, 230, 501, 20))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(Form)
        self.line_6.setGeometry(QtCore.QRect(0, 270, 501, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "лаб"))
        self.label_op1.setText(_translate("Form", "1"))
        self.label_op0.setText(_translate("Form", "0"))
        self.label_comp_title.setText(_translate("Form", "Компьютеры"))
        self.label_comp0.setText(_translate("Form", "0"))
        self.label_op2.setText(_translate("Form", "2"))
        self.label_comp1.setText(_translate("Form", "1"))
        self.label_lost_clients_title.setText(_translate("Form", "Вероятность отказа"))
        self.label_clients_title.setText(_translate("Form", "Заявки"))
        self.label_op_title.setText(_translate("Form", "Операторы"))
        self.pushButton_model.setText(_translate("Form", "Рассчитать"))
        self.le_op1_m.setText(_translate("Form", "40"))
        self.le_op1_d.setText(_translate("Form", "10"))
        self.le_op2_d.setText(_translate("Form", "20"))
        self.le_op2_m.setText(_translate("Form", "40"))
        self.label_client_pm.setText(_translate("Form", "delta"))
        self.le_client_m.setText(_translate("Form", "10"))
        self.le_client_d.setText(_translate("Form", "2"))
        self.le_op0_m.setText(_translate("Form", "20"))
        self.label_op0_pm.setText(_translate("Form", "time"))
        self.le_op0_d.setText(_translate("Form", "5"))
        self.label_client_count_title.setText(_translate("Form", "Всего заявок"))
        self.le_client_count.setText(_translate("Form", "300"))
        self.le_comp0_m.setText(_translate("Form", "15"))
        self.le_comp1_m.setText(_translate("Form", "30"))