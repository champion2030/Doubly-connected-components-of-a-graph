import sys
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QSizePolicy, \
    QPushButton, QGridLayout, QInputDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from files.enter import First_Widget
from files.Temp import User_Class
import os
from collections import defaultdict
from collections import defaultdict


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.title = 'КДМ ИДЗ'
        self.left = 200
        self.top = 200
        self.width = 1350
        self.height = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        vlay = QVBoxLayout(widget)
        hlay = QHBoxLayout()
        vlay.addLayout(hlay)
        self.setGeometry(self.left, self.top, self.width - 100, self.height)

        m = WidgetPlot(self)
        vlay.addWidget(m)


class WidgetPlot(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.grid = QGridLayout()
        self.canvas = PlotCanvas()

        self.do_matrix = QPushButton('Матрица смежности', self)
        self.do_matrix.setFixedHeight(50)

        self.draw_graph = QPushButton('Построить граф', self)
        self.draw_graph.setFixedHeight(50)

        self.task = QPushButton('Найти двусвязные компоненты', self)
        self.task.setFixedHeight(50)

        self.grid.setSpacing(20)
        self.grid.setColumnMinimumWidth(0, 200)
        self.grid.addWidget(self.do_matrix, 1, 0)
        self.grid.addWidget(self.draw_graph, 1, 1)
        self.grid.addWidget(self.task, 1, 2)

        self.grid.addWidget(self.canvas, 0, 0, 1, 3)
        self.setLayout(self.grid)

        self.do_matrix.clicked.connect(self.canvas.open_matrix_enter)
        self.draw_graph.clicked.connect(self.canvas.read_graph_from_file)
        self.task.clicked.connect(self.canvas.task)


class PlotCanvas(FigureCanvas):
    matrix = None
    graph = None
    cnames = [
        '#7FFFD4','g','blue','r','brown','mediumorchid','blueviolet','navy','royalblue','darkslategrey','limegreen','darkgreen','yellow','darkorange',
        '#D2691E','#FF7F50','#6495ED','#FFF8DC','#DC143C','#00FFFF','#00008B','#008B8B','#B8860B','#A9A9A9','#006400','#BDB76B','#8B008B','#556B2F','#FF8C00',
        '#FFD700', '#DAA520','#808080','#008000','#ADFF2F','#F0FFF0', '#FF69B4','#CD5C5C', '#4B0082','#FFFFF0', '#F0E68C','#E6E6FA','#FFF0F5','#7CFC00', '#FFFACD',
    '#ADD8E6', '#F08080','#E0FFFF','#FAFAD2','#90EE90','#D3D3D3','#FFB6C1','#FFA07A','#20B2AA','#87CEFA',
    '#778899','#B0C4DE','#FFFFE0','#00FF00','#32CD32','#FAF0E6','#FF00FF','#800000','#66CDAA','#0000CD','#BA55D3','#9370DB','#3CB371','#7B68EE','#00FA9A','#48D1CC',
    '#C71585','#191970','#F5FFFA','#FFE4E1','#FFE4B5','#FFDEAD','#000080','#FDF5E6',
    '#808000','#6B8E23','#FFA500','#FF4500','#00FF7F','#4682B4','#D2B48C','#008080','#D8BFD8','#FF6347','#40E0D0','#EE82EE','#F5DEB3',
    '#FFFFFF','#F5F5F5','#FFFF00','#9ACD32'
    ]

    def __init__(self):
        self.user = User_Class()
        self.second = First_Widget()
        figure = plt.figure()
        FigureCanvas.__init__(self, figure)
        self.setParent(None)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def read_graph_from_file(self):
        self.matrix = np.array(self.user.give_matrix())
        if self.user.get_identificator() == 1:
            self.graph = nx.Graph(self.matrix)
            self.plot()
        elif self.user.get_identificator() == 2:
            self.graph = nx.DiGraph(self.matrix)
            self.plot()
        else:
            error = QMessageBox()
            error.setWindowTitle("Matrix error")
            error.setText("Вы не ввели граф")
            error.setIcon(QMessageBox.Critical)
            error.exec_()

    def plot(self):
        self.figure.clear()
        nx.draw_circular(self.graph, with_labels=True, node_size=850)
        self.draw_idle()

    def open_matrix_enter(self):
        self.second.show()

    def task(self):
        if self.graph is None:
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Graph error")
            error_dialog.setText("Сначала нужно задать и построить граф")
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.exec_()
        elif len(self.graph.edges()) == 0:
            error = QMessageBox()
            error.setWindowTitle("Matrix error")
            error.setText("В графе нет рёбер")
            error.setIcon(QMessageBox.Critical)
            error.exec_()
        elif self.user.get_identificator() == 1:
            self.neorGraph()
        elif self.user.get_identificator() == 2:
            self.graph = nx.DiGraph(self.matrix)
            self.orGraph()


    def neorGraph(self):
        b = 0
        g = Graph(self.graph.number_of_nodes())
        k = self.graph.edges()
        for i in k:
            g.addEdge(i[0], i[1])
        m = g.BCC()
        if self.user.get_identificator() == 1:
            self.graph = nx.Graph()
        elif self.user.get_identificator() == 2:
            self.graph = nx.DiGraph()
        for i in m:
            b += 1
            for j in i:
                self.graph.add_edge(j[0], j[1], color=self.cnames[b])
        self.plot_1()

    def orGraph(self):
        colors = list()
        g = OrGraph(self.graph.number_of_nodes())
        k = self.graph.edges()
        for i in k:
            g.addEdge(i[0], i[1])
        m = g.printSCCs()
        x = -1
        for i in m:
            x += 1
            for j in i:
                if j in m[x]:
                    colors.append(self.cnames[x])
        self.plot_2(colors)

    def plot_1(self):
        self.figure.clear()
        edges = self.graph.edges()
        colors = [self.graph[u][v]['color'] for u, v in edges]
        nx.draw_circular(self.graph, with_labels=True, node_size=850, edge_color=colors, width=5)
        self.draw_idle()

    def plot_2(self, colors):
        self.figure.clear()
        nx.draw_circular(self.graph, node_color=colors, node_size=850, with_labels=True)
        self.draw_idle()


class Graph:
    matrix = []

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.Time = 0
        self.count = 0
        self.i = 0
        self.matrix.clear()
        self.file = open('Listing.txt', 'w')

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def BCCUtil(self, u, parent, low, disc, st):
        children = 0
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        for v in self.graph[u]:
            if disc[v] == -1:
                self.file.write('Так как disc[{}] == -1\n'.format(v))
                parent[v] = u
                self.file.write('  parent[{}] = {}\n'.format(v, u))
                children += 1
                self.file.write('  children = {}\n'.format(children))
                st.append((u, v))
                self.file.write('  st = {}\n'.format(st))
                self.file.write('  рекурсивно вызываем эту же функцию\n')
                self.BCCUtil(v, parent, low, disc, st)
                self.file.write('  low[{}] = min({}, {}) = {}\n'.format(u, low[u], low[v], min(low[u], low[v])))
                low[u] = min(low[u], low[v])
                if parent[u] == -1 and children > 1 or parent[u] != -1 and low[v] >= disc[u]:
                    self.file.write(
                        'Так как {} - точка сочленения, удалим все ребра из списка до ({}, {})\n'.format(u, u, v))
                    self.count += 1
                    w = -1
                    self.matrix.append([])
                    while w != (u, v):
                        w = st.pop()
                        self.matrix[self.i].append(w)
                        self.file.write('список w = {}\n'.format(w))
                        self.file.write('matrix = {}\n'.format(self.matrix))
                    self.i += 1
            elif v != parent[u] and low[u] > disc[v]:
                self.file.write('Так как {} != parent[{}] and low[{}] > disc[{}]\n'.format(v, u, u, v))
                low[u] = min(low[u], disc[v])
                self.file.write('  low[{}] = min(low[{}], disc[{}]) = {}\n'.format(u, u, v, low[u]))
                st.append((u, v))
                self.file.write('  st = {}\n'.format(st))

    def BCC(self):

        disc = [-1] * self.V
        low = [-1] * self.V
        parent = [-1] * self.V
        st = []
        self.i = 0
        self.file.write('Исходные данные: количество вершин - {}\n'.format(self.V))
        self.file.write('disc - пути обнаруженных вершин - {}\n'.format(disc))
        self.file.write('low - самая ранняя посещенная вершина - {}\n'.format(low))
        self.file.write('st - посещенные ребра - {}\n'.format(st))
        for i in range(self.V):
            if disc[i] == -1:
                self.file.write(
                    'Так как disc[{}] == -1, вызываем рекурсивную функцию для поиска точек сочленения\n'.format(i))
                self.BCCUtil(i, parent, low, disc, st)
            if st:
                self.file.write('Список не пуст, значит вытащим оттуда все ребра\n')
                self.count = self.count + 1
                self.matrix.append([])
                while st:
                    w = st.pop()
                    self.matrix[self.i].append(w)
                    self.file.write('список st = {}\n'.format(st))
                    self.file.write('matrix = {}\n'.format(self.matrix))
                self.i += 1
        self.file.write('Результат {}\n'.format(self.matrix))
        self.file.close()
        return self.matrix


class OrGraph:
    matrix = []

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.matrix.clear()
        self.z = 0

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def DFSUtil(self, v, visited):
        visited[v] = True

        self.matrix[self.z].append(v)
        for i in self.graph[v]:
            if visited[i] == False:
                self.DFSUtil(i, visited)
            else:
                self.z += 1

    def fillOrder(self, v, visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                self.fillOrder(i, visited, stack)
        stack = stack.append(v)

    def getTranspose(self):
        g = OrGraph(self.V)
        for i in self.graph:
            for j in self.graph[i]:
                g.addEdge(j, i)
        return g

    def printSCCs(self):
        stack = []
        visited = [False] * self.V
        for i in range(self.V):
            if visited[i] == False:
                self.fillOrder(i, visited, stack)
        gr = self.getTranspose()
        visited = [False] * (self.V)
        while stack:
            i = stack.pop()
            if visited[i] == False:
                self.matrix.append([])
                gr.DFSUtil(i, visited)
        return self.matrix


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
