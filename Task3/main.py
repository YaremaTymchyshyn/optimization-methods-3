import numpy as np
from scipy.optimize import linprog

c = [-1, 4, 1]
A = [[3, 4, 1], [1, 2, 1], [0, 0, 1]]
b = [7, 6, 4]

t_a = np.array(A).T
t_b = np.array(b)
t_c = np.array(c)

result = linprog(t_b, A_ub=-t_a, b_ub=-t_c, method='highs')

if result.success:
    print('y1 =', round(result.x[0], 2), '\ny2 =', round(result.x[1], 2), '\ny3 =', round(result.x[1], 2))
    print('F(y) =', int(-result.fun))
else:
    print('Функція необмежена')
