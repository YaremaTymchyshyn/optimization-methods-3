import random
import sympy
from sympy import *
import numpy as np
import matplotlib.pyplot as plt


def sven(f, x, x0, h):
    x1 = x0 + h
    f0 = f.subs(x, x0)
    f1 = f.subs(x, x1)
    if f1 > f0:
        h = -h
        x1 = x0 + h
        f1 = f.subs(x, x1)
    while f1 < f0:
        h = h*2
        x2 = x1 + h
        f2 = f.subs(x, x2)
        f0 = f1
        f1 = f2
    return [x1, x2]

e = 0.001
x = symbols('x')
f = x**2 + 5*x + 4
f_np = lambdify(x, f, "numpy")

not_sorted = sven(f, x, 3, 2)
not_sorted.sort()
res = not_sorted
a, b = res[0], res[1]
a1, b1 = a, b
df = diff(f, x)
f_a = df.subs(x, a)
f_b = df.subs(x, b)

if (1/2)*(b1-a1) >= e:
    y1 = f.subs(x, a1) + f_a * (x - a1)
    y2 = f.subs(x, b1) + f_b * (x - b1)
    y_f = lambdify(x, sympy.Max(y1, y2), 'numpy')

    x_values = np.linspace(-3, 1, 1000)
    y_values = f_np(x_values)
    plt.plot(x_values, y_values)
    y_values = y_f(x_values)
    plt.plot(x_values, y_values)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.show()

    x_ = sympy.solve(y1-y2, x)[0]
    f_x = df.subs(x, x_)
    if f_x > 0:
        b1 = x_
    elif f_x < 0:
        a1 = x_
    while  (1/2)*(b1-a1) >= e and f_x != 0:
        f_a = df.subs(x, a1)
        f_b = df.subs(x, b1)
        y1 = f.subs(x, a1) + f_a * (x - a1)
        y2 = f.subs(x, b1) + f_b * (x - b1)
        y_f = lambdify(x, sympy.Max(y1, y2), 'numpy')

        y_values = f_np(x_values)
        plt.plot(x_values, y_values)
        y_values = y_f(x_values)
        plt.plot(x_values, y_values)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.show()

        x_ = sympy.solve(y1 - y2, x)[0]
        f_x = df.subs(x, x_)
        if f_x > 0:
            b1 = x_
        elif f_x < 0:
            a1 = x_