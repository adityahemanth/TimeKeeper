#!/usr/bin/env python

import socket, threading
import time
import json
import ast

log = {}
dic = {}
clock = 0;



class ClientThread(threading.Thread):

    def __init__(self,ip,port,socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        print "[+] New thread started for "+ip+":"+str(port)


    def run(self):    

        global clock,log,clock

        rcv = c.recv(2048)

        pair = rcv.split("<>")

        clock += 1;
        if(len(pair) == 1):
            del dic[pair[0]]
            c.send("200")

        elif(len(pair) == 2):
            dic[pair[0]] = pair[1]
            c.send("200")

        else:
            c.send("404")

        log[clock] = rcv
        print("dict: ",dic)
        print("log: ",log)
        c.close();



def sendLog(self,tt,ip,port,socket):

    self.tt = tt
    for x in log:
        if(x >= tt):
            pass

host = "0.0.0.0"
port = 9999

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))
threads = []


while True:
    tcpsock.listen(4)
    (c, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, c)
    newthread.start()
    threads.append(newthread)
