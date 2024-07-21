import numpy as np


def northwest_corner_method(supply, demand, costs):
    supply_remaining = np.copy(supply)
    demand_remaining = np.copy(demand)
    costs = costs.astype(float)
    volume_of_deliveries = np.zeros(costs.shape, dtype=int)
    total_cost = 0
    row_index = 0
    col_index = 0

    while row_index < len(supply) and col_index < len(demand):
        quantity_transferred = min(supply_remaining[row_index], demand_remaining[col_index])
        volume_of_deliveries[row_index, col_index] = quantity_transferred
        supply_remaining[row_index] -= quantity_transferred
        demand_remaining[col_index] -= quantity_transferred
        total_cost += quantity_transferred * costs[row_index, col_index]
        if supply_remaining[row_index] == 0:
            row_index += 1
        if demand_remaining[col_index] == 0:
            col_index += 1

    return volume_of_deliveries, total_cost


def minimum_cost_method(supply, demand, costs):
    supply_remaining = np.copy(supply)
    demand_remaining = np.copy(demand)
    costs = costs.astype(float)
    volume_of_deliveries = np.zeros(costs.shape, dtype=int)
    total_cost = 0

    while np.sum(supply_remaining) > 0 and np.sum(demand_remaining) > 0:
        min_cost_index = np.unravel_index(np.argmin(costs), costs.shape)
        i, j = min_cost_index
        quantity_transferred = min(supply_remaining[i], demand_remaining[j])
        volume_of_deliveries[i, j] = quantity_transferred
        supply_remaining[i] -= quantity_transferred
        demand_remaining[j] -= quantity_transferred
        total_cost += quantity_transferred * costs[i, j]
        costs[i, j] = 1e9

    return volume_of_deliveries, total_cost


def vogel_approximation_method(supply, demand, costs):
    supply = supply.copy()
    demand = demand.copy()
    costs = costs.astype(float)
    volume_of_deliveries = np.zeros(costs.shape, dtype=int)
    total_cost = 0

    while np.sum(supply) > 0 and np.sum(demand) > 0:
        row_penalty = np.zeros(len(supply))
        col_penalty = np.zeros(len(demand))

        for i in range(len(supply)):
            if supply[i] > 0:
                row_costs = np.sort(costs[i])
                if len(row_costs) > 1:
                    row_penalty[i] = row_costs[1] - row_costs[0]
                else:
                    row_penalty[i] = row_costs[0] if len(row_costs) == 1 else 0

        for j in range(len(demand)):
            if demand[j] > 0:
                col_costs = np.sort(costs[:, j])
                if len(col_costs) > 1:
                    col_penalty[j] = col_costs[1] - col_costs[0]
                else:
                    col_penalty[j] = col_costs[0] if len(col_costs) == 1 else 0

        max_row_penalty_index = np.argmax(row_penalty)
        max_col_penalty_index = np.argmax(col_penalty)

        if row_penalty[max_row_penalty_index] >= col_penalty[max_col_penalty_index]:
            row = max_row_penalty_index
            col = np.argmin(costs[row])
        else:
            col = max_col_penalty_index
            row = np.argmin(costs[:, col])

        quantity_transferred = min(supply[row], demand[col])
        volume_of_deliveries[row, col] = quantity_transferred
        supply[row] -= quantity_transferred
        demand[col] -= quantity_transferred

        total_cost += quantity_transferred * costs[row, col]

        costs[row, col] = np.inf

    return volume_of_deliveries, total_cost


def potentials(costs_or, volume_of_deliveries):
    volume_of_delivery = volume_of_deliveries.copy()
    u = np.full(int(costs_or.size / costs_or[0].size), None)
    v = np.full(costs_or[0].size, None)
    u[0] = 0

    for i in range(u.size):
        for j in range(v.size):
            if volume_of_delivery[i][j] != 0:
                if u[i] is not None:
                    v[j] = costs_or[i][j] - u[i]
                elif v[j] is not None:
                    u[i] = costs_or[i][j] - v[j]
    print(u, v)


def main():
    supply = np.array([30, 40, 20])
    demand = np.array([14, 26, 16, 34])
    costs = np.array([[4, 5, 6, 6], [6, 7, 4, 9], [7, 6, 8, 4]])

    method_choice = input("Виберіть метод (1 - Північно-західний кут, 2 - Мінімальний елемент, 3 - Метод Фогеля): ")

    if method_choice == "1":
        volume_of_deliveries, total_cost = northwest_corner_method(supply, demand, costs)
    elif method_choice == "2":
        volume_of_deliveries, total_cost = minimum_cost_method(supply, demand, costs)
    elif method_choice == "3":
        volume_of_deliveries, total_cost = vogel_approximation_method(supply, demand, costs)
    else:
        print("Ви ввели неправильний варіант методу.")
        return

    print("")
    print("Розв'язок транспортної задачі:")
    print(volume_of_deliveries)
    print("")
    print("Загальна вартість перевезень:", total_cost)
    print("")
    print("Потенціали:")
    potentials(costs, volume_of_deliveries)


if __name__ == "__main__":
    main()
