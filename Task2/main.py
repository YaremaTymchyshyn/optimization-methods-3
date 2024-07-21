from scipy.optimize import linprog


def solve_linear_program(c, A_eq=None, b_eq=None, A_ub=None, b_ub=None):
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, method='highs')
    return res.x, res.fun


# Problem 1
c1 = [1, -1, 1, 2]
A_eq1 = [[1, 1, 1, 2], [0, 1, 1, 1], [0, 0, 1, -1]]
b_eq1 = [7, 5, 3]
x1, min1 = solve_linear_program(c1, A_eq1, b_eq1)
print("Problem 1 solution:")
print("x1 =", int(x1[0]), ", x2 =", int(x1[1]), ", x3 =", int(x1[2]), ", x4 =", int(x1[3]), ", min =", int(min1))

# Problem 2
c2 = [-1, 5, 1, -1]
A_eq2 = [[1, 3, 3, 1]]
b_eq2 = [3]
A_ub2 = [[-2, 0, -3, 1]]
b_ub2 = [-4]
x2, min2 = solve_linear_program(c2, A_eq2, b_eq2, A_ub2, b_ub2)
print("\nProblem 2 solution:")
print("x1 =", int(x2[0]), ", x2 =", int(x2[1]), ", x3 =", int(x2[2]), ", x4 =", int(x2[3]), ", min =", int(min2))
