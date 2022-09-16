import sys
from PyQt5.QtWidgets import *

from ui import MainWindowui
import KeyboardDialog
import ReactionTimeDialog
import AimerDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButtonReaction.clicked.connect(self.reactionHandler)
        self.ui.pushButtonAimer.clicked.connect(self.aimerHandler)
        self.ui.pushButtonKeyboard.clicked.connect(self.keyboardHandler)

        self.ui.actionExit.triggered.connect(self.actionExitHandler)

    def actionExitHandler(self):
        self.close()

    def reactionHandler(self):
        md = ReactionTimeDialog.MainWindow()
        result = md.exec()

    def aimerHandler(self):
        md = AimerDialog.MainWindow()
        result = md.exec()

    def keyboardHandler(self):
        md = KeyboardDialog.MainWindow()
        result = md.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
