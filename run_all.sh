#!/bin/bash

pqn="pqn.n3"
log="logs/sepsis.n3"
dir="queries"
times="times.csv"

echo "query,networking,reasoning\n" > $times 

file_rx='.*/(.*)'
time_rx='.*networking ([^ ]+).*reasoning ([^ ]+).*'
for path in "$dir"/*; do
    query="${path##*/}"
    echo $query

    error=$( { eye $pqn $log --query $path --nope > out/$query; } 2>&1 )
    # echo $error
    
    [[ $error =~ $time_rx ]]
    netw_time=${BASH_REMATCH[1]}
    reas_time=${BASH_REMATCH[2]}

    echo "$query,$netw_time,$reas_time" >> $times
    
    echo "networking: $netw_time, reasoning: $reas_time"
    echo ""
done