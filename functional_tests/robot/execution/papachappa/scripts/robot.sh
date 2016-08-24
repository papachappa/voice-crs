#!/bin/bash

#dt=`date+%Y_%m_%d`
#tm=`date +%H_%M`
#testnum="0"
##/"$dt"_"$tm"_"$testnum"\
path="../../../implementation/testsuites/QA_testsuite/"
varfile="../settings/env_settings.py"

date=`date +"%Y-%d-%m_%H_%M_%S"`
mkdir -p reports/$date

pybot -d reports/$date \
      -b debug.log \
      -L DEBUG:DEBUG \
      -x result \
      -W `tput cols` \
      -e inworkORdisable \
      --variablefile $varfile \
      $path #/"$testnum"*
