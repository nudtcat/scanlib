#!/usr/bin/env pyhton
# -*- coding:utf-8 -*-

from gevent import monkey
monkey.patch_all()
import gevent
import Queue
import platform
from subprocess import Popen, PIPE
import re
import sys

file = sys.argv[1]

ip_queue = Queue.Queue()
with open(file, 'r') as f:
    for line in f:
        ip_queue.put(line.strip())

def pinger(ip, times=1):
    if platform.system() == 'Linux':
        p = Popen(['ping', '-c ' + str(times), ip], stdout=PIPE)
        m = re.search('[^0]\sreceived', p.stdout.read())
        if m is not None:
            return True
    if platform.system() == 'Windows':
        p = Popen('ping -n ' + str(times) + ' ' + ip, stdout=PIPE)
        m = re.search('TTL', p.stdout.read())
        if m:
            return True
    return False

def run():
    while True:
        try:
            ip = ip_queue.get(block=False)
        except:
            break
        if pinger(ip):
            print ip

l=[]
for i in range(50):
    g=gevent.spawn(run)
    l.append(g)
for g in l:
    g.join()

