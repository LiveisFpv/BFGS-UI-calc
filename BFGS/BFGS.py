# -*- coding: utf-8 -*-
import numpy as np  # Импорт библиотеки для работы с массивами и матрицами
import numpy.linalg as ln  # Подмодуль для вычислений, связанных с линейной алгеброй
import scipy as sp  # Импорт библиотеки SciPy для оптимизации и других научных расчетов

class BFGS():
    """
    Класс реализующий метод BFGS для минимизации функции.
    """
    def __init__(self,x,f,fprime,maxiter=None,epsi=10e-3):
        """
        Параметры
        ----------
        f : function
            Целевая функция для минимизации.
        fprime : function
            Градиент целевой функции.
        x0 : nparray
            Начальная точка.
        maxiter : int, optional
            Максимальное число итераций (по умолчанию зависит от размерности задачи).
        epsi : float, optional
            Критерий остановки по норме градиента (по умолчанию 10e-3).
        """
        self.x = x
        self.f = f
        self.fprime = fprime
        self.maxiter = maxiter
        self.epsi = epsi
        self.iterations={
            "iterations":[
                {
                    'iteration': 0,
                    'coord': self.x.tolist(),
                    'f': float(self.f(self.x))
                }
            ]
            }
    def add_iter(self,xk,hk,k):
        self.iterations['iterations'].append({
            'iteration': k,
            'coord': xk.tolist(),
            'hessian': hk.tolist(),
            'f': float(self.f(xk))
        })
    # Реализация метода BFGS для минимизации функции
    def bfgs_method(self):
        """
        Минимизация функции f(x) методом BFGS.
        """
        if self.maxiter is None:
            # Если максимальное число итераций не указано, то задаем значение
            self.maxiter = len(self.x) * 200

        k = 0  # Номер итерации
        gfk = self.fprime(self.x)  # Градиент функции в начальной точке
        N = len(self.x)  # Размерность задачи
        I = np.eye(N)  # Единичная матрица
        Hk = I  # Начальная матрица Гессе (приближение)
        xk = self.x  # Текущая точка
    
        # Основной цикл оптимизации
        while ln.norm(gfk) > self.epsi and k < self.maxiter:  # Условие остановки: градиент мал или достигнут лимит итераций
            
            # pk - направление поиска, определяется как -Hk * gfk
            pk = -np.dot(Hk, gfk)
            
            # Выполняем линейный поиск для нахождения шага alpha_k
            line_search = sp.optimize.line_search(self.f, self.fprime, xk, pk)
            alpha_k = line_search[0]  # Берем только значение alpha_k
            
            if alpha_k is None:
                alpha_k = 0.05  # Если линейный поиск не дал значения, используем фиксированный шаг
            
            # Обновляем текущую точку xk
            xkp1 = xk + alpha_k * pk  # Новая точка
            sk = xkp1 - xk  # Вектор изменения точки
            xk = xkp1  # Обновляем текущую точку
            
            # Обновляем градиент
            gfkp1 = self.fprime(xkp1)  # Новый градиент
            yk = gfkp1 - gfk  # Разница градиентов
            gfk = gfkp1  # Обновляем текущий градиент
            dot_ysk = np.dot(yk, sk)
            
            # Если скалярное произведение слишком мало, избегаем деления на ноль
            if np.abs(dot_ysk) < 1e-10:
                print("Warning: Skalar product is too small, skipping Hessian update")
            else:
            # Обновляем матрицу Гессе (приближенно) с использованием формулы BFGS
                ro = 1.0 / dot_ysk
                A1 = I - ro * np.outer(sk, yk)  # Промежуточная матрица
                A2 = I - ro * np.outer(yk, sk)  # Промежуточная матрица
                Hk = np.dot(A1, np.dot(Hk, A2)) + ro * np.outer(sk, sk)
            
            k += 1  # Увеличиваем счетчик итераций
            self.add_iter(xk, Hk, k)
            
            
        return (xk, self.iterations)  # Возвращаем точку минимума и количество итераций

if __name__=="__main__":
    # Определение целевой функции, которую требуется минимизировать
    def f(x):
        # Функция принимает вектор x и возвращает значение квадратичной функции
        return x[0]**2 - x[0]*x[1] + x[1]**2 + 9*x[0] - 5*x[1] + 20


    # Градиент целевой функции
    def f1(x):
        # Возвращает градиент целевой функции как массив (частные производные по каждой переменной)
        return np.array([2 * x[0] - x[1] + 9, -x[0] + 2*x[1] - 5])
    # Выполняем метод BFGS, начиная с точки [1, 1]
    result, json = BFGS(np.array([1, 1]),f, f1,None,10e-6).bfgs_method()

    # Печатаем результат
    print('Result of BFGS method:')
    print(f'Final Result (best point): {result}')  # Итоговая точка
    print('Iterations:', json)  # Количество итераций