from gurobipy.gurobipy import *

## Example taken from Dr. Ray Jian Zhang: https://www.youtube.com/watch?v=vQzpydNOWDY

fund_returns = [1 + 0.01 * i for i in range(1, 11)]
account_returns = 1.045
number_of_funds = len(fund_returns)

b = [1000] + [100] * number_of_funds
B = [1] + [0] * number_of_funds

y_star = 1500
LB = float('-inf')
UB = float('inf')
epsilon = 0.1

iteration = 0

# Display problem parameters:
print("\n### Problem Parameters ###")
print("Savings Account return: {}".format(account_returns))
print("Fund returns: {} with length {}".format(fund_returns, len(fund_returns)))
print("B: {} with length {}".format(B, len(B)))
print("b: {} with length {}".format(b, len(b)))
print("##########################\n")

def solve_masterproblem(feasibility_cuts, optimality_cuts, iteration):
    print("\n\n### Solving Masterproblem ###")
    model = Model("MasterProblem")
    y = model.addVar(vtype=GRB.INTEGER, lb=0)
    z = model.addVar(vtype=GRB.CONTINUOUS)
    model.setObjective(z, GRB.MAXIMIZE)

    for shadow_prices in feasibility_cuts:
        model.addConstr(quicksum((b[i] - B[i] * y) * shadow_prices[i] for i in range(11)) >= 0)

    for shadow_prices in optimality_cuts:
        model.addConstr(z <= account_returns * y + quicksum((b[i] - B[i] * y) * shadow_prices[i] for i in range(11)))

    model.update()
    model.optimize()
    model.write("master_problem_" + str(iteration) + ".lp")
    return y.X, model.ObjVal


def solve_subproblem(y_star):
    print("\n\n### Solving Subproblem ###")
    model = Model("Subproblem")
    model.setParam("InfUnbdInfo", 1)
    x_i = model.addVars(number_of_funds, vtype=GRB.CONTINUOUS, lb=0, name="fund_i")
    model.addConstr(y_star + quicksum(x_i[i] for i in range(number_of_funds)) <= 1000, name="total_budget")
    model.addConstrs((x_i[i] <= 100 for i in range(number_of_funds)), name="max_amount_for_funds")

    model.setObjective(quicksum(fund_returns[i] * x_i[i] for i in range(number_of_funds)), GRB.MAXIMIZE)
    model.optimize()

    shadow_prices = model.getAttr(GRB.Attr.Pi)

    return shadow_prices, model.status, model.ObjVal


feasibility_cuts = []
optimality_cuts = []

while UB - LB > epsilon:
    iteration += 1

    print("\n# Report of iteration {} #".format(iteration))
    print("Solving subproblem with given y_star: {}".format(y_star))

    shadow_prices, subproblem_status, obj_value_sp = solve_subproblem(y_star)

    print("Dual variables:")
    print(shadow_prices)
    print("")

    if subproblem_status == 3:
        # subproblem primal infeasible, dual unbounded --> add feasibility cut
        feasibility_cuts.append(shadow_prices)

    elif subproblem_status == 2:
        # Careful: LB in example calculated via shadow prices. Should not matter.
        LB = max(LB, account_returns * y_star + obj_value_sp)
        optimality_cuts.append(shadow_prices)

    else:
        print("problem with subproblem status")

    print("\nSolving subproblem with provided y_star of {} results in lower bound: {}".format(y_star, LB))

    y_star, UB = solve_masterproblem(feasibility_cuts, optimality_cuts, iteration)

    print("\nSolved master problem with newly added cuts. New upper bound: {}\n".format(UB))

print("-----------------")
print("\n final amount in savings account: {}".format(y_star))
