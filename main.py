#!/usr/local/bin/python2
import os
import pexpect
import os
import struct
import fcntl
import termios
import signal
import sys
system_ip="XXX.XXX.XXX.XXX"
name="username"
password="password"
def sigwinch_passthrough (sig, data):
    winsize = getwinsize()
    global child
    child.setwinsize(winsize[0],winsize[1])

def getwinsize():
    """This returns the window size of the child tty.
    The return value is a tuple of (rows, cols).
    """
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912L
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]


child=pexpect.spawn("ssh {}@{}".format(name,system_ip))
child.expect("Verification code")
Key=os.popen("./authenticator.py").read().replace("\n","")
child.sendline(Key)
child.expect("Password")
child.sendline("{}".format(password))
signal.signal(signal.SIGWINCH, sigwinch_passthrough)
winsize = getwinsize()
child.setwinsize(winsize[0], winsize[1])
child.interact()
child.close()
