# Process Querying in Notation3 (PQN)

This repository contains the [Notation3 (N3)](http://notation3.org) implementation of the Process Querying in N3 (PQN) language.
The goal of this language is to query process traces in order to make sense of an event log before process mining.

- The [pqn.n3](pqn.n3) file contains the current N3 implementation of PQN.
- The [queries/constraints](queries/constraints) folder contains test queries for the individual PQN constraints on the sepsis event log [1].
- The [convert_log.py](convert/convert_log.py) script converts an event log (XES format) into an equivalent RDF format. See [convert_log.ipynb](convert/convert_log.ipynb) for an example on how to call this script. These scripts rely on the `rdflib` and `pm4py` dependencies, among others.

To run an individual test query (such as `q1.n3`) on the full sepsis event log, run the following command:
```
./run.sh -q queries/constraints/q1.n3 -l logs/sepsis_all.n3
```

To run all test queries (e.g., on 10% of the sepsis event log), run the following command:
```
./run_all.sh -d queries/constraints -l logs/sepsis_10.n3 -r results/times_10.csv
```

You can run `./run.sh -h` and `./run_all.sh -h` for details on the usage of each shell script.
Note that the output of each query will show up under the `out/` folder.

# References
[1] Mannhardt, F., Blinde, D.: Analyzing the Trajectories of Patients with Sepsis using Process Mining. In: RADAR+ EMISA@ CAiSE. pp. 72–80 (2017).