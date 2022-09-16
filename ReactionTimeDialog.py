import sys
import time
from threading import Timer
import random
from PyQt5.QtWidgets import *
from ui import ReactionDialogui

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ReactionDialogui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Reaction Time Test')
        self.ui.pushButton.clicked.connect(self.pushButtonHandler)

        self.t1 = None
        self.curr_button = 'ReactionTimeTestButton'

    def pushButtonHandler(self):
        if self.curr_button == 'ReactionTimeTestButton' or self.curr_button == 'TooSoonButton' or self.curr_button == 'TryAgainButton':
            waitForGreenButton(self)
            self.timer = Timer(random.randint(2, 5), clickButton, args=(self, ))
            self.timer.start()
        elif self.curr_button == 'WaitForGreenButton':
            tooSoonButton(self)
        elif self.curr_button == 'ClickButton':
            tryAgainButton(self)

def clickButton(cls):
    cls.curr_button = 'ClickButton'
    cls.ui.pushButton.setStyleSheet('QPushButton {background-color: green; color: white; font: 8pt MS Sans Serif;}')
    cls.ui.pushButton.setText('Click')
    cls.t1 = time.perf_counter()

def tryAgainButton(cls):
    cls.curr_button = 'TryAgainButton'
    t2 = time.perf_counter()
    cls.ui.pushButton.setStyleSheet('QPushButton {background-color: blue; color: white; font: 8pt MS Sans Serif;}')
    final_score = f'{int(1000 * (t2 - cls.t1))} ms'
    cls.ui.pushButton.setText(f'🕐\n{final_score}\nClick to keep going')

def waitForGreenButton(cls):
    cls.curr_button = 'WaitForGreenButton'
    cls.ui.pushButton.setStyleSheet('QPushButton {background-color: red; color: white; font: 8pt MS Sans Serif;}')
    cls.ui.pushButton.setText('Wait for green')

def tooSoonButton(cls):
    cls.curr_button = 'TooSoonButton'
    cls.ui.pushButton.setStyleSheet('QPushButton {background-color: blue; color: white; font: 8pt MS Sans Serif;}')
    cls.ui.pushButton.setText('❕\nToo soon\nClick to try again')
    cls.timer.cancel()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
