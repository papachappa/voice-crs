import subprocess, signal, os
from subprocess import Popen, PIPE
import subprocess


def KillProcess(*names):
    p = subprocess.Popen(['ps', 'ax'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.splitlines():
        for name in names:
            if name  in line:
               pid = int(line.split(None, 1)[0])
               os.kill(pid, signal.SIGKILL)



def KillJava():
     p1 = subprocess.Popen(["netstat", "-nap"], stdout=PIPE)
     p2 = subprocess.Popen(["grep", "java"], stdin=p1.stdout, stdout=subprocess.PIPE)
     p3 = subprocess.Popen(["grep", "udp"], stdin=p2.stdout, stdout=subprocess.PIPE)
     p4 = subprocess.Popen(["awk", "{print $6}"], stdin=p3.stdout, stdout=subprocess.PIPE)
     p5 = subprocess.Popen(["cut", "-d", "/", "-f", "1"], stdin=p4.stdout, stdout=subprocess.PIPE)

     output = p5.communicate()[0]
     output = output.split('\n')
     del output[-1]

     p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
     p2.stdout.close()
     p3.stdout.close()
     p4.stdout.close()
     p5.stdout.close()
     for pid in output:
         pid = int(pid)
         os.kill(pid, signal.SIGKILL)



