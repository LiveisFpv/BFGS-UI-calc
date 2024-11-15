# -*- coding: utf-8 -*-
import numpy as np  # Импорт библиотеки для работы с массивами и матрицами
import numpy.linalg as ln  # Подмодуль для вычислений, связанных с линейной алгеброй
import scipy as sp  # Импорт библиотеки SciPy для оптимизации и других научных расчетов


# Определение целевой функции, которую требуется минимизировать
def f(x):
    # Функция принимает вектор x и возвращает значение квадратичной функции
    return x[0]**2 - x[0]*x[1] + x[1]**2 + 9*x[0] - 5*x[1] + 20


# Градиент целевой функции
def f1(x):
    # Возвращает градиент целевой функции как массив (частные производные по каждой переменной)
    return np.array([2 * x[0] - x[1] + 9, -x[0] + 2*x[1] - 5])


# Реализация метода BFGS для минимизации функции
def bfgs_method(f, fprime, x0, maxiter=None, epsi=10e-3):
    """
    Минимизация функции f(x) методом BFGS.

    Параметры
    ----------
    f : function
        Целевая функция для минимизации.
    fprime : function
        Градиент целевой функции.
    x0 : ndarray
        Начальная точка.
    maxiter : int, optional
        Максимальное число итераций (по умолчанию зависит от размерности задачи).
    epsi : float, optional
        Критерий остановки по норме градиента (по умолчанию 10e-3).
    """
    
    if maxiter is None:
        # Если максимальное число итераций не указано, то задаем значение
        maxiter = len(x0) * 200

    # Начальные значения
    k = 0  # Номер итерации
    gfk = fprime(x0)  # Градиент функции в начальной точке
    N = len(x0)  # Размерность задачи
    I = np.eye(N, dtype=int)  # Единичная матрица
    Hk = I  # Начальная матрица Гессе (приближение)
    xk = x0  # Текущая точка
   
    # Основной цикл оптимизации
    while ln.norm(gfk) > epsi and k < maxiter:  # Условие остановки: градиент мал или достигнут лимит итераций
        
        # pk - направление поиска, определяется как -Hk * gfk
        pk = -np.dot(Hk, gfk)
        
        # Выполняем линейный поиск для нахождения шага alpha_k
        line_search = sp.optimize.line_search(f, f1, xk, pk)
        alpha_k = line_search[0]  # Берем только значение alpha_k
        
        # Обновляем текущую точку xk
        xkp1 = xk + alpha_k * pk  # Новая точка
        sk = xkp1 - xk  # Вектор изменения точки
        xk = xkp1  # Обновляем текущую точку
        
        # Обновляем градиент
        gfkp1 = fprime(xkp1)  # Новый градиент
        yk = gfkp1 - gfk  # Разница градиентов
        gfk = gfkp1  # Обновляем текущий градиент
        
        # Обновляем матрицу Гессе (приближенно) с использованием формулы BFGS
        ro = 1.0 / (np.dot(yk, sk))  # Скейлящий множитель
        A1 = I - ro * sk[:, np.newaxis] * yk[np.newaxis, :]  # Промежуточная матрица
        A2 = I - ro * yk[:, np.newaxis] * sk[np.newaxis, :]  # Промежуточная матрица
        Hk = np.dot(A1, np.dot(Hk, A2)) + (ro * sk[:, np.newaxis] * sk[np.newaxis, :])
        
        k += 1  # Увеличиваем счетчик итераций
        
    return (xk, k)  # Возвращаем точку минимума и количество итераций


# Выполняем метод BFGS, начиная с точки [1, 1]
result, k = bfgs_method(f, f1, np.array([1, 1]))

# Печатаем результат
print('Result of BFGS method:')
print('Final Result (best point): %s' % (result))  # Итоговая точка
print('Iteration Count: %s' % (k))  # Количество итераций