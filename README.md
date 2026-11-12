### Fleet Assignment Model: 
Reassigns aircraft types to JFK routes to minimize operating cost under a CO2 cap,
then sweeps the required CO2 reduction (alpha) from 0% to 3%.

### Setup

Need Python 3.9 or newer.

**Mac / Linux**
```
cd fleet_assignment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```
cd fleet_assignment
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```
python src/main.py
```

### Expected output

Current: cost = $4,024,633, CO2 = 5,619,090 kg, then one block per alpha.
alpha = 2.5% and 3.0% are infeasible with the current fleet.
