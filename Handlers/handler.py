from Interface.interface import Ui_BFGS_calc
from Interface.ResWindow import Ui_Result
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from Handlers import parse,api
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import json
import sys

class Ui_BFGS(Ui_BFGS_calc,QMainWindow):
    def __init__(self):
        super(Ui_BFGS,self).__init__()
        self.setupUi(self)
        self.Calculate.clicked.connect(self.calculate_button_clicked)
        self.Save.triggered.connect(self.save_button_clicked)
        self.Create_report.triggered.connect(self.create_report)
        self.Open.triggered.connect(self.open_button_clicked)
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
        """Обновляет таблицу в соответствии с введенными данными"""
        vars=parse.parse(self.Func.text())
        self.Table_func.setRowCount(0)
        for i, var in enumerate(vars):
            self.Table_func.insertRow(i)
            self.Table_func.setItem(i, 0, QTableWidgetItem(str(var)))
            self.Table_func.setItem(i, 1, QTableWidgetItem(str(0)))
            self.Table_func.setItem(i, 2, QTableWidgetItem(str(0)))
        
    
    def calculate_button_clicked(self):
        """Выполняет вычисления и отображает результат в новом окне либо окно ошибки"""
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
        # print(self.json)
        #Запускаем api для взаимодействия с приложением и передаем данные
        res=api.api_service()
        res.parse_json(self.json)
        try:
            #Пытаемся получить данные
            res=res.get_result_BFGS()
            self.json['iterations']=res[1]
            # print(self.json)
            self.create_res_window()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить приближение: {e}")
        


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
    
    def create_report(self):
        """Создает отчет и сохраняет его в указанное пользователем место (JSON или TXT)."""
        self.calculate_button_clicked()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить отчет как",
            "",
            "JSON Files (*.json);;Text Files (*.txt);;All Files (*)",
        )
        if file_path:
            try:
                if file_path.endswith(".txt"):
                    self._save_as_txt(file_path)
                else:  # По умолчанию сохраняем в JSON
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(self.json, file, ensure_ascii=False, indent=4)
                QMessageBox.information(self, "Успех", "Отчет успешно сохранен!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить отчет: {e}")

    def _save_as_txt(self, file_path):
        """Сохраняет отчет в текстовом формате."""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("=== ОТЧЕТ ===\n\n")
                file.write(f"Функция: {self.json['func']}\n")
                file.write(f"Эпсилон: {self.json['epsilon']}\n\n")
                file.write("Таблица функций:\n")
                file.write("{:<10}{:<15}{:<15}\n".format("Переменная", "Координата", "Производная"))
                for var, coord, deriv in zip(
                    self.json['table_func']['vars'],
                    self.json['table_func']['coords'],
                    self.json['table_func']['derivatives']
                ):
                    file.write("{:<10}{:<15}{:<15}\n".format(var, coord, deriv))
                file.write("\nИтерации:\n")
                if self.json['iterations']:
                    for i, iteration in enumerate(self.json['iterations']['iterations']):
                        file.write(f"Итерация {i}:\n")
                        file.write(f"  Значение функции: {iteration['f']}\n")
                        file.write(f"  Координаты: {iteration['coord']}\n")
                else:
                    file.write("Нет данных об итерациях.\n")
        except Exception as e:
            raise e


    def open_button_clicked(self):
        """Загружает JSON-файл и обновляет данные в приложении."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть JSON-файл",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                self.json = data
                self.Func.setText(data['func'])
                self.EPS.setText(str(data['epsilon']))
                self.Table_func.setRowCount(0)
                for i, var in enumerate(data['table_func']['vars']):
                    self.Table_func.insertRow(i)
                    self.Table_func.setItem(i, 0, QTableWidgetItem(var))
                    self.Table_func.setItem(i, 1, QTableWidgetItem(str(data['table_func']['coords'][i])))
                    self.Table_func.setItem(i, 2, QTableWidgetItem(str(data['table_func']['derivatives'][i])))
                QMessageBox.information(self, "Успех", "Файл успешно загружен!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {e}")

    def save_button_clicked(self):
        """Сохраняет текущие данные в JSON-файл."""
        self.json['func']=self.Func.text()
        self.json['epsilon']=float(self.EPS.text())
        for r in range(0, self.Table_func.rowCount()):
            self.json['table_func']['vars'].append(self.Table_func.item(r,0).text())
            self.json['table_func']['coords'].append(float(self.Table_func.item(r,1).text()))
            self.json['table_func']['derivatives'].append(self.Table_func.item(r,2).text())
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить данные как",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    js=self.json.copy()
                    js['iterations']=[]
                    json.dump(js, file, ensure_ascii=False, indent=4)
                QMessageBox.information(self, "Успех", "Данные успешно сохранены!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные: {e}")