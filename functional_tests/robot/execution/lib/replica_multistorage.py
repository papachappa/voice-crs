#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import fileinput
from subprocess import Popen, PIPE
import subprocess
import shutil

REPLICA_AGENT_PATH = "/usr/protei/Protei-CRS/Replica-Agent"
REPLICA_CLIENT_PATH = "/usr/protei/Protei-CRS/Replica-Client"
CRS_REMOTE_PATH = '/usr/protei/Protei-CRS/Voice'
STORAGE_PATH = '/usr/protei/Protei-CRS/Replica-Client/storage'

flag = str(sys.argv[1])
rack = str(sys.argv[2])

# chan_num = str(sys.argv[3])
# file_count_local = int(file_count_local)
# file_count_remote = int(file_count_remote)
# chan_num = int(chan_num)


#### Old function when path sets in python py file
# def add_another_path_in_config():
#     processing_path = False
#     if 'VOICE_LOCAL_PATH = \'/var/protei/Protei-CRS-Storage/voice/local\'' not in open('%s/bin/client.py' % REPLICA_CLIENT_PATH).read():
#         for line in fileinput.input('%s/bin/client.py' % REPLICA_CLIENT_PATH, inplace=1):
#             if line.startswith('DIGEST_URI'):
#                 processing_path = True
#             else:
#                 if processing_path:
#                     print 'VOICE_LOCAL_PATH = \'/var/protei/Protei-CRS-Storage/voice/local\''
#                     print 'META_LOCAL_PATH = \'/var/protei/Protei-CRS-Storage/meta/local\''
#                 processing_path = False
#             print line.rstrip()

#     if 'VOICE_PATH = \'/var/protei/Protei-CRS-Storage/voice/remote\'' not in open('%s/bin/agent.py' % REPLICA_AGENT_PATH).read():
#         for line in fileinput.input('%s/bin/agent.py' % REPLICA_AGENT_PATH, inplace=1):
#             if line.startswith('DIGEST_URI'):
#                 processing_path = True
#             else:
#                 if processing_path:
#                     print 'VOICE_PATH = \'/var/protei/Protei-CRS-Storage/voice/remote\''
#                     print 'META_PATH = \'/var/protei/Protei-CRS-Storage/meta/remote\''
#                 processing_path = False
#             print line.rstrip()


def add_another_path_in_config():
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
        f.write('IntervalBackup = 30\n')
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
        f.write('IntervalBackup = 30\n')
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



def get_multi_storage_dir():
    DIRS = ['/usr/protei/Protei-CRS/Voice/storage/voice/', '/var/protei/Protei-CRS-Storage/voice/']
    for i in DIRS:
        for dirpath, dirs, files in os.walk(i):
            if files:
               print i
               return i


def check_multi_storage():
      actual_dir = get_multi_storage_dir()
      first_list = []
      second_list = []
      local_path = 'local'
      remote_path = 'remote'
      del first_list[:]
      del second_list[:]
      s = subprocess.Popen("find %s%s -regex '.*/[0-9]+_[0-9]+_[a-zA-Z0-9]+_g[0-9]+_.._[a-zA-Z0-9]+_[a-zA-Z0-9]+' | sort -n | cut -d '/' -f9-" % (actual_dir, local_path),shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      for item in s.stdout.readlines():
              item = item.strip()
              first_list.append(item)
      print "*INFO* Length of first list %s" % len(first_list)
      print first_list
      s = subprocess.Popen("find %s%s -regex '.*/[0-9]+_[0-9]+_[a-zA-Z0-9]+_g[0-9]+_.._[a-zA-Z0-9]+_[a-zA-Z0-9]+' | sort -n | cut -d '/' -f9-" % (actual_dir, remote_path), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      for item in s.stdout.readlines():
              item = item.strip()
              second_list.append(item)
      print "*INFO* Length of second list %s" % len(second_list)
      print second_list
      if len(first_list) != len(second_list):
              raise AssertionError("*ERROR* Files on servers are not identical")



if __name__ == '__main__':
     if flag == "1":
        add_another_path_in_config()
     if flag == "0":
        check_multi_storage()

