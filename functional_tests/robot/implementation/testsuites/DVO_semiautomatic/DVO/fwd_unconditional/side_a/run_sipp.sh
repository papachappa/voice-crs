#!/bin/bash

#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#SC_DIR=../../scenarios
SIPP=/usr/protei/utils/sipp/sipp

$SIPP -sf ./scenario.xml\
        -set cgpn 5000000\
        -set service 6000000\
        -set domen 192.168.108.26\
        -p 5555\
        -l 1\
        -m 1\
        -skip_rlimit\
        -trace_msg \
        -mi 192.168.108.26\
        -mp 13500\
        -message_file ./log \
        -i 192.168.108.26\
        192.168.108.26:5060

exit $?

