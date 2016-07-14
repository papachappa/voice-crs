#!/bin/bash

#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#SC_DIR=../../scenarios
SIPP=/usr/protei/utils/sipp/sipp

$SIPP -sf ./scenario.xml\
        -set cgpn 6000000\
        -set domen 192.168.108.26\
        -l 1\
        -m 1\
        -p 5556\
        -skip_rlimit\
        -trace_msg \
        -message_file ./log \
        -i 192.168.108.26\
        192.168.108.26:5060

exit $?

