from BFGS import BFGS
from Interface.interface import Ui_BFGS_calc
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from Handlers import parse
class Ui_BFGS(Ui_BFGS_calc,QMainWindow):
    def __init__(self):
        super(Ui_BFGS,self).__init__()
        self.setupUi(self)
        self.Calculate.clicked.connect(self.calculate_button_clicked)
        self.Save.toggled.connect(self.save_button_clicked)
        self.Create_report.toggled.connect(self.create_report_button_clicked)
        self.Open.toggled.connect(self.open_button_clicked)
        self.Func.textChanged.connect(self.update_table)
        self.json={
            'func': "",
            'epsilon': 0.001,
            'table_func': {
                'vars': [],
                'coords': [],
                'derivatives': []
            },
            'iterations':[]
        }

    def update_table(self):
        vars=parse.parse(self.Func.text())
        self.Table_func.setRowCount(0)
        for i, var in enumerate(vars):
            self.Table_func.insertRow(i)
            self.Table_func.setItem(i, 0, QTableWidgetItem(str(var)))
            self.Table_func.setItem(i, 1, QTableWidgetItem(str(0)))
            self.Table_func.setItem(i, 2, QTableWidgetItem(str(0)))
        
    
    def calculate_button_clicked(self):
        self.json={
            'func': self.Func.text(),
            'epsilon': float(self.EPS.text()),
            'table_func': {
                'vars': [],
                'coords': [],
                'derivatives': []
            },
            'iterations':[]
        }
        func_str = self.Func.text()
        epsilon = float(self.EPS.text())
        f1=[]
        for r in range(0, self.Table_func.rowCount()):
            self.json['table_func']['vars'].append(self.Table_func.item(r,0).text())
            self.json['table_func']['coords'].append(float(self.Table_func.item(r,1).text()))
            self.json['table_func']['derivatives'].append(self.Table_func.item(r,2).text())
            f1.append(self.Table_func.item(r,2).text())
    
    def create_report_button_clicked(self):
        pass
    
    def open_button_clicked(self):
        pass
    
    def save_button_clicked(self):
        pass