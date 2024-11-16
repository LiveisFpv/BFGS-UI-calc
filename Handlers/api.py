from BFGS import BFGS
import numpy as np
class api_service():
    def __init__(self):
        self.ui_json = {}
        self.func=""
        self.eps=0.001
        self.vars=[]
        self.coords=[]
        self.derivatives=[]
    
    def parse_json(self,ui_json):
        """
        Параметры
        ---------
        ui_json : {
        func: string
        epsilon: float
        table_func: {
            vars: list
            coords: list
            derivatives: list
            }
        }
        Получаем информацию с пользовательского интерфейса и распаковываем их
        """

        self.ui_json = ui_json
        self.func = self.ui_json['func']
        self.eps = self.ui_json['epsilon']
        self.vars = self.ui_json['table_func']['vars']
        self.coords = self.ui_json['table_func']['coords']
        self.derivatives = self.ui_json['table_func']['derivatives']
        self.func=self.get_func(self.func)
        
        def derivate_func():
            derivatives_func = []
            for v in self.derivatives:
                derivatives_func.append(self.get_func(v))
            def function(x):
                return np.array([derivative(x) for derivative in derivatives_func])
            return function
        
        self.fprime=derivate_func()
    
    def get_func(self, func):
        def string_to_function(expression):
            def function(x):
                if x is None:
                    raise ValueError("Input 'x' cannot be None")
                
                # Проверка, что x - это список или массив
                if not hasattr(x, '__iter__'):
                    raise TypeError(f"Expected an iterable for 'x', but got {type(x)}")

                # Создаем словарь для переменных x
                local_dict = {'x': x}
                
                # Отладочный вывод: Проверяем что передаем в eval
                # print(f"Evaluating expression: {expression} with x = {local_dict}")
                
                # Выполняем eval с использованием локального контекста
                try:
                    return eval(expression, {"__builtins__": None,"np": np}, local_dict)
                except Exception as e:
                    raise ValueError(f"Error evaluating expression: {e}")
            return function
        return string_to_function(func)
    

    def get_result_BFGS(self):
        """
        Передаем основную информацию в пакет для расчета минимума методом BFGS
        """
        x0 = np.array([float(coord) for coord in self.coords])
        f = self.func
        fprime = self.fprime
        result, k = BFGS.BFGS(x0,f, fprime,None, self.eps).bfgs_method()
        return result, k


# Test functions:
if __name__ == '__main__':
    ui_json = {
        'func': 'x[0]**2 - x[0]*x[1] + x[1]**2 + 9*x[0] - 5*x[1] + 20',
        'epsilon': 0.001,
        'table_func': {
            'vars': ['x[0]', 'x[1]'],
            'coords': ['1', '2'],
            'derivatives': ['2*x[0] - x[1] + 9', '-x[0] + 2*x[1] - 5']
        }
    }
    api_service = api_service()
    api_service.parse_json(ui_json)
    try:
        result, k = api_service.get_result_BFGS()
        print(f'Минимум достигнут в точке: {result}')
    except Exception as e:
        print(f'Ошибка: {e}')