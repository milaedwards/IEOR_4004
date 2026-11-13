# runs baseline check and the alpha sweep

from gurobipy import GRB
from variables import load_params
from model import solve

p = load_params()
R, K = p["R"], p["K"]
print(f"Current: cost = ${p['cost_base']:,.0f}, CO2 = {p['E_base']:,.0f} kg")

for alpha in [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03]:
    m, x = solve(p, alpha)

    if m.SolCount == 0:
        print(f"\nalpha = {alpha:.1%}: infeasible")
        continue

    emissions = sum(p["E"][r, k] * x[r, k].X for r in R for k in K)
    print(f"\nalpha = {alpha:.1%}: cost = ${m.ObjVal:,.0f} " 
          f"({m.ObjVal / p['cost_base'] - 1:+.1%} vs current), "
          f"CO2 {1 - emissions / p['E_base']:.2%} below current, "
          f"gap {m.MIPGap:.3%}")

    for k in K:
        trips = round(sum(x[r, k].X for r in R))
        hours = sum(p["T"][r, k] * x[r, k].X for r in R)
        cap = 1.1 * p["N"][k] * p["U"][k]
        print(f"   {k:9s}: {trips:3d} trips, {hours:6.1f} of {cap:6.1f} hours")