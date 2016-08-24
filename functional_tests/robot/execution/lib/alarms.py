#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable-all

from subprocess import Popen, PIPE
import subprocess
import shlex

logger = logging.getLogger('crsRemoteLibrary')
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)

class Alarms(object):


    def umount_storage(self, storage):
        command = subprocess.Popen(["umount -l %s" % (storage)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = command.communicate()[0]
        stderr = command.communicate()[1]
        print 'STDOUT:{0}, STDERR:{1}'.format(stdout, stderr)

    def mount_storage(self, storage):
        command = subprocess.Popen(["mount {0}.bin {0} -o loop".format(storage)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = command.communicate()[0]
        stderr = command.communicate()[1]
        print 'STDOUT:{0}, STDERR:{1}'.format(stdout, stderr)

    def check_for_alarms(self, file_f, *words):
        datafile = file(file_f)
        for word in words:
            datafile.seek(0)
            if word not in datafile.read():
               raise AssertionError("*ERROR* File does not contain a %s section. Not good!" % word)





if __name__ == '__main__':
  import sys
  from robotremoteserver import RobotRemoteServer
  RobotRemoteServer(crsRemoteLibrary(), *sys.argv[1:])
