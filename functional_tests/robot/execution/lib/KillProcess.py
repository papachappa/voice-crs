import subprocess, signal, os

def KillProcess(*names):
    p = subprocess.Popen(['ps', 'ax'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.splitlines():
        for name in names:
            if name  in line:
               pid = int(line.split(None, 1)[0])
               os.kill(pid, signal.SIGKILL)

