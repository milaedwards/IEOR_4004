# creates decision variables, objective function, and constraints

import gurobipy as gp
from gurobipy import GRB


def solve(p, alpha):
    R, K = p["R"], p["K"]
    m = gp.Model("fleet_assignment")

    # Decision variable: x[r,k] = number of round trips on route r by aircraft type k
    x = m.addVars(R, K, vtype=GRB.INTEGER, lb=0, name="x")

    # Objective Function
    m.setObjective(gp.quicksum(p["c"][r, k] * x[r, k] for r in R for k in K), GRB.MINIMIZE)

    # Every flight must be assigned an aircraft
    for r in R:
        m.addConstr(gp.quicksum(x[r, k] for k in K) == p["n"][r])

    # CO2 emissions limit: optimized aircraft assignments must produce less CO2 than current assignments
    m.addConstr(gp.quicksum(p["E"][r, k] * x[r, k] for r in R for k in K)
                <= (1 - alpha) * p["E_base"])

    # The aircraft assigned to each route must have enough seats to accommodate demand
    for r in R:
        m.addConstr(gp.quicksum(p["S"][k] * x[r, k] for k in K) >= p["D"][r])

    # Aircraft range: cannot assign aircraft to a flight that is larger than its max range
    for r in R:
        for k in K:
            if p["d"][r] > p["Range"][k]:
                m.addConstr(x[r, k] == 0)

    # Total flying hours of an aircraft cannot be larger than total hours available
    for k in K:
        m.addConstr(gp.quicksum(p["T"][r, k] * x[r, k] for r in R) <= 1.1 * p["N"][k] * p["U"][k])

    m.optimize()
    return m, x