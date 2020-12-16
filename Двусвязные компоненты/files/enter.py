from PyQt5.QtWidgets import QFileDialog, QMessageBox

from files.Temp import User_Class
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):

        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 561, 51))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)

        self.table = QtWidgets.QTableWidget(Form)
        self.table.setGeometry(QtCore.QRect(10, 100, 551, 221))
        self.table.setColumnCount(4)
        self.table.setRowCount(4)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        columns = self.table.columnCount()
        numbers = []
        for i in range(0, columns):
            numbers.append(str(i))
        self.table.setHorizontalHeaderLabels(numbers)
        self.table.setVerticalHeaderLabels(numbers)
        for i in range(0, columns):
            for j in range(0, columns):
                if i == j:
                    self.table.setItem(i, j, QtWidgets.QTableWidgetItem('0'))

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)

        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(310, 330, 251, 50))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.save_matrix_neog = QtWidgets.QPushButton(self.layoutWidget)
        self.save_matrix_neog.setObjectName("save_matrix_neog")
        self.horizontalLayout.addWidget(self.save_matrix_neog)
        self.cancel_matrix_neog = QtWidgets.QPushButton(self.layoutWidget)
        self.cancel_matrix_neog.setObjectName("cancel_matrix_neog")
        self.horizontalLayout.addWidget(self.cancel_matrix_neog)
        self.take_file_matrix = QtWidgets.QPushButton(Form)
        self.take_file_matrix.setGeometry(QtCore.QRect(420, 50, 141, 30))
        self.take_file_matrix.setObjectName("take_file_matrix")
        self.add_nodes = QtWidgets.QPushButton(Form)
        self.add_nodes.setGeometry(QtCore.QRect(20, 50, 140, 30))
        self.add_nodes.setObjectName("add_nodes")

        self.remove_nodes = QtWidgets.QPushButton(Form)
        self.remove_nodes.setGeometry(QtCore.QRect(220, 50, 140, 30))
        self.remove_nodes.setObjectName("remove_nodes")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Матрица смежности"))
        self.label.setText(_translate("Form", "Матрица смежности"))
        self.save_matrix_neog.setText(_translate("Form", "Сохранить"))
        self.cancel_matrix_neog.setText(_translate("Form", "Отмена"))
        self.take_file_matrix.setText(_translate("Form", "Считать с файла"))
        self.add_nodes.setText(_translate("Form", "Добавить вершину"))
        self.remove_nodes.setText(_translate("Form", "Удалить вершину"))


class First_Widget(QtWidgets.QWidget):
    numbers = list()

    def __init__(self):
        super(First_Widget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.show_matrix()
        self.ui.cancel_matrix_neog.clicked.connect(self.close_window)
        self.ui.save_matrix_neog.clicked.connect(self.save_matrix)
        self.ui.take_file_matrix.clicked.connect(self.read_from_file)
        self.ui.add_nodes.clicked.connect(self.more_column)
        self.ui.remove_nodes.clicked.connect(self.min_column)

    def more_column(self):
        n = self.ui.table.columnCount()
        self.ui.table.setRowCount(n + 1)
        self.ui.table.setColumnCount(n + 1)
        self.ui.table.resizeColumnsToContents()
        self.ui.table.resizeRowsToContents()
        columns = self.ui.table.columnCount()
        numbers = []
        for i in range(0, columns):
            numbers.append(str(i))
        self.ui.table.setHorizontalHeaderLabels(numbers)
        self.ui.table.setVerticalHeaderLabels(numbers)
        for i in range(0, columns):
            for j in range(0, columns):
                if i == j:
                    self.ui.table.setItem(i, j, QtWidgets.QTableWidgetItem('0'))

    def min_column(self):
        n = self.ui.table.columnCount()
        self.ui.table.setRowCount(n - 1)
        self.ui.table.setColumnCount(n - 1)
        self.ui.table.resizeColumnsToContents()
        self.ui.table.resizeRowsToContents()
        numbers = []
        columns = self.ui.table.columnCount()
        for i in range(0, columns):
            numbers.append(str(i))
        self.ui.table.setHorizontalHeaderLabels(numbers)
        self.ui.table.setVerticalHeaderLabels(numbers)
        for i in range(0, columns):
            for j in range(0, columns):
                if i == j:
                    self.ui.table.setItem(i, j, QtWidgets.QTableWidgetItem('0'))

    def show_matrix(self):
        us = User_Class()
        matrix = np.array(us.give_matrix())
        l = len(matrix)
        if l == 0:
            self.ui.table.setRowCount(4)
            self.ui.table.setColumnCount(4)
        else:
            self.ui.table.setRowCount(l)
            self.ui.table.setColumnCount(l)
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix)):
                self.ui.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(matrix[i][j])))
        self.head_table()

    def close_window(self):
        self.numbers.clear()
        self.hide()

    def read_from_file(self):
        file_name = QFileDialog.getOpenFileName()
        if file_name != ('', ''):
            path = file_name[0]
            temp = ""
            with open(path, "r") as file:
                line = file.readline()
                while line:
                    temp += line
                    line = file.readline()
            t = temp.split("\n")
            a = []
            for i in range(len(t)):
                s = t[i]
                a.append(s.split())
            l = self.ui.table.columnCount()
            if l != len(t):
                self.ui.table.setColumnCount(len(t))
                self.ui.table.setRowCount(len(t))
            for i in range(0, len(t)):
                for j in range(0, len(t)):
                    self.ui.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(a[i][j])))
            self.head_table()

    def head_table(self):
        l = self.ui.table.columnCount()
        numbers = []
        for i in range(0, l):
            numbers.append(str(i))
        self.ui.table.setHorizontalHeaderLabels(numbers)
        self.ui.table.setVerticalHeaderLabels(numbers)
        self.ui.table.resizeColumnsToContents()
        self.ui.table.resizeRowsToContents()

    def isSquare(self, m):
        return all(len(row) == len(m) for row in m)

    def check_ravnobok_matrix(self):
        if self.isSquare(self.numbers):
            return True
        else:
            error = QMessageBox()
            error.setWindowTitle("Matrix error")
            error.setText("Матрица должна быть квадратная!")
            error.setIcon(QMessageBox.Critical)
            error.exec_()
            return False

    def check_isNumeric_matrix(self):
        k = False
        for i in range(len(self.numbers)):
            for j in range(len(self.numbers[i])):
                if self.numbers[i][j].isnumeric():
                    if self.numbers[i][j] == '1' or self.numbers[i][j] == '0':
                        g = int(self.numbers[i][j])
                        self.numbers[i][j] = g
                        k = True
                    else:
                        error = QMessageBox()
                        error.setWindowTitle("Matrix error")
                        error.setText("В матрице могут быть только числа 0 или 1")
                        error.setIcon(QMessageBox.Critical)
                        error.exec_()
                        return False
                else:
                    error = QMessageBox()
                    error.setWindowTitle("Matrix error")
                    error.setText("В матрице должны быть только числа")
                    error.setIcon(QMessageBox.Critical)
                    error.exec_()
                    return False
        return k

    def check_main_diagonal(self):
        d = [self.numbers[i][i] for i in range(len(self.numbers))]
        count_zero = np.count_nonzero(d)
        if count_zero == 0:
            return True
        else:
            error = QMessageBox()
            error.setWindowTitle("Matrix error")
            error.setText("В главной диагонали должны быть только нули")
            error.setIcon(QMessageBox.Critical)
            error.exec_()
            return False

    def check_symmetric(self):
        for k in range(len(self.numbers)):
            for l in range(len(self.numbers[k])):
                if self.numbers[k][l] != self.numbers[l][k]:
                    return "No"
        return "Yes"

    def check_symmetric_org(self):
        count = 0
        for k in range(len(self.numbers)):
            for l in range(len(self.numbers[k])):
                if self.numbers[k][l] == 1 and self.numbers[l][k] == 1:
                    count += 1
        if count == 0:
            return True
        else:
            error = QMessageBox()
            error.setWindowTitle("Matrix error")
            error.setText("В ориентированной матрице нет симметричных элементов")
            error.setIcon(QMessageBox.Critical)
            error.exec_()
            return False

    def save_matrix(self):
        self.numbers.clear()
        columns = self.ui.table.columnCount()
        self.numbers = [[0] * columns for i in range(columns)]
        for i in range(0, columns):
            for j in range(0, columns):
                t = self.ui.table.item(i, j)
                if t:
                    if t.text():
                        self.numbers[i][j] = self.ui.table.item(i, j).text()
                else:
                    error = QMessageBox()
                    error.setWindowTitle("Matrix error")
                    error.setText("Таблица не заполненна полностью")
                    error.setIcon(QMessageBox.Critical)
                    error.exec_()
                    return False
        if self.check_ravnobok_matrix():
            if self.check_isNumeric_matrix():
                if self.check_main_diagonal():
                    if self.check_symmetric() == "Yes":
                        temp = User_Class()
                        temp.take_matrix(self.numbers)
                        temp.setIdentificator(1)
                        self.close()
                    elif self.check_symmetric_org():
                        temp = User_Class()
                        temp.take_matrix(self.numbers)
                        temp.setIdentificator(2)
                        self.close()

