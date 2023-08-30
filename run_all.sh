#!/bin/bash

usage="usage:
run_all.sh -d <dir> -l <log> -r <results> [ -q <pqn> ]
where
    -d <dir> is the directory with query files
    -l <log> is the event log
    -r <results> is the results file to write to
    -p <pqn> is the PQN implementation"

while getopts "d:l:r:" option; do
    case "${option}" in
        d | dir)
            dir=${OPTARG}
        ;;
        l | log)
            log=${OPTARG}
        ;;
        r | results)
            results=${OPTARG}
        ;;
        p | pqn)
            pqn=${OPTARG}
        ;;
        *)
            echo "$usage"
            exit 1
        ;;
    esac
done

if [ -z "$dir" ] || [ -z "$log" ] || [ -z "$results" ]; then
    echo "$usage"
    exit 1
fi

if [[ -z "$pqn" ]]; then
    pqn="pqn.n3"
fi

echo "query,networking,reasoning" > $results 

time_rx='.*networking ([^ ]+).*reasoning ([^ ]+).*'
for path in "$dir"/*; do
    query="${path##*/}"
    echo $query

    error=$( { eye $pqn $log --query $path --nope > out/$query; } 2>&1 )
    # echo $error
    
    [[ $error =~ $time_rx ]]
    netw_time=${BASH_REMATCH[1]}
    reas_time=${BASH_REMATCH[2]}

    echo "$query,$netw_time,$reas_time" >> $results
    
    echo "networking: $netw_time, reasoning: $reas_time"
    echo ""
done