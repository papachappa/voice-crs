#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import *
from fabric.operations import run, put
import pdb
import os
import signal
import time
import glob
import datetime
import time
import subprocess
from subprocess import Popen, PIPE

import sys
sys.path.insert(0, "../papachappa/settings")
from env_settings import *

#REMOTE_SIPP_DIR = os.getenv('REMOTE_SIPP_DIR', '/usr/protei/robot/sipp_remote_library')
REMOTE_CRS_DIR = os.getenv('REMOTE_CRS_DIR', '/usr/protei/Protei-CRS/')
REMOTE_MKD_DIR = os.getenv('REMOTE_MKD_DIR', '/usr/protei/Protei-MKD')
REMOTE_MCU_DIR = os.getenv('REMOTE_MCU_DIR', '/usr/protei/Protei-MCU')
REMOTE_MVSIP_DIR = os.getenv('REMOTE_MVSIP0_DIR', '/usr/protei/Protei-MV.SIP')


def check_library_is_running(lib_name, host_ip, port=""):
   with settings(user='root', password='elephant', host_string=host_ip, warn_only=True):
      command = run("ps afx | grep '%s %s %s' | grep -v grep | wc -l" % (lib_name, host_ip, port), pty=False)

      if command == "0":
         return False
      else:
         return True


class Error(AssertionError):
    pass

class Manipulation():

   def manipulate(self, component, action, host_ip):
      with settings(user='root', password='elephant', host_string=host_ip):
        if component == "MCU" and host_ip == "192.168.125.12":
         print '**DEBUG** %s, %s, %s' % (component, action, host_ip)
         run("%s/%s/%s -f" % (REMOTE_MKD_DIR, component, action), warn_only=True, shell=True, pty=False)
        else: 
         print '**DEBUG** %s, %s, %s' % (component, action, host_ip)
         run("/usr/protei/Protei-%s/%s/%s -f" % (component, component, action), warn_only=True, shell=True, pty=False)
        out = run('echo $?')
        if out != "0":
          raise AssertionError("Something went wrong!")

   def file_manipulate(self, command, file_1, file_2, host_ip):
      with settings(user='root', password='elephant', host_string=host_ip):
        print '**DEBUG** %s, %s, %s, %s' % (command, file_1, file_2, host_ip)
        run("%s %s %s" % (command, file_1, file_2), warn_only=True, shell=True, pty=False)
        out = run('echo $?')
        print "*INFO* std out: %s" % out.stdout 
        if out != "0":
          raise AssertionError("Something went wrong!")

   def run_command(self, login, passwd, command, host_ip):
      with settings(user=login, password=passwd, host_string=host_ip):
        print '**DEBUG** %s, %s' % (command, host_ip)
        s = run("%s" % command, warn_only=True, shell=True, pty=False)
        print s
        #return out
        out = run('echo $?')
        print "*INFO* std out: %s" % out.stdout
        if out != "0":
          raise AssertionError("Something went wrong!")

   def get_module_version(self, name, command, host_ip):
      with settings(user='root', password='elephant', host_string=host_ip):
        print '**DEBUG** %s, %s' % (command, host_ip)
        out = run("%s" % command, warn_only=True, shell=True, pty=False)
        #out = out.split('\n')
        out = out.stdout.split('\n')[0:7]
        print "*INFO* %s Version:" % name
        for line in out:
            print "*INFO* %s" % line
        #return out



   def run_command_without_bash(self, command, host_ip):
      env.shell = "/bin/sh -c"
      with settings(user='root', password='elephant', host_string=host_ip):
        print '**DEBUG** %s, %s' % (command, host_ip)
        run("%s" % command, warn_only=True, shell=True, pty=False)
        #return out
        out = run('echo $?')
        print "*INFO* std out: %s" % out.stdout
        if out != "0":
          raise AssertionError("Something went wrong!")



   def tshark(self, duration, path_pcap, host_ip):
      with settings(user='root', password='elephant', host_string=host_ip):
        print '**DEBUG** Running command with path and host %s, %s' % (path_pcap, host_ip)
        run('nohup tshark -a duration:%s -i lo -B 50 -w %s >& /dev/null < /dev/null &' % (duration, path_pcap), warn_only=True, shell=True, pty=False)
        out = run('echo $?')
        print "*INFO* std out: %s" % out.stdout 
        if out != "0":
          raise AssertionError("Something went wrong!")

   def tshark_dump(self, path_pcap, path_txt, host_ip):
      with settings(user='root', password='elephant', host_string=host_ip):
        try:
         out = run('tshark -r %s -o rtp.heuristic_rtp:TRUE -qz rtp,streams > %s' % (path_pcap, path_txt), warn_only=True, shell=True, pty=False)
         print out
        except:
            raise  AssertionError("Something went wrong!")


   def reset_crs_conf(self):
        
        crs_bak = os.path.abspath("%s/config/component/backup/crs.cfg.bak" % REMOTE_crs_DIR)
        crs_orig = os.path.abspath("%s/config/component/crs.cfg" % REMOTE_crs_DIR)
        
        with settings(user='root', password='elephant', host_string='192.168.125.7', warn_only=True):

         try: 
           run('/bin/cp -rf %s %s' % (crs_bak,crs_orig), warn_only=True)
         
         except SystemExit:
            raise  AssertionError("Error in copying file!")
         
         print "*INFO* Config file rewrited succesfully"

         try:
           run('%s/restart -f' % REMOTE_crs_DIR) 
           time.sleep(1)

         except SystemExit:
            raise  AssertionError("Error in restarting crs!")

         print "*INFO* crs reloaded successfully"


   # MKD-MKD
   # MKD-MCU
   def check_pids_count(self, process, command, host_ip):
      with settings(user='root', password='elephant', host_string=host_ip, warn_only=True):
        pid = run("ps afx | grep %s | grep -v grep | wc -l" % process)
        #pid = ("ps afx | grep %s | grep -v grep | wc -l" % process)
        #s = Popen(pid, shell=True, stdin=PIPE, stderr=PIPE, stdout=PIPE)
        #pids_data = subprocess.check_output(pid, shell=True)

        if command == "stop" and pid == "0":
          print "*INFO* Program PID file does not exist. All is good"
        elif command == "start" and pid == "1":
          print "*INFO* Program PID file exist. All is good"
        elif command == "restart" and pid == "1":
          print "*INFO* Program PID file exist. All is good"  
        else:
         raise  AssertionError("Error in PID file!")  


   def start_crs_library(self, host_ip, port, path):
      lib_name = 'crs_remote_library.py'
      with settings(user='root', password='elephant', host_string=host_ip, warn_only=True):
         if not check_library_is_running(lib_name, host_ip, port):
            print "Library %s have not started, starting..." % lib_name
            run('nohup python2.7 %s/%s %s %s >& /dev/null < /dev/null &' % (path, lib_name, host_ip, port), pty=False)
         else:
            print "**DEBUG** %s already started" % lib_name
         if not check_library_is_running(lib_name, host_ip, port):
            raise AssertionError("Can't start %s:%s:%s/%s" % (host_ip, port, path, lib_name))

   def stop_crs_library(self, host_ip):
      with settings(user='root', password='elephant', host_string=host_ip, warn_only=True):
         command = run("kill $(ps afx | grep crs_remote_library.py | grep -v grep | awk '{print $1}')", pty=False)
         time.sleep(5)
         if check_library_is_running("crs_remote_library.py", host_ip):
            raise  AssertionError("Something went wrong in killing crs_remote_library!")
         print "**INFO** crs_remote_library successfully killed"


   def start_sipp_library(self, host_ip, port, path):
      lib_name = 'sipp_remote_library.py'
      with settings(user='root', password='elephant', host_string=host_ip, warn_only=True):
         if not check_library_is_running('sipp_remote_library.py', host_ip, port):
            print "Library have not started, starting..."
            run('nohup python2.7 %s/%s %s %s >& /dev/null < /dev/null &' % (path, lib_name, host_ip, port), pty=False)
         else:
            print "**DEBUG** sipp_remote_library already started" 
            return
         if not check_library_is_running(lib_name, host_ip, port):
            raise AssertionError("Can't start %s:%s:%s/%s" % (host_ip, port, path, lib_name))

   def stop_sipp_library(self, host_ip):
      with settings(user='root', password='elephant', host_string=host_ip, warn_only=True):
         command = run("kill $(ps afx | grep sipp_remote_library.py | grep -v grep | awk '{print $1}')", pty=False)
         time.sleep(5)
         if check_library_is_running("sipp_remote_library.py", host_ip):
            raise  AssertionError("Something went wrong in killing sipp_remote_library!") 
         print "**INFO** sipp_remote_library successfully killed"


   def upload_file(self, login, passwd, host_ip, src, dst):
      with settings(user=login, password=passwd, host_string=host_ip, warn_only=True):
         command = put(src, dst, mode=0755)
         time.sleep(1)


   def check_for_identity(self, login_1, passwd_1, host_ip_1, login_2, passwd_2, host_ip_2, flag="Default"):
      first_list = []
      second_list = []
      local_path = ''
      remote_path = ''
      for  i in range(2):
              print i
              del first_list[:]
              del second_list[:]

              if i == 0:
                 local_path = 'local'
                 remote_path = 'remote'
              else:
                 local_path = 'remote'
                 remote_path = 'local'

              with settings(user=login_1, password=passwd_1, host_string=host_ip_1, warn_only=True):
                 command = run("find {0}/voice/{1} -regex '.*/[0-9]+_[0-9]+_[a-zA-Z0-9]+_g[0-9]+_.._[a-zA-Z0-9]+_[a-zA-Z0-9]+' | sort -n | cut -d '/' -f9-".format(NEW_CRS_STORAGE, local_path), pty=False)
                 for item in command.splitlines():
                     first_list.append(item)
              print len(first_list)
              print first_list
              with settings(user=login_2, password=passwd_2, host_string=host_ip_2, warn_only=True):
                 command = run("find {0}/voice/{1} -regex '.*/[0-9]+_[0-9]+_[a-zA-Z0-9]+_g[0-9]+_.._[a-zA-Z0-9]+_[a-zA-Z0-9]+' | sort -n | cut -d '/' -f9-".format(NEW_CRS_STORAGE, remote_path), pty=False)
                 for item in command.splitlines():
                     second_list.append(item)
              print len(second_list)
              print second_list
              if set(first_list) != set(second_list) and flag == "Default":
                      raise AssertionError("*ERROR* Files on servers are not identical")
              if flag == "Overdays" and i == 0 and len(second_list) != 0:
                      raise AssertionError("*ERROR* Replica worked over storage time and days?!")
              if flag == "Overdays" and i == 1 and len(first_list) != 0:
                      raise AssertionError("*ERROR* Replica worked over storage time and days?!")


### Before existing Client config
   # def edit_replica_storage_life(self, login, passwd, host_ip, file_f="{0}/bin/client.py".format(REPLICA_CLIENT_PATH), before="STORAGE_LIFE_DAY = 182", days="STORAGE_LIFE_DAY = 182"):
   #  with settings(user=login, password=passwd, host_string=host_ip):
   #       out = run('sed -i -- "s/STORAGE_LIFE = [0-9]*/STORAGE_LIFE = 1/g" {0}'.format(file_f), warn_only=True, shell=True, pty=False)
   #       out = run('sed -i -- "s/{0}/{1}/g" {2}'.format(before, days, file_f), warn_only=True, shell=True, pty=False)

   def edit_replica_storage_life(self, login, passwd, host_ip, file_f="{0}/bin/client.py".format(REPLICA_CLIENT_PATH), before="StorageLife = 182", days="StorageLife = 182"):
    with settings(user=login, password=passwd, host_string=host_ip):
         out = run('sed -i -- "s/StorageLife = [0-9]*/StorageLife = 1/g" {0}'.format(file_f), warn_only=True, shell=True, pty=False)
         out = run('sed -i -- "s/{0}/{1}/g" {2}'.format(before, days, file_f), warn_only=True, shell=True, pty=False)

   def date_manipulation(self, login, passwd, host_ip, days=40):
       now = datetime.datetime.now()
       ts_end = now - datetime.timedelta(days=40)
       ts_end = ts_end.strftime("%m%d%H%M%Y")
       print now, ts_end
       with settings(user=login, password=passwd, host_string=host_ip):
         out = run('LC_ALL=C date {0}'.format(ts_end), warn_only=True, shell=True, pty=False)

   def date_now(self, login, passwd, host_ip):
       now = datetime.datetime.now()
       ts_end = now.strftime("%m%d%H%M%Y")
       print now, ts_end
       with settings(user=login, password=passwd, host_string=host_ip):
         out = run('LC_ALL=C date {0}'.format(ts_end), warn_only=True, shell=True, pty=False)


   def check_multistorage(self, login, passwd, host_ip, count_1, count_2):
        first_list = []
        second_list = []
        with settings(user=login, password=passwd, host_string=host_ip, warn_only=True):
                 command = run("find {0}/voice/local/1 -regex '.*/[0-9]+_[0-9]+_[a-zA-Z0-9]+_g[0-9]+_.._[a-zA-Z0-9]+_[a-zA-Z0-9]+' -size +9000c | sort -n | cut -d '/' -f9-".format(CRS_STORAGE_REMOTE_PATH_ANOTHER), pty=False)
                 for item in command.splitlines():
                     first_list.append(item)
                 command = run("find {0}/voice/local/1 -regex '.*/[0-9]+_[0-9]+_[a-zA-Z0-9]+_g[0-9]+_.._[a-zA-Z0-9]+_[a-zA-Z0-9]+' -size +9000c | sort -n | cut -d '/' -f9-".format(CRS_STORAGE_REMOTE_PATH_YET_ANOTHER), pty=False)
                 for item in command.splitlines():
                     second_list.append(item)

        if count_1 != len(first_list) or count_2 != len(second_list):
                       raise AssertionError("*ERROR* Probably error with file count")

#find /var/fs5/voice/local/1 -regex '.*/[0-9]+_[0-9]+_[a-zA-Z0-9]+_g[0-9]+_.._[a-zA-Z0-9]+_[a-zA-Z0-9]+' -size +9000c | sort -n | cut -d '/' -f9-

#a = Manipulation()
#a.check_multistorage('root', 'elephant', '192.168.108.26', 6, 4)
#a.edit_replica_storage_life('root', 'elephant', '192.168.106.97')
# a.get_module_version('CRS-BE', '/usr/protei/Protei-CRS-BE/version', "192.168.108.26")
# a.get_module_version('CRS-Meta', '/usr/protei/Protei-CRS-Meta/version', "192.168.108.26")
# a.get_module_version('MKD', '/usr/protei/Protei-MKD/MKD/version', "192.168.108.26")
# a.get_module_version('MCU', '/usr/protei/Protei-MKD/MCU/version', "192.168.108.26")

