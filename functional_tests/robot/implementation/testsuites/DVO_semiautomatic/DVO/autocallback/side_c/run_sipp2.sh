#!/bin/bash

#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#SC_DIR=../../scenarios
SIPP=/usr/protei/utils/sipp/sipp

$SIPP -sf ./scenario2.xml.sipp\
        -set cgpn 6000001\
        -p 5557\
        -l 1\
        -m 1\
        -skip_rlimit\
        -trace_msg \
        -mi 192.168.108.26\
        -mp 13504\
        -trace_err\
        -error_file ./error\
        -message_file ./log \
        -i 192.168.108.26\
        192.168.108.26:5060

exit $?

