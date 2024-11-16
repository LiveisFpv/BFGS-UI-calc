from Interface.interface import Ui_BFGS_calc
from Interface.ResWindow import Ui_Result
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from Handlers import parse,api
from PyQt6 import QtCore, QtGui, QtWidgets
import sys

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
        self.e=None
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
        for r in range(0, self.Table_func.rowCount()):
            self.json['table_func']['vars'].append(self.Table_func.item(r,0).text())
            self.json['table_func']['coords'].append(float(self.Table_func.item(r,1).text()))
            self.json['table_func']['derivatives'].append(self.Table_func.item(r,2).text())
        print(self.json)
        res=api.api_service()
        res.parse_json(self.json)
        try:
            res=res.get_result_BFGS()
            self.json['iterations']=res[1]
            print(self.json)
        except Exception as e:
            self.e=e
        self.create_res_window()
        


    def create_res_window(self):
        # Используем уже существующий QApplication
        if not QApplication.instance():
            app = QApplication(sys.argv)  # если QApplication не существует
        else:
            app = QApplication.instance()

        # Создаем окно результата, но не добавляем новый layout
        self.result_window = QtWidgets.QWidget()  # Это новое окно, которое мы показываем
        self.result_ui = Ui_Result()
        self.result_ui.setupUi(self.result_window)
        
        # Обновляем информацию в окне результата
        
        if self.json['iterations']!=[]:
            self.result_ui.Func.setText(self.json['func'])
            # Заполняем таблицу результатами
            self.result_ui.res_func_table.setRowCount(len(self.json['iterations']['iterations']))
            for i, iteration in enumerate(self.json['iterations']['iterations']):
                self.result_ui.res_func_table.setItem(i, 0, QTableWidgetItem(str(i)))  # Номер
                self.result_ui.res_func_table.setItem(i, 1, QTableWidgetItem(str(iteration['f'])))  # Значение функции
                self.result_ui.res_func_table.setItem(i, 2, QTableWidgetItem(str(iteration['coord'])))  # Координаты

            self.result_window.show()
        else:
            self.result_ui.Func.setText(str(self.e))
            self.result_window.show()
    
    def create_report_button_clicked(self):
        pass
    
    def open_button_clicked(self):
        pass
    
    def save_button_clicked(self):
        pass