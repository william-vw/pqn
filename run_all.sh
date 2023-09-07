#!/bin/bash

usage="usage:
run_all.sh -t <type> -d <dir> -l <log> -r <results> -n <runs> -p <pqn>
where
    -t <type> is the run type (eye or pvm)
    -d <dir> is the directory with query files
    -l <log> is the event log
    -r <results> is the results file to write to
    -n <runs> is the number of runs
    -p <pqn> is the PQN implementation"

while getopts "t:d:l:r:n:p:" option; do
    case "${option}" in
        t | type)
            type=${OPTARG}
        ;;
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

if [ $type != "eye" ] && [ $type != "pvm" ]; then
    echo "use 'eye' or 'pvm' for type parameter"
    exit 1
fi

if [[ -z "$pqn" ]]; then
    pqn="pqn.n3"
fi

echo -e "using $pqn\n"

echo "query,startup,networking,reasoning" > $results 

time_rx='.*starting ([^ ]+).*networking ([^ ]+).*reasoning ([^ ]+).*'
for path in "$dir"/*; do
    query="${path##*/}"
    echo $query
    echo ""

    total_strt_time=0
    total_netw_time=0
    total_reas_time=0
    for ((i=1;i<=runs;i++)); do
        echo "run $i"

        if [ $type == 'eye' ]; then
            error=$( { eye $pqn --turtle $log --query $path --nope > out/$query; } 2>&1 )
        elif [ $type == 'pvm' ]; then
            error=$( { swipl -x $pqn -- --query $path --nope > out/$query; } 2>&1 )
        fi
        # echo $error
        
        [[ $error =~ $time_rx ]]
        run_strt_time=${BASH_REMATCH[1]}
        run_netw_time=${BASH_REMATCH[2]}
        run_reas_time=${BASH_REMATCH[3]}
        echo "starting: $run_strt_time, networking: $run_netw_time, reasoning: $run_reas_time"

        ((total_strt_time+=run_strt_time))
        ((total_netw_time+=run_netw_time))
        ((total_reas_time+=run_reas_time))
    done
    ((avg_strt_time=total_strt_time/runs))
    ((avg_netw_time=total_netw_time/runs))
    ((avg_reas_time=total_reas_time/runs))

    echo "$query,$avg_strt_time,$avg_netw_time,$avg_reas_time" >> $results
        
    echo -e "\navg. starting: $avg_strt_time, avg. networking: $avg_netw_time, avg. reasoning: $avg_reas_time\n\n"
done