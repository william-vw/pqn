#!/bin/bash

usage="usage:
run.sh -t <type> -q <query> -l <log> -p <pqn>
where
    -t <type> is the run type (eye or pvm)
    -q <query> is the query over the event log
    -l <log> is the event log
    -p <pqn> is the PQN implementation"

while getopts "t:q:l:p:" option; do
    case "${option}" in
        t | type)
            type=${OPTARG}
        ;;
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

if [ $type != "eye" ] && [ $type != "pvm" ]; then
    echo "use 'eye' or 'pvm' for type parameter"
    exit 1
fi

if [[ -z "$pqn" ]]; then
    pqn="pqn.n3"
fi

echo -e "using $pqn\n"

if [ $type == 'eye' ]; then
    eye $pqn --turtle $log --query $query --nope
elif [ $type == 'pvm' ]; then
    swipl -x $pqn -- --query $query --nope
fi