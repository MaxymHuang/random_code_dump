from pulp import *

# Declare lp problem
lp_problem = LpProblem('HW5_Problem_2', LpMinimize)

# Create variables
months = 12

Hire = LpVariable.dicts("H", list(range(months + 1)), 0, cat="Continuous")
Fire = LpVariable.dicts("F", list(range(months + 1)), 0, cat="Continuous")
Inventory = LpVariable.dicts("I", list(range(months + 1)), 0, cat="Continuous")
Production = LpVariable.dicts("P", list(range(months + 1)), 0, cat="Continuous")
Shortage = LpVariable.dicts("S", list(range(months + 1)), 0, cat="Continuous")
Workforcelvl = LpVariable.dicts("W", list(range(months + 1)), 0, cat="Continuous")

num_workday = 20
Demand = [144000000, 134000000, 123600000, 144000000, 108000000, 72000000, 72000000, 72000000, 120000000, 108000000, 144000000, 144000000]


# State the Lp problem
lp_problem += lpSum(320*Hire[t] + 600*Fire[t] + 0.5*Inventory[t] + 4*Production[t] + 4.2*Shortage[t] for t in range(1, months))
    
    

# Subject to constraints
lp_problem += Workforcelvl[0] == 64000
lp_problem += Inventory[0] == 1000000
lp_problem += Inventory[months] >= 24000000

for t in range(1, months+1):
    lp_problem += Workforcelvl[t] == Workforcelvl[t-1] + Hire[t] - Fire[t]
    lp_problem += Inventory[t] == Inventory[t-1] + Production[t] + Shortage[t] - Demand[t-1]
    lp_problem += Production[t] == (8 * 12) * num_workday * Workforcelvl[t]

# solving the LP
lp_problem.solve()

print(lp_problem)
for v in lp_problem.variables():
    print(v.name, "=", v.varValue)

print("Optimized Value =", pulp.value(lp_problem.objective))
print("Status:", LpStatus[lp_problem.status])
