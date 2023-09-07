# Process Querying in Notation3 (PQN)

## Improved Querying Times

Due to significant optimizations of the PQN implementation, we can report much faster query execution times (on the full sepsis log) than currently reported in the PODS4H submission:

| Query                                       | Execution Time (ms) |
|---------------------------------------------|---------------------|
| pq:activitiesCoOccurOrNoneOccurs (q23.n3)   | 43                  |
| pq:activitiesDoNotCoOccur (q24.n3)          | 49                  |
| pq:allActivitiesOccurAtLeastNTimes (q5.n3)  | 26                  |
| pq:activityDoesNotOccur (q22.n3)            | 52                  |
| pq:activityOccursAtLeastNTimes (q2.n3)      | 22                  |
| pq:allActivitiesOccur (q3.n3)               | 41                  |

All times are averaged over 10 runs. All query execution times for all event logs can be found in the [`results/`](results/) folder.

By further optimizing the loading of the RDF log, we can also report `121ms`, `244ms`, and `507ms` loading times for 25%, 50%, and 100% of the sepsis event log [1], respectively.

We refer to instructions below to reproduce our experiments.

## Instructions

This repository contains the [Notation3 (N3)](http://notation3.org) implementation of the Process Querying in N3 (PQN) language.
The goal of this language is to query process traces in order to make sense of an event log before process mining.

- The [pqn.n3](pqn.n3) file contains the current N3 implementation of PQN.
- The [queries/constraints](queries/constraints) folder contains test queries for the individual PQN constraints on the sepsis event log [1].
- The [convert_log.py](convert/convert_log.py) script converts an event log (XES format) into an equivalent RDF format. See [convert_log.ipynb](convert/convert_log.ipynb) for an example on how to call this script. These scripts rely on the `pm4py` and `pandas` dependency, among others.

First, install the latest version of the [`eye`](https://github.com/eyereasoner/eye/tags) reasoner (the experiments were performed with v.4.14.12).

You can run `./test.sh -h`, `./run.sh -h` and `./run_all.sh -h` for details on the usage of each shell script.

### Test single query

To test an individual query using eye on the full sepsis event log, run the following command:
```
./test.sh -t eye -q queries/sepsis_multi.n3 -l logs/sepsis_reif_all.n3 -p pqn_reif.n3
```

To do the same using a pre-compiled `pvm` image (see below):
```
./test.sh -t pvm -q queries/sepsis_multi.n3 -l logs/sepsis_reif_all.n3 -p pqn_reif.pvm
```

### Measure performance of single query

To measure the performance of an individual test query using eye on the full sepsis event log, run the following command:
```
./run.sh -t eye -q queries/sepsis_multi.n3 -l logs/sepsis_reif_all.n3 -r results/eye/times_reif_all.csv  -n 10 -p pqn_reif.n3
```

To do the same using a pre-compiled `pvm` image (see below):
```
./run.sh -t pvm -q queries/sepsis_multi.n3 -l logs/sepsis_reif_all.n3 -r results/pvm/times_reif_all.csv  -n 10 -p pqn_reif.pvm
```

Where result times will appear in `results/times_all.csv` for this example, and times will be averaged over 10 runs. Query outputs will appear in the `out/` folder.


### Measure performance of a directory of queries

To measure the performance of all test queries using eye on the full sepsis event log, run the following command:
```
./run_all.sh -t eye -d queries/constraints -l logs/sepsis_reif_all.n3 -r results/eye/times_reif_all.csv -n 10 -p pqn_reif.n3
```

To do the same using a pre-compiled `pvm` image (see below):
```
./run_all.sh -t pvm -d queries/constraints -l logs/sepsis_reif_all.n3 -r results/pvm/times_reif_all.csv -n 10 -p pqn_reif.pvm
```


### Pre-compiling a PVM image

To pre-compile a `pvm` image:
```
eye pqn_reif.n3 --turtle logs/sepsis_reif_all.n3 --image pqn_reif.pvm
```

To directly run a `pvm` image:
```
swipl -x pqn_reif.pvm -- --query queries/sepsis_multi.n3 --nope 
```


# References
[1] Mannhardt, F., Blinde, D.: Analyzing the Trajectories of Patients with Sepsis using Process Mining. In: RADAR+ EMISA@ CAiSE. pp. 72–80 (2017).
