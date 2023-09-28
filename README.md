# Process Querying in Notation3 (PQN)

## Live Demo

A live demo, using the sepsis event log [1] and a query with multiple constraints, can be found here: [https://n3-editor.herokuapp.com/n3/pqn/s/3NaOtDMR](https://n3-editor.herokuapp.com/n3/pqn/s/3NaOtDMR).

Note that you can try out any other XES event log as well.

## Performance Tests

The [logs](logs) folder contains subsets (25%, 50%, 100%) of the sepsis event log [1]. 
The [queries/constraints](queries/constraints) folder contains test queries for individual PQN constraints on the sepsis log.
We ran performance tests for these test queries on the different log subsets.
The query execution times for all event logs can be found in the [`results/`](results/) folder.
All times are averaged over 10 runs. 

We refer to instructions below to reproduce our experiments.

## Instructions

This repository contains the [Notation3 (N3)](http://notation3.org) implementation of the Process Querying in N3 (PQN) language.
The goal of this language is to query process traces in order to make sense of an event log before process mining.

- The [pqn.n3](pqn.n3) file contains the current N3 implementation of PQN.
- The [queries/constraints](queries/constraints) folder contains test queries for the individual PQN constraints on the sepsis event log [1].
- The [convert_log.py](convert/convert_log.py) script converts an event log (XES format) into an equivalent RDF format. See [convert_log.ipynb](convert/convert_log.ipynb) for an example on how to call this script. These scripts rely on the `pm4py` and `pandas` dependency, among others.

First, install the latest version of the [`eye`](https://github.com/eyereasoner/eye/tags) reasoner (the experiments were performed with v.4.14.12).

To run an individual test query (such as `q1.n3`) on the full sepsis event log, run the following command:
```
./run.sh -q queries/constraints/q1.n3 -l logs/sepsis_all.n3 -p pqn.n3
```

To run all test queries on a particular log (e.g., the [full sepsis event log](logs/)), run the following command:
```
./run_all.sh -d queries/constraints -l logs/sepsis_all.n3 -r results/times_all.csv -n 10 -p pqn.n3
```
Where result times will appear in `results/times_all.csv` for this example, and times will be averaged over 10 runs. Query outputs will appear in the `out/` folder.

You can run `./run.sh -h` and `./run_all.sh -h` for details on the usage of each shell script.

# References
[1] Mannhardt, F., Blinde, D.: Analyzing the Trajectories of Patients with Sepsis using Process Mining. In: RADAR+ EMISA@ CAiSE. pp. 72–80 (2017).
