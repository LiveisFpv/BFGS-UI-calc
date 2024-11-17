from Handlers import handler
from PyQt6 import QtWidgets
import sys
app = QtWidgets.QApplication(sys.argv)
ui = handler.Ui_BFGS()
ui.show()
app.exec()