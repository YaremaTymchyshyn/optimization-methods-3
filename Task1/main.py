import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve


# Визначення нерівностей
inequalities = [
    lambda x1, x2: x1 - x2 - 1 <= 0,
    lambda x1, x2: x1 + x2 - 2 <= 0,
    lambda x1, x2: x1 - (2 * x2) >= 0,
    lambda x1, x2: (2 * x1) + (2 * x2) - 1 >= 0
]


# Побудова графіків нерівностей
x = np.linspace(-3, 3, 400)
y = np.linspace(-3, 3, 400)
X, Y = np.meshgrid(x, y)
region = np.zeros_like(X, dtype=bool)


for ineq in inequalities:
    region = np.logical_and(region, ineq(X, Y))

plt.figure(figsize=(8, 6))

plt.plot(x, x - 1, label='x1 - x2 <= 1', color='red')
plt.plot(x, 2 - x, label='x1 + x2 <= 2', color='green')
plt.plot(x, x / 2, label='x1 - 2*x2 >= 0', color='blue')
plt.plot(x, (1 - 2 * x) / 2, label='2*x1 + 2*x2 >= 1', color='purple')

plt.fill_between(x, x - 1, -3, where=(x - 1 >= -3), alpha=0.1, color='red')
plt.fill_between(x, 2 - x, -3, where=(2 - x >= -3), alpha=0.1, color='green')
plt.fill_between(x, -3, x / 2, where=(x / 2 >= -3), alpha=0.1, color='blue')
plt.fill_between(x, (1 - 2 * x) / 2, -3, where=((1 - 2 * x) / 2 >= -3), alpha=0.1, color='purple')


# Знаходження точок перетину
x1, x2 = symbols('x1 x2')

eq1 = Eq(x1 - x2, 1)
eq2 = Eq(x1 + x2, 2)
eq3 = Eq(x1 - 2 * x2, 0)
eq4 = Eq(2 * x1 + 2 * x2, 1)

points = {}
points['A'] = solve((eq3, eq4), (x1, x2))
points['B'] = solve((eq2, eq3), (x1, x2))
points['C'] = solve((eq1, eq2), (x1, x2))
points['D'] = solve((eq1, eq4), (x1, x2))

intersection = {}
for name, solution in points.items():
    if solution:
        x1_value = solution[x1]
        x2_value = solution[x2]
        intersection[name] = (float(x1_value.evalf()), float(x2_value.evalf()))
    else:
        print(f"No solution found for point {name}.")

print("Intersection points:", intersection)


# Побудова точок перетину
for name, point in intersection.items():
    plt.scatter(*point, color='k')
    plt.text(point[0] + 0.1, point[1] + 0.1, name, fontsize=12)

sorted_names = ['A', 'B', 'C', 'D']
sorted_points = [intersection[name] for name in sorted_names]
sorted_x = [point[0] for point in sorted_points]
sorted_y = [point[1] for point in sorted_points]
plt.plot(sorted_x + [sorted_x[0]], sorted_y + [sorted_y[0]], color='k', linestyle='-', linewidth=3)


# Система координат та градієнт
plt.axhline(0, color='black', linewidth=0.5)  # Horizontal line for x-axis
plt.axvline(0, color='black', linewidth=0.5)  # Vertical line for y-axis
plt.arrow(0, 0, 1, -2, head_width=0.1, head_length=0.1, fc='k', ec='k')


# Визначення цільової функції
def objective_function(x1, x2):
    return x1 - 2 * x2


# Обчислення значення цільової функції в кожній точці перетину
values = {name: objective_function(point[0], point[1]) for name, point in intersection.items()}


# Знаходження усіх точок з мінімальним значенням
min_value = min(values.values())
min_points = [point for point, value in values.items() if value == min_value]
print("Minimum value:", min_value)
print("Points achieving the minimum value:", min_points)


# Знаходження усіх точок з максимальним значенням
max_value = max(values.values())
max_points = [point for point, value in values.items() if value == max_value]
print("Maximum value:", max_value)
print("Points achieving the maximum value:", max_points)


# Побудова графа
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Linear Programming Problem')
plt.xlim(-3, 3)
plt.ylim(-3, 3)
plt.legend()
plt.grid(True)
plt.show()
