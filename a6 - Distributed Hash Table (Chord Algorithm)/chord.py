#!/bin/python

import math
import os
import random
import re
import sys
import time
import bisect

random.seed(123)
k_bit = 32

#
# Complete the Node and CircularLinkedList class below.
#

class Node:
    # implement here. see case1 below for required attributes
    def __init__(self, data, k=k_bit):
        self.id = random.getrandbits(k)
        self.data = data
        self.next = None
        self.finger = {}
    
    def __repr__(self):
        return str(self.id)
        
    
class CircularLinkedList:
    # implement here. see case 2 below for required attribute
    def __init__(self):
        self.head = None
        self.nodes = []
        self.node_ids = []
    
    def sorted_insert(self, node):
        if not self.head:
            self.head = node
            node.next = node
            self.nodes.append(node)
            self.node_ids.append(node.id)
        else:
            # Insert node
            ins_ind = bisect.bisect_left(self.node_ids, node.id)
            self.nodes.insert(ins_ind, node)
            self.node_ids.insert(ins_ind, node.id)
            # Update next attribute of node, and node before it if applicable
            if (ins_ind != len(self.nodes)-1):
                node.next = self.nodes[ins_ind+1]
            else:
                node.next = self.head
            if ins_ind:
                self.nodes[ins_ind-1].next = node
            # Update head of CLL
            self.head = self.nodes[0]
    
    def get_list(self):
        cllist = [(str(node.id), str(node.data), node.finger)
                  for node in self.nodes]
        return cllist
            
    
def distance(a, b, k=k_bit):
    # implement here. measures the clockwise distance from node a to node b with 
    # respect to the id.
    if b >= a:
        return b - a
    if a > b:
        return (2**k - a) + b
    
def find_node(start, key):
    node = start
    while True:
        if node.id == key:
            return node
        dist = distance(node.id, key)
        next_node = node.next
        next_dist = distance(next_node.id, key)
        if next_dist > dist:
            return node
        node, dist = next_node, next_dist
          
def store(start, key, value):
    # finds the node responsible for the key starting from the "start" node and 
    # returns the value of the key stored in that node
    node = find_node(start, key)
    node.data[key] = value
    return value
    
def lookup(start, key):
    #find the value stored at the key starting at the node "start" and traversing 
    # the list
    node = find_node(start, key)
    return node.data[key]
    
def update(node, k=k_bit):
    # updates the finger table for given node
    for i in range(k):
        finger_val = (node.id + 2**(i)) % 2**k
        s = find_node(node, key=finger_val)
        node.finger[i] = s

def find_finger(node, key, k=k_bit):
    # use the nodes finger table to get the node closest to the key
    # First check if starting node is the successor
    if node.id == key:
        return node
    dist = distance(node.id, key)
    next_dist = distance(node.next.id, key)
    if next_dist > dist:
        return node
    
    # If not, then find finger closest to key in node's finger table
    closest_finger = node
    prev_dist = distance(node.id, key)
    for i in range(k):
        if node.finger[i].id == key:
            return node.finger[i]
        dist = distance(node.finger[i].id, key)
        if dist > prev_dist:
            break
        closest_finger = node.finger[i]
        prev_dist = dist
    
    # Then repeat with the new starting node being the closest finger
    return find_finger(node=closest_finger, key=key)
    
def finger_lookup(start, key):
    # find the value stored at the key using finger table lookups starting with 
    # node "start"
    node = find_finger(start, key)
    if type(node.data) == dict:
        return node.data[key]
    else:
        return node.data
    
def finger_store(start, key, value):
    # store key value pair using finger tables starting with node "start"
    node = find_finger(start, key)
    if type(node.data) != dict:
        node.data = {}
    node.data[key] = value
    return value
    
def case3(fptr):
    # what is the largest possible node id in the network if k=32?
    answer = 2**32
    fptr.write(str(answer)+ '\n')

def setup1():
    arr = [x for x in range(0, 2 ** 5)]
    cll = CircularLinkedList()
    for i in range(len(arr)):
        temp = Node(arr[i])
        cll.sorted_insert(temp)
    current = cll.head
    while True:
        update(current)
        current = current.next
        if current == cll.head: break
    return cll


def case1(fptr):
    node = Node({}, k_bit)
    fptr.write(str(node.id) + '\n')
    fptr.write(str(node.data) + '\n') 
    fptr.write(str(node.next) + '\n')
    fptr.write(str(node.finger) + '\n')
    
def case2(fptr):
    cll = CircularLinkedList()
    fptr.write(str(cll.head) + '\n')
    l = [cll.sorted_insert(Node({}, k_bit)) for x in range(10)]
    cllist = cll.get_list()
    for e in cllist:
        for d in e:
            fptr.write(str(d) + ' ')
        fptr.write('\n')
        
def case4(fptr):
    d1 = distance(10, 10)
    d2 = distance(10, 100)
    d3 = distance(100, 10)
    fptr.write(str(d1) + '\n')
    fptr.write(str(d2) + '\n')
    fptr.write(str(d3) + '\n')
    
def case5(fptr):
    cll = CircularLinkedList()
    l = [cll.sorted_insert(Node({}, k_bit)) for x in range(10)]
    node = find_node(cll.head, 462568970)
    fptr.write(str(node.id) + '\n')
    fptr.write(str(node.data) + '\n')
    fptr.write(str(node.next.id) + '\n')
    
def case6(fptr):
    cll = CircularLinkedList()
    l = [cll.sorted_insert(Node({}, k_bit)) for x in range(10)]
    store(cll.head, 1606153229, 4)
    value = lookup(cll.head, 1606153229)
    fptr.write(str(value) + '\n')
    
def case7(fptr):
    # tests speed of regular insert
    arr = [x for x in range(0, 2 ** 12)]
    start = CircularLinkedList()
    start_time = time.time()
    for i in range(len(arr)):
        temp = Node(arr[i])
        start.sorted_insert(temp)
    process_time = time.time() - start_time
    print("SortedInsert took {} seconds".format(process_time))
    
def case8(fptr):
    cll = setup1()
    node = find_node(cll.head, 344973245)
    fptr.write(str(node.data)+'\n')
    n28 = node.finger[28]
    n30 = node.finger[30]
    fptr.write(str(n28.data)+ '\n')
    fptr.write(str(n30.data) + '\n')
    
def case9(fptr):
    cll = setup1()
    value = finger_lookup(cll.head, 344973245)
    fptr.write(str(value)+'\n')
    new_k = 2415140493
    finger_store(cll.head, new_k, 701)
    val = finger_lookup(cll.head, new_k)
    fptr.write(str(val) + '\n')
    node = find_node(cll.head, new_k)
    fptr.write(str(list(node.data.values())[0]) + '\n')
    fptr.write(str(node.id) + '\n')
    
    

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    
    case_num = input()
    
    globals()['case' + str(case_num)](fptr)

    fptr.close()