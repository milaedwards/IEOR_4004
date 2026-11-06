# runs baseline check and the alpha sweep, then saves to results

from gurobipy import GRB
from variables import load_params
from model import solve

p = load_params()

for alpha in [0, 0.05, 0.10, 0.15, 0.20]:
    m, x = solve(p, alpha)

    if m.Status != GRB.OPTIMAL:
        print(f"alpha = {alpha:.0%}: infeasible")
        continue

    print(f"\nalpha = {alpha:.0%}: total cost = ${m.ObjVal:,.0f}")
    for (r, k), var in x.items():
        if var.X > 0.5:
            print(f"   {r}: {int(var.X)} round trips on {k}")