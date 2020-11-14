#!/bin/python3

import math
import os
import random
import re
import sys
import json
import unittest





# you will need to pass the test cases below. test_D will be called 4 different times to test that orders are
# handled properly. test_B, C, and D will each be called once to ensure that all handle methods are impelemented.

class OrderBook:
    def __init__(self):
        self.list_asks = []
        self.list_bids = []
        # the list of bids and offers is self explanatory. 
        # the orders attribute keeps a record of all the orders where they key is the order id and the
        # value is the order. If used correctly, this should help you implement the handle methods below.
        self.orders = {}
    
    def handle_order(self, o):
        if o['action']=='new':
            self.handle_new(o)
        elif o['action']=='modify':
            self.handle_modify(o)
        elif o['action']=='delete':
            self.handle_delete(o)
        else:
            print('Error-Cannot handle this action')
            
    def handle_new(self, o):
        self.orders[o['id']] = o
        list_orders = None
        desc = False
        if o['side'] == "ask":
            list_orders = self.list_asks
        elif o['side'] == "bid":
            list_orders = self.list_bids
            desc = True
        list_orders.append(o)
        list_orders.sort(key=lambda x: x['price'], reverse=desc)

    def handle_modify(self,o):
        previous = self.orders[o['id']]
        if previous['side'] == "ask":
            self.list_asks[self.list_asks.index(previous)]['quantity'] = o['quantity']
        elif previous['side'] == "bid":
            self.list_bids[self.list_bids.index(previous)]['quantity'] = o['quantity']
        self.orders[o['id']]['quantity'] = o['quantity']
        
    def handle_delete(self,o):
        to_delete = self.orders.pop(o['id'])
        if to_delete['side'] == "ask":
            self.list_asks.pop(self.list_asks.index(to_delete))
        elif to_delete['side'] == "bid":
            self.list_bids.pop(self.list_bids.index(to_delete))
        
    def find_order_in_a_list(self,o,lookup_list = None):
        pass

    def display_content(self,fptr):
    # you certainly don't need to touch this part
        fptr.write('BIDS\n')
        for o in self.list_bids:
            fptr.write("%d %d %d\n" % (o['id'],o['price'],o['quantity']))
        fptr.write('OFFERS\n')
        for o in self.list_asks:
            fptr.write("%d %d %d\n" % (o['id'],o['price'],o['quantity']))