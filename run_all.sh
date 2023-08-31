#!/bin/bash

usage="usage:
run_all.sh -d <dir> -l <log> -r <results> -n <runs> -p <pqn>
where
    -d <dir> is the directory with query files
    -l <log> is the event log
    -r <results> is the results file to write to
    -n <runs> is the number of runs
    -p <pqn> is the PQN implementation"

while getopts "d:l:r:n:p:" option; do
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
        n | runs)
            runs=${OPTARG}
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

echo -e "using $pqn\n"

echo "query,networking,reasoning" > $results 

time_rx='.*networking ([^ ]+).*reasoning ([^ ]+).*'
for path in "$dir"/*; do
    query="${path##*/}"
    echo $query
    echo ""

    total_netw_time=0
    total_reas_time=0
    for ((i=1;i<=runs;i++)); do
        echo "run $i"

        error=$( { eye $pqn --turtle $log --query $path --nope > out/$query; } 2>&1 )
        # echo $error
        
        [[ $error =~ $time_rx ]]
        run_netw_time=${BASH_REMATCH[1]}
        run_reas_time=${BASH_REMATCH[2]}
        echo "networking: $run_netw_time, reasoning: $run_reas_time"

        ((total_netw_time+=run_netw_time))
        ((total_reas_time+=run_reas_time))
    done

    ((avg_netw_time=total_netw_time/runs))
    ((avg_reas_time=total_reas_time/runs))

    echo "$query,$avg_netw_time,$avg_reas_time" >> $results
        
    echo -e "\navg. networking: $avg_netw_time, avg. reasoning: $avg_reas_time\n\n"
done