from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
import sys
from MainWindow import Ui_MainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from Kalah import *
from RealPlayer import *
from GoodBot import *
import time

class ClickedLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, e):  # press or maybe release?
        super().mouseReleaseEvent(e)
        self.clicked.emit()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.temp_states = []
        self.index = 0
        self.clicked_cell = -1
        self.edited_cells = []
        self.error_cell = -1
        self.step_time = 200  # ms
        self.is_run = False
        self.cell_color = QtGui.QColor(140, 90, 60)  # brown

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(QtCore.QSize(1100, 500))

        self.ui.label.setFont(QtGui.QFont("Calibri", 30))
        self.ui.label.setGeometry(QtCore.QRect(0, 20, self.width(), 40))

        board_width = 1000
        self.board_rect = QtCore.QRect((self.width() - board_width) / 2, 150, board_width, board_width / 4)

        mapper = QtCore.QSignalMapper(self)
        self.cells = [ClickedLabel(self) for i in range(14)]
        for i in range(14):
            if i != 6 and i != 13:
                self.cells[i].clicked.connect(mapper.map)
                mapper.setMapping(self.cells[i], i)
        mapper.mapped.connect(self.CellClicked)

        self.qp = QPainter()
        self.show()

    def CellClicked(self, i):
        if not self.is_run and not kalah.IsEnd:
            if i in kalah.GetPossibleMoves():
                self.error_cell = -1
                self.is_run = True
                self.temp_states = kalah.MakeMove(i)
                self.index = 0
                self.clicked_cell = i
                self.edited_cells = []
                QtCore.QTimer.singleShot(self.step_time, self.UpdateBoard)
                """if not kalah.IsEnd and kalah.active_player == 0:
                        kalah.MakeMoves(player0.ChooseMove(kalah))
                        self.SetCellsValues(kalah.state)"""
            else:
                self.error_cell = i

    def UpdateBoard(self):
        if self.index < len(self.temp_states):
            self.SetCellsValues(self.temp_states[self.index][0])
            self.edited_cells = self.temp_states[self.index][1]
            self.index += 1
        if self.index == len(self.temp_states):
            self.is_run = False
            self.clicked_cell = -1
            self.index += 1
        elif self.index > len(self.temp_states):
            self.edited_cells = []
            return
        QtCore.QTimer.singleShot(self.step_time, self.UpdateBoard)

    def GetColorFor(self, cell_index):
        """if kalah.IsEnd and self.edited_cells == []:
            if cell_index ==
        else:"""
        if cell_index == self.clicked_cell:
            color = QtGui.QColor(180, 90, 60)
        elif cell_index in self.edited_cells:
            color = QtGui.QColor(200, 140, 110)
        elif cell_index == self.error_cell:
            color = QtGui.QColor(240, 80, 80)
        else:
            color = QtGui.QColor(140, 90, 60)
        return color

    def DrawBoard(self):
        self.qp.setPen(QPen(QtGui.QColor(0, 0, 0), 2, Qt.SolidLine))
        self.qp.setBrush(QBrush(QtGui.QColor(240, 230, 180), Qt.SolidPattern))
        self.qp.drawRect(self.board_rect)

        cell_size = self.board_rect.width() / 10
        font = QtGui.QFont()
        font.setPixelSize(cell_size / 3)
        font.setFamily("TimesNewRoman")
        for i in range(14):
            self.cells[i].setFont(font)
            self.cells[i].setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.cells[i].setGeometry(QtCore.QRect(0, 0, cell_size, cell_size))
            self.cells[i].setStyleSheet("QLabel {color : black; }")

        for i in range(6):
            self.cell_color = self.GetColorFor(i)
            self.DrawCircle(self.board_rect.right() - cell_size * (2.5 + i), self.board_rect.top() + cell_size / 2, cell_size / 2.5)
            self.cell_color = self.GetColorFor(i + 7)
            self.DrawCircle(self.board_rect.left() + cell_size * (2.5 + i), self.board_rect.bottom() - cell_size / 2, cell_size / 2.5)
            self.cells[i].move(self.board_rect.right() - cell_size * (3 + i), self.board_rect.top())
            self.cells[i+7].move(self.board_rect.left() + cell_size * (2 + i), self.board_rect.bottom() - cell_size)

        self.cell_color = self.GetColorFor(6)
        self.DrawEllipse(self.board_rect.left() + cell_size, self.board_rect.top() + cell_size * 1.25, cell_size / 1.2, cell_size / 2.5)
        self.cell_color = self.GetColorFor(13)
        self.DrawEllipse(self.board_rect.right() - cell_size, self.board_rect.top() + cell_size * 1.25, cell_size / 1.2, cell_size / 2.5)
        self.cells[6].resize(cell_size * 2, cell_size * 0.82)
        self.cells[13].resize(cell_size * 2, cell_size * 0.82)
        self.cells[6].move(self.board_rect.left(), self.board_rect.top() + cell_size * 0.84)
        self.cells[13].move(self.board_rect.right() - cell_size * 2, self.board_rect.top() + cell_size * 0.84)

    def DrawCircle(self, x_center, y_center, radius):
        self.qp.setPen(QPen(QtGui.QColor(180, 100, 70), 3, Qt.SolidLine))
        self.qp.setBrush(QBrush(self.cell_color, Qt.SolidPattern))
        self.qp.drawEllipse(x_center - radius, y_center - radius, radius * 2, radius * 2)

    def DrawEllipse(self, x_center, y_center, radius_h, radius_v):
        self.qp.setPen(QPen(QtGui.QColor(180, 100, 70), 3, Qt.SolidLine))
        self.qp.setBrush(QBrush(self.cell_color, Qt.SolidPattern))
        self.qp.drawEllipse(x_center - radius_h, y_center - radius_v, radius_h * 2, radius_v * 2)

    def paintEvent(self, event):
        self.qp.begin(self)
        self.DrawBoard()
        self.qp.end()

    def SetCellsValues(self, state):
        for i in range(14):
            self.cells[i].setText(str(state[i]))

app = QtWidgets.QApplication([])
window = MainWindow()

kalah = Kalah()
window.SetCellsValues(kalah.state)
player0 = RealPlayer(0)
player1 = RealPlayer(1)
#  temp_moves = kalah.MakeMoves(player0.ChooseMove(kalah))
sys.exit(app.exec_())
