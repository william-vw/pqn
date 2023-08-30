#!/bin/bash

usage="usage:
run.sh -q <query> -l <log> [ -q <pqn> ]
where
    -q <query> is the query over the event log
    -l <log> is the event log
    -p <pqn> is the PQN implementation"

while getopts "q:l:p:" option; do
    case "${option}" in
        q | query)
            query=${OPTARG}
        ;;
        l | log)
            log=${OPTARG}
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

if [ -z "$query" ] || [ -z "$log" ]; then
    echo "$usage"
    exit 1
fi

if [[ -z "$pqn" ]]; then
    pqn="pqn.n3"
fi

echo -e "using $pqn\n"

TIMEFORMAT="time: %3R"
time {
echo "eye $pqn --turtle $log --query $query --nope"
eye $pqn --turtle $log --query $query --nope
}