#!/bin/bash

#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#SC_DIR=../../scenarios
SIPP=/usr/protei/utils/sipp/sipp

$SIPP -sf ./scenario.xml\
        -set cgpn 6000000\
        -set service *21*6000001#\
        -set domen 192.168.108.26\
        -p 5556\
        -l 1\
        -m 1\
        -skip_rlimit\
        -trace_msg \
        -message_file ./log \
        -i 192.168.108.26\
        -au 6000000\
        -ap 6000000\
        192.168.108.26:5060

exit $?

