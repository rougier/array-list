# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import time
import numpy as np
from typed_list import TypedList


n = 100000

l = []
t = time.clock()
for i in xrange(n):
    l.append(i)
t0 = time.clock() -t 

a = TypedList(dtype=int)
t = time.clock()
for i in xrange(n):
    a.append(i)
t1 = time.clock() -t 

a = TypedList(dtype=int)
t = time.clock()
for i in xrange(n/1000):
    a.append(i+np.arange(1000),1)
t2 = time.clock() -t 

a = TypedList(dtype=int)
t = time.clock()
a.append(i+np.arange(n),1)
t3 = time.clock() -t 

print "list:                %.3fs" % (t0)
print "List (batch=1):      %.3fs" % (t1)
print "List (batch=1000):   %.3fs" % (t2)
print "List (batch=100000): %.3fs" % (t3)
