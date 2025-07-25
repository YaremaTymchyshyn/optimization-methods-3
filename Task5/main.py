import random
import sympy
from sympy import *
from scipy.optimize import minimize_scalar
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

df = diff(f, x)
critical_points = solve(df, x)
boundary_points = res
values = [df.subs(x, x_val) for x_val in critical_points + boundary_points]
maximum_value = max(values)
minimum_value = min(values)
x0 = 0#random.randint(a, b)
L = max(abs(maximum_value), abs(minimum_value))

r_i = f.subs(x, x0) - L * abs(x - x0)
r0 = lambdify(x, r_i, 'numpy')
res = minimize_scalar(lambda x: r0(x), bounds=(a, b), method='bounded')
xk = res.x
if abs(r_i.subs(x, xk) - f.subs(x, xk)) > e:
    while abs(r_i.subs(x, xk) - f.subs(x, xk)) > e:
        qk = f.subs(x, xk) - L * abs(x - xk)
        r_i = sympy.Max(r_i, qk)
        r_i_k = lambdify(x, r_i, 'numpy')


        x_values = np.linspace(-3, 1, 1000)
        y_values = f_np(x_values)
        plt.plot(x_values, y_values)
        y_values = r_i_k(x_values)
        plt.plot(x_values, y_values)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.show()

        res = minimize_scalar(lambda x: r_i_k(x), bounds=(a, b), method='bounded')
        xk = res.x
