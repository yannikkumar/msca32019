#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socket
import statistics
import threading

thread_number = 10
res_mean = [None] * thread_number
res_stdev = [None] * thread_number
 
    
class TCPClient(threading.Thread):

    def __init__(self, offset, host, port):
        super().__init__()
        self.offset = offset
        self.host = host
        self.port = port

    def work_with_server(self):
        global res_mean
        global res_stdev
        # set up socket 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # connect to server
                sock.connect((self.host, self.port))
                
                while not (res_mean[self.offset] or res_stdev[self.offset]):
                    # receive data from server
                    received_data = sock.recv(4096)
                    if received_data:
                        decoded_sample = received_data.decode('utf-8')
                        sample = [float(val) for val in decoded_sample.split(',')
                                if val]
                        res_mean[self.offset] = statistics.mean(sample)
                        res_stdev[self.offset] = statistics.stdev(sample)
                    else:
                        print("No data received.")
            except Exception:
                print(f"Client-side exception: {sys.exc_info()[1]}")
            finally:
                pass


    def run(self):
        self.work_with_server()