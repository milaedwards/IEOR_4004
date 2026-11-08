
from pathlib import Path
import pandas as pd


def load_params():
    data_folder = Path(__file__).resolve().parent.parent / "data"

    summary = pd.read_csv(data_folder / "summary.csv", skiprows=2)
    costs = pd.read_csv(data_folder / "route_costs.csv", skiprows=2)

    # Routes and aircraft types
    summary = summary[summary["route (r)"].str.startswith("JFK-")].copy()

    R = summary["route (r)"].tolist()
    K = ["A220-300", "A320", "A321", "A321neo"]

    # Number of round trips and distance for each route
    n = dict(zip(R, summary.iloc[:, 2].astype(int)))
    d = dict(zip(R, summary.iloc[:, 1].astype(float)))

    # Aircraft parameters
    N = {}
    Range = {}
    U = {}
    S = {}

    for i, k in enumerate(K):
        row = summary.iloc[i]

        N[k] = int(row.iloc[12])
        Range[k] = float(row.iloc[13])
        U[k] = float(row.iloc[14])
        S[k] = float(row.iloc[20])

    # Original aircraft assignments
    x0 = {}

    for _, row in summary.iterrows():
        r = row.iloc[0]

        for i, k in enumerate(K):
            x0[r, k] = int(row.iloc[3 + i])

    # Passenger demand from column AY
    D = dict(zip(R, summary.iloc[:, 50].astype(float)))

    # Flight time, operating cost and CO2 emissions
    T = {}
    c = {}
    E = {}

    for _, row in costs.iterrows():
        r = row.iloc[0]

        for i, k in enumerate(K):
            T[r, k] = float(row.iloc[1])
            E[r, k] = float(row.iloc[7 + i])
            c[r, k] = float(row.iloc[12 + i])

    # Check that the routes match in both files
    if set(R) != set(costs["route (r)"]):
        raise ValueError("Routes do not match between CSV files")

    # Baseline CO2 emissions
    E_base = sum(
        x0[r, k] * E[r, k]
        for r in R
        for k in K
    )

    return {
        "R": R,
        "K": K,
        "n": n,
        "D": D,
        "d": d,
        "S": S,
        "Range": Range,
        "N": N,
        "U": U,
        "T": T,
        "c": c,
        "E": E,
        "E_base": E_base
    }


