import sys
import time
import random
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ClickedLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(500, 100, 800, 600)
        self.setMaximumSize(self.width(), self.height())
        self.setWindowTitle('Aimer')
        self.setStyleSheet('background-color: cyan')

        self.setCursor(Qt.CrossCursor)
        pixmap = QPixmap('images/target.png')
        self.pixmap = pixmap.scaled(20, 20)

        self.diffucultText = 'Easy'
        self.score = 0
        self.count = 0
        self.loop = 10

        self.timer_label = QLabel(self)
        self.timer_label.setGeometry(int(self.width() / 2) - 50, 2, 100, 50)
        self.timer_label.setStyleSheet('border: 4px solid black')
        self.timer_label.setFont(QFont('Arial', 25))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.close()

        self.buttonEasy = QPushButton('Easy', self)
        self.buttonEasy.setGeometry(150, 70, 100, 30)
        self.buttonEasy.clicked.connect(self.buttonEasyHandler)
        self.buttonEasy.setStyleSheet('background-color: orange')
        self.buttonMedium = QPushButton('Medium', self)
        self.buttonMedium.setGeometry(350, 70, 100, 30)
        self.buttonMedium.clicked.connect(self.buttonMediumHandler)
        self.buttonMedium.setStyleSheet('background-color: orange')
        self.buttonHard = QPushButton('Hard', self)
        self.buttonHard.setGeometry(550, 70, 100, 30)
        self.buttonHard.clicked.connect(self.buttonHardHandler)
        self.buttonHard.setStyleSheet('background-color: orange')

        self.score_label = QLabel(self)
        self.score_label.close()
        self.score_label.setGeometry(300, 150, 200, 120)
        self.score_label.setFont(QFont('Arial', 25))
        self.score_label.setAlignment(Qt.AlignCenter)

        self.pushButtonStart = QPushButton('Start', self)
        self.pushButtonStart.setGeometry(350, 300, 100, 100)
        self.pushButtonStart.pressed.connect(self.pushButtonStartHandler)
        self.pushButtonStart.setFont(QFont('Arial', 15))
        self.pushButtonStart.setStyleSheet('background-color: orange; color: white')

    def buttonEasyHandler(self):
        self.diffucultText = 'Easy'
        self.buttonEasy.setStyleSheet('background-color: yellow')
        self.buttonMedium.setStyleSheet('background-color: orange')
        self.buttonHard.setStyleSheet('background-color: orange')
    def buttonMediumHandler(self):
        self.buttonMedium.setStyleSheet('background-color: yellow')
        self.buttonEasy.setStyleSheet('background-color: orange')
        self.buttonHard.setStyleSheet('background-color: orange')
        self.diffucultText = 'Medium'
    def buttonHardHandler(self):
        self.buttonHard.setStyleSheet('background-color: yellow')
        self.buttonEasy.setStyleSheet('background-color: orange')
        self.buttonMedium.setStyleSheet('background-color: orange')

        self.diffucultText = 'Hard'

    def paintEvent(self, pe):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawRect(1, 1, 796, 596)

    def showTime(self):
        if self.flag:
            self.count += 1
        self.text = str(self.count / 10)
        self.timer_label.setText(self.text)

    def labelPressEvent(self):
        label = self.sender()
        label.close()
        self.score += 1
        if self.score == len(self.target_list):
            self.flag = False
            self.score = 0
            self.count = 0
            self.timer.stop()
            record = self.timer_label.text()
            self.score_label.setText(f'Congratzz\n{str(len(self.target_list))} attemps on\n{self.text} seconds.')
            self.pushButtonStart.setText('Try Again')
            self.pushButtonStart.show()
            self.score_label.show()
            self.buttonEasy.show()
            self.buttonMedium.show()
            self.buttonHard.show()

    def pushButtonStartHandler(self):
        self.flag = True
        self.timer_label.show()
        self.pushButtonStart.close()
        self.score_label.close()
        self.buttonEasy.close()
        self.buttonMedium.close()
        self.buttonHard.close()

        if self.diffucultText == 'Easy':
            self.target_list = [ClickedLabel(self) for _ in range(10)]
            for target in self.target_list:
                target.clicked.connect(self.labelPressEvent)
        elif self.diffucultText == 'Medium':
            self.target_list = [ClickedLabel(self) for _ in range(20)]
            for target in self.target_list:
                target.clicked.connect(self.labelPressEvent)
        elif self.diffucultText == 'Hard':
            self.target_list = [ClickedLabel(self) for _ in range(30)]
            for target in self.target_list:
                target.clicked.connect(self.labelPressEvent)

        create_thread = threading.Thread(target=create_target_proc, args=(self, ))
        create_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(100)


def create_target_proc(cls):
    for target in cls.target_list:
        target.setPixmap(cls.pixmap)
        target.setGeometry(random.randint(100, 700), random.randint(100, 500), 20, 20)
        target.show()
        time.sleep(0.3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
