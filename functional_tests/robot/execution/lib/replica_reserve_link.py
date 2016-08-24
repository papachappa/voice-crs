#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import fileinput
from subprocess import Popen, PIPE
import subprocess
import shutil
import re
import time
import signal

REPLICA_AGENT_PATH = "/usr/protei/Protei-CRS/Replica-Agent"
REPLICA_CLIENT_PATH = "/usr/protei/Protei-CRS/Replica-Client"
CRS_REMOTE_PATH = '/usr/protei/Protei-CRS/Voice'
STORAGE_PATH = '/usr/protei/Protei-CRS/Replica-Client/storage'
CHAN_NUM = '1'

flag = str(sys.argv[1])
rack = str(sys.argv[2])

# chan_num = str(sys.argv[3])
# file_count_local = int(file_count_local)
# file_count_remote = int(file_count_remote)
# chan_num = int(chan_num)


def create_dd_files():
    #voice_list = []
    p = re.compile('[0-9a-f]+_[0-9a-f]+_[0-9a-f]+_((g729)|(g711)|(g723))_(r|m|t)x.*')
    for dirpath, dirs, files in os.walk('%s/voice/local/%s' % (STORAGE_PATH, CHAN_NUM)):
        for file in files:
             m = p.match(file)
             if m:

               command = subprocess.Popen(["dd if=/dev/zero of=%s/%s bs=1M count=100" % (dirpath, file)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
               stdout = command.communicate()[0]
               print stdout


def add_bandwith_limit_in_config():
    if rack == "1":

        #Create config file in agent in side_A
        f = open('%s/config/config.cfg' % REPLICA_AGENT_PATH, 'w+')
        f.write('[Common]\n')
        f.write('PrimaryIP = "192.0.2.42"\n')
        f.write('PrimaryPort = 9999\n')
        f.write('ReserveIP = "192.168.106.97"\n')
        f.write('ReservePort = 9999\n')
        f.write('[Path]\n')
        f.write('MetaRemote = "./storage/meta/remote"\n')
        f.write('VoiceRemote = ["./storage/voice/remote", "/var/protei/Protei-CRS-Storage/voice/remote"]\n')
        f.write('[Authentication]\n')
        f.write('Username = \'repl\'\n')
        f.write('Password = \'pass\'\n')
        f.close()


        #Create config file in client in side_A
        f = open('%s/config/config.cfg' % REPLICA_CLIENT_PATH, 'w+')
        f.write('[Common]\n')
        f.write('StorageLife = 182\n')
        f.write('IntervalBackup = 10\n')
        f.write('CountConnections = 10\n')
        f.write('PrimaryIP = "192.0.2.41"\n')
        f.write('PrimaryPort = 9999\n')
        f.write('ReserveIP = "192.168.72.203"\n')
        f.write('ReservePort = 9999\n')
        f.write('[Path]\n')
        f.write('MetaLocal = "./storage/meta/local"\n')
        f.write('VoiceLocal = ["./storage/voice/local", "/var/protei/Protei-CRS-Storage/voice/local"]\n')
        f.write('MetaRemote = "./storage/meta/remote"\n')
        f.write('VoiceRemote = ["./storage/voice/remote", "/var/protei/Protei-CRS-Storage/voice/remote"]\n')
        f.write('[Authentication]\n')
        f.write('Username = \'repl\'\n')
        f.write('Password = \'pass\'\n')
        f.close()

    if rack == "2":

        #Create config file in agent in side_B
        f = open('%s/config/config.cfg' % REPLICA_AGENT_PATH, 'w+')
        f.write('[Common]\n')
        f.write('PrimaryIP = "192.0.2.41"\n')
        f.write('PrimaryPort = 9999\n')
        f.write('ReserveIP = "192.168.72.203"\n')
        f.write('ReservePort = 9999\n')
        f.write('[Path]\n')
        f.write('MetaRemote = "./storage/meta/remote"\n')
        f.write('VoiceRemote = ["./storage/voice/remote", "/var/protei/Protei-CRS-Storage/voice/remote"]\n')
        f.write('[Authentication]\n')
        f.write('Username = \'repl\'\n')
        f.write('Password = \'pass\'\n')
        f.close()


        #Create config file in client in side_B
        f = open('%s/config/config.cfg' % REPLICA_CLIENT_PATH, 'w+')
        f.write('[Common]\n')
        f.write('StorageLife = 182\n')
        f.write('IntervalBackup = 10\n')
        f.write('CountConnections = 10\n')
        f.write('PrimaryIP = "192.0.2.42"\n')
        f.write('PrimaryPort = 9999\n')
        f.write('ReserveIP = "192.168.106.97"\n')
        f.write('ReservePort = 9999\n')
        f.write('PrimaryBandwidthLimit = 1000\n')
        f.write('[Path]\n')
        f.write('MetaLocal = "./storage/meta/local"\n')
        f.write('VoiceLocal = ["./storage/voice/local", "/var/protei/Protei-CRS-Storage/voice/local"]\n')
        f.write('MetaRemote = "./storage/meta/remote"\n')
        f.write('VoiceRemote = ["./storage/voice/remote", "/var/protei/Protei-CRS-Storage/voice/remote"]\n')
        f.write('[Authentication]\n')
        f.write('Username = \'repl\'\n')
        f.write('Password = \'pass\'\n')
        f.close()


    if rack == "3":

        #Create config file in agent in side_A
        f = open('%s/config/config.cfg' % REPLICA_AGENT_PATH, 'w+')
        f.write('[Common]\n')
        f.write('PrimaryIP = "192.0.2.42"\n')
        f.write('PrimaryPort = 9999\n')
        f.write('ReserveIP = "192.168.106.97"\n')
        f.write('ReservePort = 9999\n')
        f.write('[Path]\n')
        f.write('MetaRemote = "./storage/meta/remote"\n')
        f.write('VoiceRemote = ["./storage/voice/remote", "/var/protei/Protei-CRS-Storage/voice/remote"]\n')
        f.write('[Authentication]\n')
        f.write('Username = \'repl\'\n')
        f.write('Password = \'pass\'\n')
        f.close()


        #Create config file in client in side_A
        f = open('%s/config/config.cfg' % REPLICA_CLIENT_PATH, 'w+')
        f.write('[Common]\n')
        f.write('StorageLife = 182\n')
        f.write('IntervalBackup = 10\n')
        f.write('CountConnections = 10\n')
        f.write('PrimaryIP = "192.0.2.41"\n')
        f.write('PrimaryPort = 9999\n')
        f.write('ReserveIP = "192.168.72.203"\n')
        f.write('ReservePort = 9999\n')
        f.write('PrimaryBandwidthLimit = 1000\n')
        f.write('[Path]\n')
        f.write('MetaLocal = "./storage/meta/local"\n')
        f.write('VoiceLocal = ["./storage/voice/local", "/var/protei/Protei-CRS-Storage/voice/local"]\n')
        f.write('MetaRemote = "./storage/meta/remote"\n')
        f.write('VoiceRemote = ["./storage/voice/remote", "/var/protei/Protei-CRS-Storage/voice/remote"]\n')
        f.write('[Authentication]\n')
        f.write('Username = \'repl\'\n')
        f.write('Password = \'pass\'\n')
        f.close()

    if rack == "4":

        #Create config file in agent in side_B
        f = open('%s/config/config.cfg' % REPLICA_AGENT_PATH, 'w+')
        f.write('[Common]\n')
        f.write('PrimaryIP = "192.0.2.41"\n')
        f.write('PrimaryPort = 9999\n')
        f.write('ReserveIP = "192.168.72.203"\n')
        f.write('ReservePort = 9999\n')
        f.write('[Path]\n')
        f.write('MetaRemote = "./storage/meta/remote"\n')
        f.write('VoiceRemote = ["./storage/voice/remote", "/var/protei/Protei-CRS-Storage/voice/remote"]\n')
        f.write('[Authentication]\n')
        f.write('Username = \'repl\'\n')
        f.write('Password = \'pass\'\n')
        f.close()


        #Create config file in client in side_B
        f = open('%s/config/config.cfg' % REPLICA_CLIENT_PATH, 'w+')
        f.write('[Common]\n')
        f.write('StorageLife = 182\n')
        f.write('IntervalBackup = 10\n')
        f.write('CountConnections = 10\n')
        f.write('PrimaryIP = "192.0.2.42"\n')
        f.write('PrimaryPort = 9999\n')
        f.write('ReserveIP = "192.168.106.97"\n')
        f.write('ReservePort = 9999\n')
        f.write('[Path]\n')
        f.write('MetaLocal = "./storage/meta/local"\n')
        f.write('VoiceLocal = ["./storage/voice/local", "/var/protei/Protei-CRS-Storage/voice/local"]\n')
        f.write('MetaRemote = "./storage/meta/remote"\n')
        f.write('VoiceRemote = ["./storage/voice/remote", "/var/protei/Protei-CRS-Storage/voice/remote"]\n')
        f.write('[Authentication]\n')
        f.write('Username = \'repl\'\n')
        f.write('Password = \'pass\'\n')
        f.close()









def start_speed_measurement():
    layout_list = []
    speed = ""
    command = subprocess.Popen(["/usr/protei/utils/misc/if_stat.sh 5 eth3"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(6)
    for line in command.stdout.readline().splitlines():
        layout_list.append(line.strip())
    os.kill(command.pid, signal.SIGINT)
    for i in layout_list:
        i = i.split('   ')
        #print "First %s, second %s, third, %s, 4th %s" % (i[0], i[1], i[2], i[3])
        speed = i[1]
    speed = speed.split(' ')[1].split(',')[0]
    speed = int(speed)
    print speed
    if speed > 9 or speed < 7:
       raise AssertionError("*ERROR* Speed is outside range!")



if __name__ == '__main__':
     if flag == "1":
        add_bandwith_limit_in_config()
     if flag == "2":
        create_dd_files()
     if flag == "3":
        start_speed_measurement()

