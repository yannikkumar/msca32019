#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socketserver
import numpy as np
from time import sleep 
import random
import threading
 
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            # take 1000 obs from standard normal distro and send them across the network.
            sample = np.random.randn(1000)
            sample = ','.join([str(val) for val in sample])
            encoded_sample = sample.encode('utf-8')
            self.request.sendall(encoded_sample)
        except:
            print("Server-side exception.")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass



if __name__ == '__main__':
    print("setting up")
    server = ThreadedTCPServer((HOST,PORT))
    print("shuttung down")