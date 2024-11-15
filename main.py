from Handlers import handler
from PyQt6 import QtCore, QtGui, QtWidgets
import sys
app = QtWidgets.QApplication(sys.argv)
BFGS_calc = QtWidgets.QMainWindow()
ui = handler.Ui_BFGS()
ui.setupUi(BFGS_calc)
BFGS_calc.show()
app.exec()