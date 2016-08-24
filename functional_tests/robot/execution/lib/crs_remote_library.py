#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable-all

"""
crs-Remote library
"""

import regex as re
import chardet
import fileinput
import wave
import contextlib
import binascii
import signal
import shutil
import os
import time
import glob
import pdb
import datetime
from subprocess import Popen, PIPE
import subprocess
import shlex
#import re
import sys
import logging
import errno
from StringIO import StringIO
from timeout import timeout
from KillProcess import KillProcess, KillJava

logger = logging.getLogger('crsRemoteLibrary')
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)
kpv_file_size = 980

def get_multi_storage_dir(conf_file="/usr/protei/Protei-CRS/Voice/config/Voice.cfg"):

         m = re.compile('(?im)BaseDirectory(?:\s)*=(?:\s)*{(?:(?:\s)*(".*")(?:\s)*;(?:\s)*)+(?:\s)*};')
         content = ""
         storage_list = []

         with open(conf_file, 'r') as inF:
             for line in inF:
                 content = content + line.strip()
         state = re.findall(m, content)
         state = state[0].split('"')
         for i in state:
             if ";" not in i and i:
                storage_list.append(i)
         #print storage_list
         return storage_list
# Optional
#         mod_list = []
#         for i in storage_list:
#              i = i + "voice/local"
#              mod_list.append(i)
#         print mod_list
####

#         for i in mod_list:
#             for dirpath, dirs, files in os.walk(i):
#                 if files:
#                    print i, "Not Empty"




def get_storage_dir(conf_file="/usr/protei/Protei-CRS/Voice/config/Voice.cfg"):
#        m = re.compile('(?im)BaseDirectories(?:\s)*=(?:\s)*{\n(?:(?:\s)*"(.*)"(?:\s)*;(?:\s)*\n)+(?:\s)*};')
        datafile = file(conf_file)
        datafile.seek(0)
        s = datafile.read()
        # print s
###        matches = re.findall('(?im)BaseDirectories(?:\s)*=(?:\s)*{\n(?:(?:\s)*"(.*)"(?:\s)*;(?:\s)*\n)+(?:\s)*};', s, overlapped=True)
        try:
           matches = re.findall('(?im)BaseDirectory="(.*)"', s)
           matches = os.path.split(matches[0])
           matches = os.path.split(matches[0])[0]
        except:
           get_multi_storage_dir()
        return matches


class ContinuableError(AssertionError):
    """
    Класс ошибки. Если обнаружена ошибка, то выполняем тесты дальше
    """
    ROBOT_CONTINUE_ON_FAILURE = True

class crsRemoteLibrary(object):

    def to_int(self, *vars):
        for var in vars:
            var = int(var)
        return vars



    def setup_crs_path(self, remote_mkd_dir='/usr/protei/Protei-MKD/MKD', remote_crs_dir='/usr/protei/Protei-CRS/Voice', remote_crs_be_dir='/usr/protei/Protei-CRS/BE',
                             remote_crs_meta_dir='/usr/protei/Protei-CRS/Meta', remote_crs_storage_dir=get_storage_dir(), remote_mcu_dir='/usr/protei/Protei-MKD/MCU',
                             remote_mvsip_dir='/usr/protei/Protei-MV.SIP'):
        """
        Функция установки значений переменных окружения
        для формирования команды для запуска crs
        """
        self.crs_dir = remote_crs_dir
        self.crs_be_dir = remote_crs_be_dir
        self.crs_meta_dir = remote_crs_meta_dir
        self.crs_storage_dir = remote_crs_storage_dir
        self.mcu_dir = remote_mcu_dir
        self.mkd_dir = remote_mkd_dir
        self.mvsip_dir = remote_mvsip_dir
        print "*INFO* Setup CRS dir: %s, MCU dir: %s, MV-SIP dir: %s, MKD dir: %s, CRS-META dir: %s, CRS-BE dir: %s, CRS-Storage dir: %s " % (self.crs_dir, self.mcu_dir, self.mvsip_dir, self.mkd_dir,
                                                                                                                                              self.crs_meta_dir, self.crs_be_dir, self.crs_storage_dir)


    def restore_config(self, config_name):
        path = "/usr/protei/Backup"
        retval = os.getcwd()
        print "*INFO* Current working directory %s" % retval
        os.chdir(path)
        retval = os.getcwd()
        print "Directory changed successfully %s" % retval

        command = subprocess.Popen(["_restore_config %s -f" % (config_name)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = command.communicate()[0]
        print 'STDOUT:{}'.format(stdout)


    def restart_module(self, *module_name):
      for module in module_name:
        path = ""

        if module == 'crs':
           path = os.path.abspath("%s/restart -f" % self.crs_dir)

        if module == 'crs_be':
           path = os.path.abspath("%s/restart -f" % self.crs_be_dir)

        if module == 'crs_meta':
           path = os.path.abspath("%s/restart -f" % self.crs_meta_dir)

        if module == 'mcu':
           path = os.path.abspath("%s/restart -f" % self.mcu_dir)

        if module == 'mkd':
           path = os.path.abspath("%s/restart -f" % self.mkd_dir)

        print "*INFO* Module name IS %s" % module
        print "*INFO* Path IS %s" % path

        s = subprocess.check_call("%s -f" % path, shell=True)
        time.sleep(1)
        if s != 0:
            raise AssertionError("Error in restarting %s" % module)
        else:
            print "*INFO* %s restarted successfully" % module

    def run_command(self, command):
        s = subprocess.check_call(command, shell=True)
        time.sleep(1)
        if s != 0:
            raise AssertionError("Error in running command!")
        else:
            print "*INFO* Command was run successfully"

    def find_voice_files(self, in_file, out_file, channel_id):
        top = "{0}/voice/local/{1}".format(in_file, channel_id)
#        if flag == 1:
#          p = re.compile('[0-9a-f]+_[0-9a-f]+_[0-9a-f]+_((g729)|(g711))_(r|m|t)x')
#        else:
#        p = re.compile('[0-9a-f]+_[0-9a-f]+_[0-9a-f]+_((g729)|(g711))_(r|m|t)x_[0-9a-f]+_[0-9a-f]+')
        p = re.compile('[0-9a-f]+_[0-9a-f]+_[0-9a-f]+_((g729)|(g711)|(g723))_(r|m|t)x.*')

        with open(out_file, 'w') as out:
            print "Start searching"
            for root, dirs, files in os.walk(top, topdown=False):
                for file in files:
                    m = p.match(file)
                    #print file
#                    statinfo = os.stat('{0}'.format(file.strip()))
#                    file_size = statinfo.st_size
#                    file_size = int(file_size)
#                    print "Size of file is %s" % file_size

                    if m:
                        out.write(os.path.join(root, m.group()))
                        out.write("\n")
                # print "Files Were Writed Down"


    def check_log_is_writing(self, file_f):
          log = '{0}/logs/{1}'.format(self.crs_dir, file_f)
          print log
          if os.stat(log).st_size != True:
             while True:
              stat1 = os.stat(log).st_mtime
              time.sleep(25)
              stat2 = os.stat(log).st_mtime
              if stat1 == stat2:
                 break
              else:
                 time.sleep(20)


    def analyzing_files(self, quality, channel_id, file_quantity):

          self.check_log_is_writing("file_info.log")
          g711 = ".*g711.*"
          g729 = ".*g729.*"
          g723 = ".*g723.*"
          wav = '{0}/voice/local/wav'.format(self.crs_storage_dir)

          if not os.path.exists(wav):
            os.makedirs(wav)

          file_f = '{0}/voice/local/recorded_list'.format(self.crs_storage_dir)

          with open(file_f, 'r') as inF:
                   for line in inF:
                       print line
                       if re.search(g729, line):
                          s = subprocess.check_call(["/usr/local/bin/g729decoder", "{0}".format(line.strip()), "{0}.raw".format(line.strip())])
                          s = subprocess.Popen(["/usr/bin/sox", "-r", " 8000", "-e", "signed", "-b", "16", "-c", "1", "{0}.raw".format(line.strip()), "{0}.wav".format(line.strip())])
                          returncode = s.wait()
                          print('sox of g729 returned {0}'.format(returncode))

                       if re.search(g711, line):
                          s = subprocess.Popen(["/usr/bin/sox", "-r", " 8000", "-e", "a-law", "-t", "raw", "-c", "1", "{0}".format(line.strip()), "{0}.wav".format(line.strip())])
                          returncode = s.wait()
                          print('sox of g711 returned {0}'.format(returncode))

                       if re.search(g723, line):
                          s = subprocess.Popen(["/root/bin/ffmpeg", "-c", "g723_1", "-f", "g723_1", "-i", "{0}".format(line.strip()), "-acodec", "pcm_u8", "{0}.wav".format(line.strip())])
                          returncode = s.wait()
                          print('sox of g723 returned {0}'.format(returncode))


          s = subprocess.Popen(["find", "{0}/voice/local/{1}/".format(self.crs_storage_dir,channel_id), "-name", "*.wav", "-exec", "cp", "{}", "{0}/voice/local/wav".format(self.crs_storage_dir), ";"])
          returncode = s.wait()
          print('find returned {0}'.format(returncode))

          os.chdir("/var/dejavu")
          log = open("{0}/voice/local/dejavu".format(self.crs_storage_dir), "w")

          files_wav = open("/usr/protei/Protei-CRS-Storage/voice/local/wav_files", "w")
          for files in os.listdir(wav):
              print >> files_wav, files
          files_wav.close()

          #self.del_file(self.crs_storage_dir)

          print "Determining quality..."
          for filename in os.listdir(wav):
              s = subprocess.Popen(["python", "dejavu.py", "--recognize", "file", "{0}/{1}".format(wav,filename)], stdout=log, stdin=log)
              returncode = s.wait()

          log.flush()
          log.close()
          print('dejavu returned {0}'.format(returncode))

          os.chdir("{0}/voice/local/".format(self.crs_storage_dir))

          p1 = subprocess.Popen(["grep", "confidence", "dejavu"], stdout=PIPE)
          p2 = subprocess.Popen(["awk", "{print $8}"], stdin=p1.stdout, stdout=subprocess.PIPE)
          p3 = subprocess.Popen(["awk", "{gsub(/,$/,\"\"); print}"], stdin=p2.stdout, stdout=subprocess.PIPE)

          p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
          p2.stdout.close()
          output = p3.communicate()[0]
          print output
          splits =  output.split()

          if  len(splits) != file_quantity:
             raise AssertionError("*ERROR* Expected quantity of files does not equals that Dejavu returned")

          splits = [ int(x) for x in splits ]
          min_ = min(splits)
          print "*INFO* Confidence is %s" % splits
          print "*INFO* Minimum quality file has %s confidence" % min_

          if  min_ >= quality:
             print "*INFO* All tracks have a good quality"
          else:
             raise AssertionError("*ERROR* There is a bad quality tracks" )


    def get_channel_list(self):
           channel = "\"ChannelID\" : 1,"
           descr = "\"Description\" : \"ATS channel\","
           status = "\"Status\" : \"OK\""
           s = subprocess.Popen(["curl", "--digest", "-u", "support:elephant", "http://192.168.108.26:8095/channels"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
           returncode = s.wait()
           print('CURL returned {0}'.format(returncode))
           outputlines = filter(lambda x:len(x)>0,(line.strip() for line in s.stdout))

           if channel and descr and status in outputlines:
              print "*INFO* BE API works!"
           else:
              raise AssertionError("*ERROR* BE API Doesn't work!")



    def get_mv_sip_rtp_time(self, mvsip_file):
        rtp_time = ""
        patt = '([0-9]+..[0-9]+..[0-9]+..[0-9]+).*RTP_AUDIO: Play during'
        #patt = '(.?[0-9]+\..?[0-9]+\..?[0-9]+\.[0-9]+).*RTP_AUDIO: Play during'
        with open(mvsip_file, 'r') as inF:
             for line in inF:
               if re.search(patt,line):
                   line = line.split("TX")[0].strip()
                   print line
                   line = line[1:-1]
                   if " " in line:
                      line = line.replace (" ", "0")
                      print line
                   line = line[0:8]
                   print line
                   rtp_time = line.replace(".", ":")
        print "*INFO* MV-SIP RTP time is %s" % rtp_time
        return rtp_time



    def ts_of_a_record_beginning(self,mvsip_file):
          #curl --digest -u root:elephant 'http://192.168.108.26:8095/search?ts_begin=2016-05-05&ts_end=2016-05-06&number=5000000'
          self.check_log_is_writing("file_info.log")
          rectified_list = []
          mvsip_rtp_time = self.get_mv_sip_rtp_time(mvsip_file)
          format = '%H:%M:%S'
          now = datetime.datetime.now()
          ts_begin = now.strftime("%Y-%m-%d")
          ts_end = now + datetime.timedelta(days=1)
          ts_end = ts_end.strftime("%Y-%m-%d")
          print "Current day time beginning %s" % ts_begin
          print "Current day time ending %s" % ts_end
          s = subprocess.Popen(["curl", "--digest", "-u", "root:elephant", "http://192.168.108.26:8095/search?channels=1&ts_begin={0}&ts_end={1}&number=5000000".format(ts_begin, ts_end)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          returncode = s.wait()
          print('CURL returned {0}'.format(returncode))
          #for line in s.stdout:
          #     print line
          outputlines = filter(lambda x:len(x)>25,(line.strip() for line in s.stdout))
          #outputlines = outputlines.decode('cp1251').encode('utf-8')
          print "CURL returned %s" % outputlines
          #print("\n".join(outputlines))
          #for item in outputlines:
              #item = item.decode("cp1251")
              #item = unicode(item, "utf-8")
              #encoded_utf8_list.append(item)
              #encoding = chardet.detect(item)
              #encoding = encoding['encoding']
              #print encoding
          #print "======================="
          #print encoded_utf8_list
          rectified_list =  [ x for x in outputlines if "Name" not in x ]
          rectified_list =  [ x for x in rectified_list if "Path" not in x ]
          print "*INFO* List without names %s" % rectified_list
          ts_begin = rectified_list[0][19:27]
          print "*INFO* Timestamp of beginning record %s" % ts_begin
          ts_end =  rectified_list[3][19:27]
          print "*INFO* Timestamp of ending record %s" % ts_end
          print "*INFO* MV-SIP RTP Start Record Time %s" % mvsip_rtp_time
          delta = datetime.datetime.strptime(ts_end, format) - datetime.datetime.strptime(ts_begin, format)
          print "*INFO* timedelta is %s" % delta
          if delta == datetime.timedelta(seconds=1) and ts_end == mvsip_rtp_time:
             print "*INFO* Timestamp of start file writing successfully checked!"
          else:
             raise AssertionError("*ERROR* Timestamp of start writing files is not the same as planned!")


    def check_fifo(self, log_file, port_start):
         #grep "start listen" trace.log | cut -d " " -f 7
         #grep "bind " trace.log | cut -d " " -f 7
         port_list = []
         port_start_fd = port_start[0:2]
         st_count = int(port_start)

         with open(log_file, 'r') as out:
                  for line in out:
                          p = re.match(('..*bind [0-9]+.[0-9]+.[0-9]+.[0-9]+:({0}[0-9]+)'.format(port_start_fd)), line)
                          if p:
                             port_list.append(int(p.group(1)))
         if len(port_list) == 0:
            raise AssertionError("*INFO* Don't Find Defined Ports")
         print "*INFO* Port list: %s" % port_list
         for line in port_list:
             if line == st_count:
                st_count += 1
             else:
                raise AssertionError("*ERROR* Ports are not sequentially allocated")



    @timeout(240, os.strerror(errno.ETIMEDOUT))
    def run_mts(self, mts_path, mts_test_file_path, logs_path, wait_flag, mode):
        #/var/mts/bin/startCmd.sh /var/mts/testsuites/writes_tx_rx_mx_g729/test.xml -seq -levelLog:DEBUG -stor:file -config:logs.STORAGE_DIRECTORY+../logs/writes_tx_rx_mx_g729/

        KillProcess("startCmd.sh", "startClass.sh")
        KillJava()
        wait_flag = int(wait_flag)
        mts_exec_command = mts_path + "/startCmd.sh "
        os.chdir(mts_path)
        mts_test_file_path = mts_test_file_path + " "
        mts_config = " -config:logs.STORAGE_DIRECTORY+../logs/{0}".format(logs_path)
        if mode == "parallel":
           mts_mode = " -par"
        else: 
           mts_mode = " -seq"
        mts_log_level = " -levelLog:ERROR"
        mts_storage = " -stor:file"
        # mts_gen_report = " -gen:true"
        # mts_show_report = " -show:true"
        mts_command = mts_exec_command + mts_test_file_path + mts_mode + mts_log_level + mts_storage      # + mts_gen_report + mts_show_report
        args = shlex.split(mts_command)
        self.mts_subprocess = Popen(["/bin/bash", "-c", "{0}".format(mts_command)], shell=False, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if wait_flag == 1:
            # returncode = self.mts_subprocess.wait()
            # print('mts command returned {0}'.format(returncode))
            self.mts_subprocess.communicate()

    def get_codec_and_type(self, file_name):
        m = file_name.strip().split('_')
        return (m[3], m[4])

    def get_name_codec_type(self, file_name):
        m = file_name.strip().split('_')
        return (m[0], m[1], m[2] ,m[3], m[4])

    def get_duration(self, file_name):
        m = file_name.strip().split('_')
        return (m[6])

    def get_crc(self, file_name):
        m = file_name.strip().split('_')
        return (m[5])



    def gen_channel_stat(self, channel_id):
        self.check_log_is_writing("file_info.log")
        file_f = '{0}/voice/local/recorded_list'.format(self.crs_storage_dir)
        self.find_voice_files(self.crs_storage_dir, file_f, channel_id)

        count = {}
        for line in open(file_f):
            codec, type_ = self.get_codec_and_type(line)
            if (codec, type_) not in count:
                count[(codec, type_)] = 1
            else:
                count[(codec, type_)] += 1

        list_count = sum(count.itervalues())

        codecs = set()
        for codec in count.keys():
            codecs.add(codec)

        whole_list = 1 if len(codecs) == 1 else 0    # если в канале все файлы с одиноковым кодеком
        # for (codec, type_), value in count.iteritems():
        #     print codec, type_, value
        print "*INFO* Codec, type and count: %s" % count
        print "*INFO* All elements have same codec and type? Yes =1, No = 0. All list elements = %s" % whole_list
        print "*INFO* Quantity of all files: %s" % list_count

        return (count, whole_list, list_count)

    def check_file_count(self, channel_id, expected_count):
        count, _, list_count = self.gen_channel_stat(channel_id)
        if list_count != expected_count:
            raise AssertionError("*ERROR* expected %s files, actual files are %s" % (expected_count, list_count))

    def check_file_codec(self, channel_id, codec, type_, expected_count):  # проверка кодека и типа
        rec_count, whole_list, list_count = self.gen_channel_stat(channel_id)
        count_summ = 0
        if whole_list == 0:
           for (c, t), count in rec_count.iteritems():
                #print c,t,count
                if c == codec and t == type_:
                   count_summ = count
           #print "Count summ is %s" % count_summ
           if count_summ == expected_count:
                print  "*INFO* Calculated count: %s with codec: %s and type: %s, Expected count: %s" % (count_summ, c, t, expected_count)
           else:
                raise AssertionError("*ERROR* expected %s file(s) with codec %s and type %s, recorded files are %s" % (expected_count, codec, type_, rec_count))

        if whole_list == 1:
           for (c, t), count in rec_count.iteritems():
                if c == codec and t == type_ and count == expected_count:
                   print  "*INFO* Calculated count: %s with codec: %s and type: %s, Expected count: %s" % (count, c, t, expected_count)
                else:
                   raise AssertionError("*ERROR* expected %s file(s) with codec %s and type %s, recorded files are %s" % (expected_count, codec, type_, rec_count))







    def move_recorded_file(self, name, channel_id):
        file_f = open('{0}/voice/local/recorded_list'.format(self.crs_storage_dir), "w")
        list_lines = []
        self.find_voice_files(self.crs_storage_dir, file_f, channel_id)
        file_f = '{0}/voice/local/recorded_list'.format(self.crs_storage_dir)
        p1 = subprocess.Popen(["cut", "-d", "_", "-f", "4-5", "{0}".format(file_f.strip())], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        buff_lines = p1.stdout.readlines()
        with open(file_f, 'r') as inF:
            for line in inF:
                print line
                if name in line:
                  line = line.strip()
                  os.chdir("/tmp")
                  retval = os.getcwd()
                  shutil.move(line, retval)




    def check_duration_of_file(self, codec_type, channel_id, expected_dur, relative_sec=0):
        self.check_log_is_writing("file_info.log")
        g711 = ".*g711.*"
        g729 = ".*g729.*"
        g723 = ".*g723.*"

        hex_list = []
        wav = '{0}/voice/local/wav'.format(self.crs_storage_dir)
        if not os.path.exists(wav):
            os.makedirs(wav)
        file_f = '{0}/voice/local/recorded_list'.format(self.crs_storage_dir)
        self.find_voice_files(self.crs_storage_dir, file_f, channel_id)


        count = []
        for line in open(file_f):
            id_, part, ts, c,t = self.get_name_codec_type(line)
            dur = self.get_duration(line)
            count.append((id_, part, ts, c, t, dur))

        with open(file_f, 'r') as inF:
                   for line in inF:
                       if re.search(g729, line):       #if codec_type in line:     #codec_type == 'g729' or codec_type == 'g729_tx' or codec_type == 'g729_rx' or codec_type == 'g729_mx' and 
                          s = subprocess.check_call(["/usr/local/bin/g729decoder", "{0}".format(line.strip()), "{0}.raw".format(line.strip())])
                          s = subprocess.Popen(["/usr/bin/sox", "-r", " 8000", "-e", "signed", "-b", "16", "-c", "1", "{0}.raw".format(line.strip()), "{0}.wav".format(line.strip())])
                          returncode = s.wait()
                          print('sox returned {0}'.format(returncode))

                       if re.search(g711, line):       #if codec_type in line:   #codec_type == 'g711' or codec_type == 'g711_tx' or codec_type == 'g711_rx' or codec_type == 'g711_mx' and 
                          s = subprocess.Popen(["/usr/bin/sox", "-r", " 8000", "-e", "a-law", "-t", "raw", "-c", "1", "{0}".format(line.strip()), "{0}.wav".format(line.strip())])
                          returncode = s.wait()
                          print('sox returned {0}'.format(returncode))

                       if re.search(g723, line):
                          s = subprocess.Popen(["/root/bin/ffmpeg", "-c", "g723_1", "-f", "g723_1", "-i", "{0}".format(line.strip()), "-acodec", "pcm_u8", "{0}.wav".format(line.strip())])
                          returncode = s.wait()
                          print('sox of g723 returned {0}'.format(returncode))


        s = subprocess.Popen(["find", "{0}/voice/local/{1}/".format(self.crs_storage_dir,channel_id), "-name", "*.wav", "-exec", "cp", "{}", "{0}/voice/local/wav".format(self.crs_storage_dir), ";"])
        returncode = s.wait()
        print('find returned {0}'.format(returncode))



        files_wav = open('{0}/voice/local/wav_files'.format(self.crs_storage_dir), "w")
        for files in os.listdir(wav):
              print >> files_wav, wav, "/", files

        files_wav = '{0}/voice/local/wav_files'.format(self.crs_storage_dir)

        for line in fileinput.FileInput('{0}/voice/local/wav_files'.format(self.crs_storage_dir), inplace=True):
              line = line.replace(" ", "")
              line = line.rstrip()
              print line

        final_duration = {}
        with open(files_wav, 'r') as inF:
             for line in inF:
                 f=open(line.strip(),"r")
                 f.seek(28)
                 a=f.read(4)
                 byteRate=0
                 for i in range(4):
                     byteRate=byteRate + ord(a[i])*pow(256,i)
                     fileSize=os.path.getsize(line.strip())
                 duration=((fileSize-44)*1000)/byteRate

                 if "g711" in line:
                    duration=duration - 1

                 ct = self.get_name_codec_type(line)
                 final_duration['_'.join(ct)] = duration

                 print "*INFO* Computed duration in base of 10: %s" % duration
                 duration = hex(duration)[2:]
                 print "*INFO* Computed duration in hex: %s" % duration
                 hex_list.append(duration)
                 f.close()

        print "*INFO* Got list of file, codec, type, durations:\n %s" % count

        comp_dur = []
        for _, _, _, _, _, dur in count:
            comp_dur.append(dur)

        if expected_dur == 0:
           print "*INFO* Computed hex list of durations:\n %s" %  hex_list
           if any(map(lambda v: v in comp_dur, hex_list)):   # check for list identical
              print "*INFO* Durations are equal"
           else:
              raise AssertionError("*ERROR* Durations don't match!")

        else:
           print "*INFO* Computed list of file, codec, type, durations in base of 10 dictionary:\n %s" % final_duration
           for key, value in final_duration.iteritems():

                      relative_duration_min = expected_dur - relative_sec
                      relative_duration_max = expected_dur + relative_sec
                      if codec_type in key:
                         if value >= relative_duration_min and value <= relative_duration_max:
                            value = int(value)
                            print "*INFO Duration Of File Within Range"
                         else:
                            raise AssertionError("*ERROR* Duration Of File Is Not In Range!")
        self.del_file(self.crs_storage_dir)




    def check_file_size(self, channel_id, min_file_size, max_file_size, file_mark, *words):

        self.check_log_is_writing("file_info.log")
        file_f = '{0}/voice/local/recorded_list'.format(self.crs_storage_dir)
        self.find_voice_files(self.crs_storage_dir, file_f, channel_id)

#если кодек и тип одинаковы 
        if file_mark == 0:
          with open(file_f, 'r') as inF:
             for line in inF:
                 print "*INFO* Recorded File is %s" % line
                 filesize=os.path.getsize(line.strip())
                 print "*INFO* Get File: %s, Get Size:%s " % (line, filesize)
                 filesize = int(filesize)
                 if filesize >= min_file_size and filesize <= max_file_size or filesize == kpv_file_size:
                    print "*INFO* File size is correct"
                 else:
                    raise AssertionError("*ERROR* Filesize is incorrect")

#если кодек и тип разные
        if file_mark == 1:
          for word in words:

           with open(file_f, 'r') as inF:
             for line in inF:
                 print "*INFO* Recorded File is %s" % line
                 if word in line:
                    filesize=os.path.getsize(line.strip())
                    print "*INFO* Get File: %s, Get Size:%s " % (line, filesize)
                    filesize = int(filesize)
                    if filesize >= min_file_size and filesize <= max_file_size or filesize == kpv_file_size:
                       print "*INFO* File size is correct"
                    else:
                       raise AssertionError("*ERROR* Filesize is incorrect")


    def check_file_size_part(self, channel_id, min_file_size, max_file_size, file_part, *words):
#если кодек и тип одинаковы, но разная длительность
          self.check_log_is_writing("file_info.log")
          file_f = '{0}/voice/local/recorded_list'.format(self.crs_storage_dir)
          self.find_voice_files(self.crs_storage_dir, file_f, channel_id)

          for word in words:

           with open(file_f, 'r') as inF:
             for line in inF:
                 print "*INFO* Recorded File is %s" % line
                 if word in line and file_part in line:
                    filesize=os.path.getsize(line.strip())
                    print "*INFO* Get File: %s, Get Size:%s " % (line, filesize)
                    if filesize >= min_file_size and filesize <= max_file_size or filesize == kpv_file_size:
                       print "*INFO* File size is correct"
                    else:
                       raise AssertionError("*ERROR* Filesize is incorrect")



    def replace_string(self, file_f,str1,str2):
        f = fileinput.FileInput(file_f, inplace=True)
        for line in f:
            s = line.replace(str1, str2)
            sys.stdout.write(s)

    def get_filename(self, mypath):
        file_f = ""
        for path, subdirs, files in os.walk(mypath):
            for name in files:
                #return os.path.join(path, name)
                file_f = os.path.join(path, name)
                print file_f
        return  file_f


    def get_integer(self, file_f, *strings):
        LIST__SET = []
        for arg in strings:
          with open(file_f, 'r') as inF:
             for line in inF:
               if re.search(arg,line):
                 s = line.split(" ")
                 s = s[2].split(";")
                 LIST__SET.append(s[0])
                 #print s
        print "*INFO* set is %s" % LIST__SET
        return LIST__SET



#    def monitor_file_is_not_empty(self, num_count, channel_id):
#          file_f = '{0}/voice/local/recorded_list'.format(self.crs_storage_dir)
#          self.find_voice_files(self.crs_storage_dir, file_f, channel_id)
#          count = 0
#          # if os.stat(file_f).st_size == 0:
#          #    raise AssertionError("*INFO* recorded_list is empty!")
#          while count != num_count:
#            with open(file_f, 'r') as inF:
#                 print "Wait while file(s) are writing"
#                 time.sleep(30)
#                 for line in inF:
#                   print "Line is %s" % line
#                   print "Count is %s" % count
#                   #file_size = os.path.getsize(line.strip())
#                   statinfo = os.stat('{0}'.format(line.strip()))
#                   file_size = statinfo.st_size
#                   file_size = int(file_size)
#                   print "Size of file is %s" % file_size
#                   if file_size > 0:
#                      count = count + 1
#                   else:
#                       raise AssertionError("*INFO* Recorded file size is empty!")
#          return True



          # while count != num_count:
          #   with open(file_f, 'r') as inF:
          #      for line in inF:
          #          time.sleep(2)
          #          print "Line is %s" % line
          #          print "Count is %s" % count
          #          statinfo = os.stat('{0}'.format(line.strip()))
          #          file_size = statinfo.st_size
          #          print "Size of file is %s" % file_size
          #          file_size = int(file_size)
          #          while file_size == 0:
          #             statinfo = os.stat('{0}'.format(line.strip()))
          #             file_size = statinfo.st_size
          #          count = count + 1
          # return True

    def check_file_exist(self, path, *files):
        for word in files:
            s = os.path.join(path, word)
            if os.path.exists(s):
               print "*INFO* File exist"
            else:
               raise AssertionError("*ERROR* File does not exist!")

    #@timeout(140, os.strerror(errno.ETIMEDOUT))
    def stop_voice(self, num_count, channel_id):
        #self.monitor_file_is_not_empty(num_count, channel_id)
        time.sleep(30)
        self.run_command("{0}/stop -f".format(self.crs_dir))

    #@timeout(140, os.strerror(errno.ETIMEDOUT))
    def stop_meta(self, num_count, channel_id):
        #self.monitor_file_is_not_empty(num_count, channel_id)
        time.sleep(30)
        self.run_command("{0}/stop -f".format(self.crs_meta_dir))


    def check_file_contain(self, file_f, wait_flag, *words):
        wait_flag = int(wait_flag)
        datafile = file(file_f)
        if wait_flag == 1:
           for word in words:
               datafile.seek(0)
               if word in datafile.read():
                  print "*INFO* File contain a %s section. All is good" % word
                  return True
               else:
                  return False

        else:

           for word in words:
               datafile.seek(0)
               if word in datafile.read():
                  print "*INFO* File contain a %s section. All is good" % word
               else:
                  raise AssertionError("*ERROR* File does not contain a %s section. Not good!" % word)


    def check_crc(self, channel_id):
        self.check_log_is_writing("file_info.log")
        file_f = '{0}/voice/local/recorded_list'.format(self.crs_storage_dir)
        self.find_voice_files(self.crs_storage_dir, file_f, channel_id)
        crc_list = []
        compute_crc_list = []

        for line in open(file_f):
            crc = self.get_crc(line)
            crc_list.append(crc)
        print "*INFO* Got %s crc_list" % crc_list

        file_f = '{0}/voice/local/recorded_list'.format(self.crs_storage_dir)
        with open(file_f, 'r') as inF:
            for line in inF:
                buf = open(line.strip(),'rb').read()
                buf = (binascii.crc32(buf) & 0xFFFFFFFF)
                crc32 = "%08X" % buf
                crc32 = str(crc32.lower())
                compute_crc_list.append(crc32)
        print "*INFO* Computed %s crc_list" % compute_crc_list
        if set(crc_list) != set(compute_crc_list):
           raise AssertionError("*ERROR* CRC32 doesnt match!")


    def check_time_of_file_creation(self, channel_id):

        self.check_log_is_writing("file_info.log")
        stat_lines = []
        file_f = '{0}/voice/local/recorded_list'.format(self.crs_storage_dir)
        self.find_voice_files(self.crs_storage_dir, file_f, channel_id)

        with open(file_f, 'r') as inF:
            for line in inF:
                statinfo = os.stat('{0}'.format(line.strip()))
                stat = statinfo.st_mtime
                print stat
                stat_lines.append(stat)
        identical =  all(x==stat_lines[0] for x in stat_lines)
        if identical == True:
           print "*INFO* Files time of creation is 01 Jan 1970"
        else:
           raise AssertionError("*ERROR* Files time of creation is NOT 01 Jan 1970")
                #(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(line.strip())
                #s = time.ctime(mtime)                #print "last modified: %s" % time.ctime(mtime)


    def check_file_exist(self, file_f, state):
        check = os.path.isfile(file_f)
        if (check == True and state == "1") or (check == False and state == "0"):
           return True
        elif (check == True and state == "0"):
             raise AssertionError("*ERROR* File exist!")
        elif check == False and state == "1":
             raise AssertionError("*ERROR* File does not exist!")

    @timeout(200, os.strerror(errno.ETIMEDOUT))
    def wait_for_record_in_file(self, file_f, wait_flag, *words):
        new_file = self.get_filename(file_f)
        while self.check_file_contain(new_file, wait_flag, *words) != True:
              self.check_file_contain(new_file, wait_flag, *words)
        return True

    def del_file(self, path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in [f for f in filenames if f.endswith(".wav") or f.endswith(".raw")]:
                file_f = os.path.join(dirpath, filename)
                os.remove(file_f)
        return 0

    def del_files_in_folder(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def emptying_file(self, path):
        open(path, 'w').close()

    def count_string_occurrence(self, file_f, qty, *words):
        count = 0
        for word in words:
            f = open(file_f)
            contents = f.read()
            count = contents.count(word)
            f.close()
        print "Number of string occurance is %s" % count
        if count == qty:
           print "*INFO* Quantity of occurenced strings is equal"
        else:
           raise AssertionError("*ERROR* Quantity of occurenced strings is not equal")


    def check_file_not_contain(self, file_f, *words):
        datafile = file(file_f)
        for word in words:
            datafile.seek(0)
            if word in datafile.read():
               raise AssertionError("*ERROR* Strings %s is in file!" % word)
            else:
              print "*INFO* File doees not contain a %s strings. Good" % word


    def list_files(self, path):
        list_f = []
        dirs = os.listdir(path)
        for file in dirs:
            list_f.append(file)
        if len(list_f) == 0:
           print "*INFO* Directory is empty"
        else:
           raise AssertionError("*ERROR* Directory is not empty")


    def find_text_block(self, file_f, marker, start, stop):
        data_list = []
        with open(file_f, "r") as f:
             data = f.read()
             pos =  0
             print "data is %s" % data
             print "type of data is %s" % type(data)
             #while data.find(marker) != -1:
             pos = data.find(marker)
             print "pos is %s" % pos
             start = data.find(start, pos)
             print "start is %s" % start
             stop = data.find(stop, pos)
             print "stop is %s" % stop
             if stop == -1 or start == -1 or data.find(marker) == -1:
                raise AssertionError("*ERROR* Requested string not found!" )
             data_list.append(data[start : stop+1].replace('\n', ''))
             #print "Datalist is %s" % data_list
             data = data[stop+1:]
             #print "data is %s" % data
        print("\n".join(data_list))
        if len(data_list) != 0:
           print "*INFO* Strings are in text block"
        else:
           raise AssertionError("*ERROR* Strings are not in text block!")


    def parse_sip_message(self, file_f, *messages):
        statinfo = os.stat(file_f)
        print "*INFO* Size of a file is %s" % statinfo.st_size
        if  statinfo.st_size == 0:
            raise AssertionError("*ERROR* Empty File!" )

        for message in messages:
            print message
            r = []
            datafile = file(file_f)
            r = datafile.read()
            patt = re.search('((.*\n){1}).*%s' % message, r)
            if not patt:
               raise AssertionError("*ERROR* String not found!")
            print patt.groups()[0].strip()
            time_of_message = re.split(' ', patt.groups()[0].strip())
            time_of_message = time_of_message[1][:8].strip()
            print time_of_message
            return time_of_message


    def parse_meta_logs(self, file_f, *messages):
        statinfo = os.stat(file_f)
        print "*INFO* Size of a file is %s" % statinfo.st_size
        if  statinfo.st_size == 0:
            raise AssertionError("*ERROR* Empty File!" )

        for message in messages:
            p1 = subprocess.Popen((["awk", "/%s/ {print $0}" % message, "{0}".format(file_f)]), stdout=subprocess.PIPE)    #awk '/ConnectionSetup/ { print $0 }' 2016-05-24\ 19\:00.log | cut -d " " -f2 | cut -d "." -f1
            p2 = subprocess.Popen(["cut", "-d", " ", "-f2"], stdin=p1.stdout, stdout=subprocess.PIPE)
            p3 = subprocess.Popen(["cut", "-d", ".", "-f1"], stdin=p2.stdout, stdout=subprocess.PIPE)

            p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
            p2.stdout.close()

            returncode = p3.wait()
            print('find returned {0}'.format(returncode))
            time_of_message = p3.stdout.readlines()[0].strip()
            #output = p1.communicate()
            #print output
            print time_of_message
            return time_of_message


    def check_event_time(self, sip_log_file, meta_log_file, sip_message, meta_message):
        if self.parse_sip_message(sip_log_file, sip_message) != self.parse_meta_logs(meta_log_file, meta_message):
           raise AssertionError("*ERROR* Time in SIP tranport and Meta Messages not equal!")
        else:
           print "*INFO* Time in SIP tranport and Meta Messages are equal!"


    def replace_string(self, file_f,str1,str2):
        f = fileinput.FileInput(file_f, inplace=True)
        for line in f:
            s = line.replace(str1, str2)
            sys.stdout.write(s)

    def umount_storage(self, storage):
        command = subprocess.Popen(["umount -l %s" % (storage)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = command.communicate()[0]
        print 'STDOUT:{0}'.format(stdout)
        command = subprocess.Popen(["for i in {4..5}; do losetup -d /dev/loop$i; done"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def mount_storage(self, storage):
        command = subprocess.Popen(["mount {0}.bin {0} -o loop".format(storage)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = command.communicate()[0]
        print 'STDOUT:{0}'.format(stdout)

    def check_for_alarms(self, file_f, *words):
        datafile = file(file_f)
        for word in words:
            datafile.seek(0)
            if word not in datafile.read():
               raise AssertionError("*ERROR* File does not contain a %s section. Not good!" % word)



#a = crsRemoteLibrary()
#a.setup_crs_path()
#a.mount_storage('/var/fs5')
#a.get_mv_sip_rtp_time("/usr/protei/Protei-MV.SIP/0/logs/RunTime.log")
#a.check_log_is_writing('file_info.log')
#print a.get_crc('/usr/protei/Protei-CRS-Storage/voice/local/4/112/e7/d03_0_aced5f41d7b2b807_g729_mx_c545d17c_185b0')
#a.get_storage_dir()
#a.find_voice_files("/usr/protei/Protei-CRS-Storage/", "/usr/protei/Protei-CRS-Storage/voice/local/recorded_list", "1")
#a.monitor_file_is_not_empty(5, "1")
#a.ts_of_a_record_beginning("/usr/protei/Protei-MV.SIP/0/logs/RunTime.log")

# a.analyzing_files(100, 1, 5)

# KillProcess("mts")
#a.check_duration_of_file("g723_mx" ,"1", 23000, 1000)
# a.check_duration_of_file("g729_rx" ,"1", 10000, 1000)
# a.check_duration_of_file_post_processing("g711_mx", "1", 7000, 1000)


if __name__ == '__main__':
  import sys
  from robotremoteserver import RobotRemoteServer
  RobotRemoteServer(crsRemoteLibrary(), *sys.argv[1:])
