import random
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui import Keyboardui

with open('sources/TurkishWords.txt', encoding='utf-8') as f:
    a = f.read().split()
with open('sources/englishWords.txt', encoding='utf-8') as f:
    b = f.read().split()

arr = random.sample(a, 50)

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Keyboardui.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.textEdit.setReadOnly(True)
        self.ui.textEdit.setEnabled(False)
        self.ui.textEdit.setFont(QFont('Georgia', 16))

        self.lineEdit = LineEdit(self)
        self.lineEdit.setGeometry(30, 200, 340, 25)
        self.lineEdit.setFont(QFont('Georgia', 13))
        self.lineEdit.setPlaceholderText('Start typing when you ready..')
        self.lineEdit.editingFinished.connect(self.lineEditFinishedHandler)
        self.lineEdit.textChanged.connect(self.lineEditTextChangedHandler)
        self.lineEdit.setFocus()

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.timer_label = QLabel(self)
        self.timer_label.setGeometry(int(self.width() / 2) - 50, 2, 100, 30)
        self.timer_label.setStyleSheet('border: 1px solid black')
        self.timer_label.setFont(QFont('Arial', 20))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setText('01:00')

        self.ui.pushButtonRes.clicked.connect(self.pushButtonResHandler)
        self.ui.pushButtonRes.setText('')
        self.ui.pushButtonRes.setIcon(QIcon('images/try_again.png'))

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(30, 10, 100, 20)
        self.comboBox.addItems(['Türkçe', 'English'])
        self.comboBox.currentIndexChanged.connect(self.comboBoxHandler)

        self.flag = False
        self.time_counter = 60
        self.count = 0
        self.score = 0

        words = ' '.join(arr)
        self.ui.textEdit.append(words)
        self.ui.textEdit.moveCursor(QTextCursor.Start)

        for _ in arr[self.count]:
            self.ui.textEdit.moveCursor(QTextCursor.Right, QTextCursor.KeepAnchor)

    def showTime(self):
        if self.flag:
            self.time_counter -= 1

        if self.time_counter == 0:
            self.ui.textEdit.clear()
            self.ui.textEdit.setEnabled(True)
            self.ui.textEdit.append('Congratzzz...')
            self.ui.textEdit.append(f'\t\t{self.score / 1} WPM')
            self.timer_label.setText('0')
            self.flag = False

        if self.flag:
            text = str(self.time_counter)
            self.timer_label.setText(text)

    def comboBoxHandler(self):
        self.pushButtonResHandler()

    def lineEditTextChangedHandler(self):
            if self.timer_label.text() != '0':
                self.lineEdit.setPlaceholderText('')
                self.flag = True

    def pushButtonResHandler(self):
        self.ui.textEdit.clear()
        self.ui.textEdit.setEnabled(False)
        self.lineEdit.clear()
        self.flag = False
        self.score = 0
        self.time_counter = 60
        self.timer_label.setText('01:00')
        self.count = 0
        self.lineEdit.setPlaceholderText('Start typing when you ready..')
        self.lineEdit.setFocus()

        if self.comboBox.currentText() == 'Türkçe':
            arr = random.sample(a, 50)
            words = ' '.join(arr)
            self.ui.textEdit.append(words)
            self.ui.textEdit.moveCursor(QTextCursor.Start)
        elif self.comboBox.currentText() == 'English':
            arr = random.sample(b, 50)
            words = ' '.join(arr)
            self.ui.textEdit.append(words)
            self.ui.textEdit.moveCursor(QTextCursor.Start)


        for _ in self.ui.textEdit.toPlainText().split()[self.count]:
            self.ui.textEdit.moveCursor(QTextCursor.Right, QTextCursor.KeepAnchor)

    def lineEditFinishedHandler(self):
        try:
            if self.lineEdit.text() == ' ':
                self.lineEdit.clear()
            else:
                self.ui.textEdit.moveCursor(QTextCursor.Right)
                self.ui.textEdit.moveCursor(QTextCursor.Right)
                guess = self.lineEdit.text().strip()
                if guess == self.ui.textEdit.toPlainText().split()[self.count]:
                    self.score += 1

                self.count += 1
                self.lineEdit.clear()

                if self.count == len(arr):
                    self.flag = False

                for _ in self.ui.textEdit.toPlainText().split()[self.count]:
                    self.ui.textEdit.moveCursor(QTextCursor.Right, QTextCursor.KeepAnchor)
        except:
            pass




class LineEdit(QLineEdit):
    def keyPressEvent(self, event: QKeyEvent):
        super(LineEdit, self).keyPressEvent(event)
        if event.key() == Qt.Key_Space:
            self.editingFinished.emit()
        if event.key() == Qt.Key_Enter:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
