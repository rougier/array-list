# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import time
import numpy as np
from array_list import ArrayList


n = 100000

l = []
t = time.clock()
for i in xrange(n):
    l.append(i)
t0 = time.clock() -t 

L = np.ones(0)
t = time.clock()
for i in xrange(n):
    L = np.append(L,i)
t1 = time.clock() -t 

a = ArrayList(dtype=int)
t = time.clock()
for i in xrange(n):
    a.append(i)
t2 = time.clock() -t 

a = ArrayList(dtype=int)
t = time.clock()
for i in xrange(n/1000):
    a.append(i+np.arange(1000),1)
t3 = time.clock() -t 

a = ArrayList(dtype=int)
t = time.clock()
a.append(i+np.arange(n),1)
t4 = time.clock() -t 

print "python list:              %.3fs" % (t0)
print "numpy array:              %.3fs" % (t1)
print "ArrayList (batch=1):      %.3fs" % (t2)
print "ArrayList (batch=1000):   %.3fs" % (t3)
print "ArrayList (batch=100000): %.3fs" % (t4)
