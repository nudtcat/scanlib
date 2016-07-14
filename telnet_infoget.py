#!/usr/bin/env python
#-*- coding:utf-8 -*-

import socket
import sys
from gevent import monkey
monkey.patch_all()
import gevent
import Queue

timeout = 5
socket.setdefaulttimeout(timeout)

ip_queue=Queue.Queue()
with open("10.23.txt","r") as f:
    for line in f:
        ip_queue.put(line.strip())

def telneter(host):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host,23))
        s.recv(2048)
        s.sendall(b"fffd01")
        return s.recv(2048)
    except:
        return None

fout=open("result.txt","w")
def run():
    while True:
        try:
            ip=ip_queue.get(block=False)
        except:
            break
        message=telneter(ip)
        if message is not None:
            fout.write(ip+"\n")
            fout.write(message+"\n")
            fout.write("================================\n")
            sys.stdout.write("=")

l=[]
for i in range(50):
    g=gevent.spawn(run)
    l.append(g)
for g in l:
    g.join()
fout.close()
