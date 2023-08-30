# Process Querying in Notation3 (PQN)

## Updated Querying Times

Due to significant optimizations of the underlying PQN implementation, we can report much faster query execution times than currently reported in the PODS4H submission:

| Query                                       | Execution Time (ms) | 
|---------------------------------------------|---------------------|
| pq:activitiesCoOccurOrNoneOccurs (q15.n3)   | 47                  |
| pq:activitiesDoNotCoOccur (q16.n3)          | 50                  |
| pq:allActivitiesOccurAtLeastNTimes (q5.n3)  | 39                  |
| pq:activityDoesNotOccur (q14.n3)            | 56                  |
| pq:activityOccursAtLeastNTimes (q2.n3)      | 21                  |
| pq:allActivitiesOccur (q3.n3)               | 32                  |

We refer to instructions below to reproduce our experiments.

## Instructions

This repository contains the [Notation3 (N3)](http://notation3.org) implementation of the Process Querying in N3 (PQN) language.
The goal of this language is to query process traces in order to make sense of an event log before process mining.

- The [pqn.n3](pqn.n3) file contains the current N3 implementation of PQN.
- The [queries/constraints](queries/constraints) folder contains test queries for the individual PQN constraints on the sepsis event log [1].
- The [convert_log.py](convert/convert_log.py) script converts an event log (XES format) into an equivalent RDF format. See [convert_log.ipynb](convert/convert_log.ipynb) for an example on how to call this script. These scripts rely on the `rdflib` and `pm4py` dependencies, among others.

To run an individual test query (such as `q1.n3`) on the full sepsis event log, run the following command:
```
./run.sh -q queries/constraints/q1.n3 -l logs/sepsis_all.n3
```

To run all test queries on a particular log (e.g., the [full sepsis event log](logs/)), run the following command:
```
./run_all.sh -d queries/constraints -l logs/sepsis_all.n3 -r results/times_all.csv
```
Where the query outputs will appear in the `out/` folder, and result times will appear in `results/times_all.csv` for this example.

You can run `./run.sh -h` and `./run_all.sh -h` for details on the usage of each shell script.
Note that the output of each query will show up under the `out/` folder.

# References
[1] Mannhardt, F., Blinde, D.: Analyzing the Trajectories of Patients with Sepsis using Process Mining. In: RADAR+ EMISA@ CAiSE. pp. 72–80 (2017).
