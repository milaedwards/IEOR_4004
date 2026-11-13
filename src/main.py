# runs baseline check and the alpha sweep

from pathlib import Path
import pandas as pd
from variables import load_params
from model import solve

p = load_params()
R, K = p["R"], p["K"]
print(f"Current: cost = ${p['cost_base']:,.0f}, CO2 = {p['E_base']:,.0f} kg")

rows = []

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

    # Route-level assignments: print only the ones that changed, save all of them
    print("   Changes vs current (route, type: current -> optimized):")
    for r in R:
        for k in K:
            new, old = round(x[r, k].X), p["x0"][r, k]
            rows.append({"alpha": alpha, "route": r, "type": k,
                        "current": old, "optimized": new})
            if new != old:
                print(f"      {r} {k}: {old} -> {new}")

out = Path(__file__).resolve().parent.parent / "results" / "assignments.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(f"\nSaved {out}")