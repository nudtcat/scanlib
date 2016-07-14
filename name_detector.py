#!/usr/bin/env python
#-*- coding:utf-8 -*-

from gevent import monkey
monkey.patch_all()
import gevent
import Queue
import sys
import socket

main_domain=sys.argv[1]

name_queue=Queue.Queue()
with open("dict/dns_prefix/dns-namesA.txt","r") as f:
    for line in f:
        name_queue.put(line.strip()+"."+main_domain)

def names(name):
    try:
        ip=socket.gethostbyname(name)
        print name,ip
    except socket.gaierror:
        pass

def run():
    while True:
        try:
            name=name_queue.get(block=False)
        except:
            break
        names(name)

l=[]
for i in range(50):
    g=gevent.spawn(run)
    l.append(g)
for g in l:
    g.join()
