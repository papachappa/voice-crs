#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


REPLICA_AGENT_PATH = "/usr/protei/Protei-CRS/Replica-Agent"
REPLICA_CLIENT_PATH = "/usr/protei/Protei-CRS/Replica-Client"
CRS_REMOTE_PATH = '/usr/protei/Protei-CRS/Voice'
STORAGE_PATH = '/usr/protei/Protei-CRS/Replica-Client/storage'


flag = str(sys.argv[4])
rack = str(sys.argv[5])
file_count_local = str(sys.argv[1])
file_count_remote = str(sys.argv[2])
chan_num = str(sys.argv[3])
file_count_local = int(file_count_local)
file_count_remote = int(file_count_remote)
chan_num = int(chan_num)

def check_recorded_files(file_count_local, file_count_remote):
    local = sum([len(files) for r, d, files in os.walk("%s/voice/local/%s" % (STORAGE_PATH, chan_num))])
    remote = sum([len(files) for r, d, files in os.walk("%s/voice/remote/%s" % (STORAGE_PATH, chan_num))])
    local = int(local)
    remote = int(remote)
    print local, remote

    if local != file_count_local or remote != file_count_remote:
       raise AssertionError("File quantity error")

def restore_config():
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
        f.write('VoiceRemote = ["./storage/voice/remote"]\n')
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
        f.write('VoiceLocal = ["./storage/voice/local"]\n')
        f.write('MetaRemote = "./storage/meta/remote"\n')
        f.write('VoiceRemote = ["./storage/voice/remote"]\n')
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
        f.write('VoiceRemote = ["./storage/voice/remote"]\n')
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
        f.write('VoiceLocal = ["./storage/voice/local"]\n')
        f.write('MetaRemote = "./storage/meta/remote"\n')
        f.write('VoiceRemote = ["./storage/voice/remote"]\n')
        f.write('[Authentication]\n')
        f.write('Username = \'repl\'\n')
        f.write('Password = \'pass\'\n')
        f.close()


# def check_mirroring():
#     file_list = []
#     rootDir = '%s/voice/' % STORAGE_PATH
#     for dirName, subdirList, fileList in os.walk(rootDir):
#                 for fname in fileList:
#                     file_list.append("%s/%s" % (dirName, fname))
#     #matching = [s for s in file_list if "RecordingList.txt" in s]
#     file_list = [ x for x in file_list if "RecordingList.txt" not in x ]
#     print file_list

if __name__ == '__main__':
     if flag == "1":
        restore_config()
     if flag == "0":
        check_recorded_files(file_count_local, file_count_remote)
