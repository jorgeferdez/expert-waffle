from ortools.linear_solver import pywraplp


def solve(weights, bin_capacity):
    data = {}
    data["weights"] = weights
    data["items"] = list(range(len(weights)))
    data["bins"] = data["items"]
    data["bin_capacity"] = bin_capacity

    solver = pywraplp.Solver.CreateSolver("SCIP")

    if not solver:
        raise RuntimeError("SCIP solver is not available. Please check your installation.")

    x = {}
    for i in data["items"]:
        for j in data["bins"]:
            x[(i, j)] = solver.IntVar(0, 1, "x_%i_%i" % (i, j))

    y = {}
    for j in data["bins"]:
        y[j] = solver.IntVar(0, 1, "y[%i]" % j)

    for i in data["items"]:
        solver.Add(sum(x[i, j] for j in data["bins"]) == 1)

    for j in data["bins"]:
        solver.Add(sum(x[(i, j)] * data["weights"][i] for i in data["items"]) <= y[j] * data["bin_capacity"])

    solver.Minimize(solver.Sum([y[j] for j in data["bins"]]))
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        packed = []
        num_bins = 0
        for j in data["bins"]:
            if y[j].solution_value() == 1:
                bin_items = []
                bin_weight = 0
                for i in data["items"]:
                    if x[i, j].solution_value() > 0:
                        bin_items.append(data["weights"][i])
                        bin_weight += data["weights"][i]
                if bin_items:
                    num_bins += 1
                    packed.append([bin_items, bin_weight])
        return num_bins, packed, None
    else:
        return 0, [], "The problem does not have an optimal solution."


def _main():
    num_bins, packed, error_message = solve([40, 40, 30, 30, 30, 27], 100)
    if (error_message):
        print(error_message)
        return

    print(num_bins, packed)


if __name__ == "__main__":
    _main()
