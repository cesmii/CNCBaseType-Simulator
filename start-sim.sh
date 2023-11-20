#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
if [ $# -eq 0 ]; then
    ARG=1
else
    ARG=$1
fi
ARG="-o $ARG"
echo Launching CNCBaseType Simulator with argument: $ARG
echo
/usr/bin/python3 $SCRIPT_DIR/sim.py $ARG
