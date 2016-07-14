#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Module For checking Eraser

'''

import os
import glob
from StringIO import StringIO
from time import *
from datetime import datetime, timedelta
import pdb
import sys
from fabric.api import *
from fabric.operations import run, put
# sys.path.insert(0, "../papachappa/settings")
# from env_settings import *

HOST_IP = "192.168.72.203"
LOGIN = 'root'
PASSWORD = '12345678'
ERASER_PATH = '/usr/protei/Protei-CRS/Eraser'
STORAGE_PATH = '/usr/protei/data/Protei-CRS/storage'

TEST_VOICE_LOCAL_DIRECTORY = '%s/voice/local/1' % STORAGE_PATH
TEST_VOICE_REMOTE_DIRECTORY = '%s/voice/remote/1' % STORAGE_PATH
TEST_META_LOCAL_DIRECTORY = '%s/meta/local/1' % STORAGE_PATH
TEST_META_REMOTE_DIRECTORY = '%s/meta/remote/1' % STORAGE_PATH

DIR_LIST = [TEST_VOICE_LOCAL_DIRECTORY, TEST_VOICE_REMOTE_DIRECTORY, TEST_META_LOCAL_DIRECTORY, TEST_META_REMOTE_DIRECTORY]

FILE_CONTENT_1 = "15d/10f/802_0_84055cfc6de0cc0b_g729_tx_c278ac43_4c90"
FILE_CONTENT_2 = "162/10f/802_0_e4215efd269eb400_g729_tx_b5cbd358_4ba0"
FILE_CONTENT_3 = "166/10f/802_0_4255cfd7e1e5005_g729_tx_1d5eeda5_6b44"
FILE_CONTENT_4 = "e2/114/802_0_c4555cfc5a137003_g729_tx_a09411a8_4bc8"


def get_today_date():
    return strftime("%Y-%m-%d", gmtime())

def get_arbitrary_date(days):
    now = datetime.now().date()
    day_shift = timedelta(days=days)
    res = str(now - day_shift)
    return res

def create_test_files(days, today_flag=0):
    try:
        with settings(user=LOGIN, password=PASSWORD, host_string=HOST_IP):



         run('mkdir -p %s/15d/10f' % TEST_VOICE_LOCAL_DIRECTORY, warn_only=False, shell=True, pty=False)
         run('mkdir -p %s/162/10f' % TEST_VOICE_LOCAL_DIRECTORY, warn_only=False, shell=True, pty=False)
         run('mkdir -p %s/15d/10f' % TEST_VOICE_REMOTE_DIRECTORY, warn_only=False, shell=True, pty=False)
         run('mkdir -p %s/162/10f' % TEST_VOICE_REMOTE_DIRECTORY, warn_only=False, shell=True, pty=False)

         run('mkdir -p %s' % TEST_META_LOCAL_DIRECTORY, warn_only=False, shell=True, pty=False)
         run('mkdir -p %s' % TEST_META_REMOTE_DIRECTORY, warn_only=False, shell=True, pty=False)

         run('mkdir -p %s/%s'% (TEST_META_LOCAL_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)
         run('mkdir -p %s/%s'% (TEST_META_REMOTE_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)


         run('> %s/15d/10f/802_0_84055cfc6de0cc0b_g729_tx_c278ac43_4c90' % TEST_VOICE_LOCAL_DIRECTORY, warn_only=False, shell=True, pty=False)
         run('> %s/162/10f/802_0_e4215efd269eb400_g729_tx_b5cbd358_4ba0' % TEST_VOICE_LOCAL_DIRECTORY, warn_only=False, shell=True, pty=False)
         run('> %s/15d/10f/802_0_84055cfc6de0cc0b_g729_tx_c278ac43_4c90' % TEST_VOICE_REMOTE_DIRECTORY, warn_only=False, shell=True, pty=False)
         run('> %s/162/10f/802_0_e4215efd269eb400_g729_tx_b5cbd358_4ba0' % TEST_VOICE_REMOTE_DIRECTORY, warn_only=False, shell=True, pty=False)

         run('> %s/%s'% (TEST_VOICE_LOCAL_DIRECTORY, get_arbitrary_date(10)), warn_only=False, shell=True, pty=False)
         run('> %s/%s'% (TEST_VOICE_REMOTE_DIRECTORY, get_arbitrary_date(10)), warn_only=False, shell=True, pty=False)


         run('echo %s > %s/%s'% (FILE_CONTENT_1, TEST_VOICE_LOCAL_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)
         run('echo %s >> %s/%s'% (FILE_CONTENT_2, TEST_VOICE_LOCAL_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)
         run('echo %s >> %s/%s'% (FILE_CONTENT_3, TEST_VOICE_LOCAL_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)
         run('echo %s >> %s/%s'% (FILE_CONTENT_4, TEST_VOICE_LOCAL_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)

         run('echo %s > %s/%s'% (FILE_CONTENT_1, TEST_VOICE_REMOTE_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)
         run('echo %s >> %s/%s'% (FILE_CONTENT_2, TEST_VOICE_REMOTE_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)
         run('echo %s >> %s/%s'% (FILE_CONTENT_3, TEST_VOICE_REMOTE_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)
         run('echo %s >> %s/%s'% (FILE_CONTENT_4, TEST_VOICE_REMOTE_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)


         run('> {0}/{1}/{1}'.format(TEST_META_LOCAL_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)
         run('> {0}/{1}/{1}'.format(TEST_META_REMOTE_DIRECTORY, get_arbitrary_date(days)), warn_only=False, shell=True, pty=False)

         if today_flag == 1:

             run('> %s/%s'% (TEST_VOICE_LOCAL_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)
             run('> %s/%s'% (TEST_VOICE_REMOTE_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)

             run('mkdir -p %s/%s'% (TEST_META_LOCAL_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)
             run('mkdir -p %s/%s'% (TEST_META_REMOTE_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)

             run('> {0}/{1}/{1}'.format(TEST_META_LOCAL_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)
             run('> {0}/{1}/{1}'.format(TEST_META_REMOTE_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)


             run('echo %s > %s/%s'% (FILE_CONTENT_1, TEST_VOICE_LOCAL_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)
             run('echo %s >> %s/%s'% (FILE_CONTENT_2, TEST_VOICE_LOCAL_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)
             run('echo %s >> %s/%s'% (FILE_CONTENT_3, TEST_VOICE_LOCAL_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)
             run('echo %s >> %s/%s'% (FILE_CONTENT_4, TEST_VOICE_LOCAL_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)

             run('echo %s > %s/%s'% (FILE_CONTENT_1, TEST_VOICE_REMOTE_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)
             run('echo %s >> %s/%s'% (FILE_CONTENT_2, TEST_VOICE_REMOTE_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)
             run('echo %s >> %s/%s'% (FILE_CONTENT_3, TEST_VOICE_REMOTE_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)
             run('echo %s >> %s/%s'% (FILE_CONTENT_4, TEST_VOICE_REMOTE_DIRECTORY, get_today_date()), warn_only=False, shell=True, pty=False)


    except RuntimeError:
         print "Something went wrong!"
         # out = run('echo $?')
         # if out != "0":
         #    raise AssertionError("Something went wrong!")


def check_all_delete():
    with settings(user=LOGIN, password=PASSWORD, host_string=HOST_IP):
         for n in DIR_LIST:
             s = os.path.split(n)
             out = run('if [ "$( ls -A {0} )" ]; then echo "Fill"; else  echo "Empty"; fi'.format(s[0]), warn_only=False, shell=True, pty=False)
             if "Empty" in out:
                 print "Directory Is Empty"
             else:
                 raise RuntimeError("Directory is not empty")


def check_delete_except_one_day():
    META_DIR = [TEST_META_LOCAL_DIRECTORY, TEST_META_REMOTE_DIRECTORY]
    VOICE_DIR = [TEST_VOICE_LOCAL_DIRECTORY, TEST_VOICE_REMOTE_DIRECTORY]
    with settings(user=LOGIN, password=PASSWORD, host_string=HOST_IP):
         for n in META_DIR:
            ### if [ -d "/usr/protei/Protei-CRS/Eraser/storage/meta/local/1/2016-07-11" ]; then echo "Exists"; fi
             with hide('running','warnings'), settings(warn_only=False):
               dir_ = run('find {0} -mindepth 1 -maxdepth 1 -type d'.format(n), warn_only=False, shell=True, pty=False)
               out = run('find {0} -mindepth 1 -maxdepth 1 -type d | wc -l'.format(n), warn_only=False, shell=True, pty=False)
               if get_today_date() in dir_ and out == "1":
                  print "OK, only today directory"
               else:
                  raise RuntimeError("There is not only today directory")
         for n in VOICE_DIR:
             with hide('running','warnings'), settings(warn_only=False):
               dir_ = run('find {0} -maxdepth 1 -type f'.format(n), warn_only=False, shell=True, pty=False)
               out = run('find {0} -maxdepth 1 -type f | wc -l'.format(n), warn_only=False, shell=True, pty=False)
               if get_today_date() in dir_ and out == "1":
                  print "OK, only today file"
               else:
                  raise RuntimeError("There is not only today file")


def run_eraser():
    with settings(user=LOGIN, password=PASSWORD, host_string=HOST_IP):
         try:
           run('cd {0}/ && ./eraser.py'.format(ERASER_PATH))
         except RuntimeError:
           print "Something went wrong!"

def edit_eraser_storage_life(file_f="{0}/eraser.py".format(ERASER_PATH), before="STORAGE_LIFE = 1", days="STORAGE_LIFE = 1"):
    with settings(user=LOGIN, password=PASSWORD, host_string=HOST_IP):
         out = run('sed -i -- "s/STORAGE_LIFE = [0-9]*/STORAGE_LIFE = 1/g" {0}'.format(file_f), warn_only=False, shell=True, pty=False)
         out = run('sed -i -- "s/{0}/{1}/g" {2}'.format(before, days, file_f), warn_only=False, shell=True, pty=False)

def add_some_garbage():
    try:
        create_test_files(1)
        with settings(user=LOGIN, password=PASSWORD, host_string=HOST_IP):
             run('cd {0} && > ABCDEFG'.format(TEST_META_LOCAL_DIRECTORY), warn_only=False, shell=True, pty=False)
             run('cd {0} && > ABCDEFG'.format(TEST_META_REMOTE_DIRECTORY), warn_only=False, shell=True, pty=False)
             run('cd {0} && > ABCDEFG'.format(TEST_VOICE_LOCAL_DIRECTORY), warn_only=False, shell=True, pty=False)
             run('cd {0} && > ABCDEFG'.format(TEST_VOICE_REMOTE_DIRECTORY), warn_only=False, shell=True, pty=False)
    except RuntimeError:
        print "Something went wrong!"

def emptying_folders():
    with settings(user=LOGIN, password=PASSWORD, host_string=HOST_IP):
         run('rm -rf {0}'.format(TEST_VOICE_LOCAL_DIRECTORY), warn_only=False, shell=True, pty=False)
         run('rm -rf {0}'.format(TEST_VOICE_REMOTE_DIRECTORY), warn_only=False, shell=True, pty=False)
         run('rm -rf {0}'.format(TEST_META_LOCAL_DIRECTORY), warn_only=False, shell=True, pty=False)
         run('rm -rf {0}'.format(TEST_META_REMOTE_DIRECTORY), warn_only=False, shell=True, pty=False)

#add_some_garbage()

# create_test_files(10)
# run_eraser()
# check_all_delete()
#edit_eraser_storage_life(days="STORAGE_LIFE = 13")
#Run LC_ALL=C before run command


# 1. Проверка что все каналы удалились - все файлы старые
# 2. Проверка что остались файлы только до нужного дня 
# 3. Проверка что лишние файлы удалились




