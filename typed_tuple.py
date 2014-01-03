# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
"""
A TypedTuple is a strongly typed tuple based on an existing numpy array. Size
is immutable while content can be changed if immutable has been set to False.

Example
-------

>>> L = TypedTuple( [[0], [1,2], [3,4,5], [6,7,8,9]] )
>>> print L
[ [0] [1 2] [3 4 5] [6 7 8 9] ]
>>> print L.data
[0 1 2 3 4 5 6 7 8 9]

You can specify several items at once by specifying common or individual sizes. A
single scalar means all items are the same size while a list of sizes is used to
specify individual item sizes.

Example
-------

>>> L = TypedTuple( np.arange(10), [3,3,4])
>>> print L
[ [0 1 2] [3 4 5] [6 7 8 9] ]
>>> print L.data
[0 1 2 3 4 5 6 7 8 9]
"""
import numpy as np


class TypedTuple(object):
    """
    A TypedTuple is a strongly typed tuple whose type can be anything that can be
    interpreted as a numpy data type.
    """

    def __init__(self, data, sizes=None, immutable=False):
        """ Create a new typed tuple using given data and sizes

        Parameters
        ----------

        data : array_like
            An array, any object exposing the array interface, an object
            whose __array__ method returns an array, or any (nested) sequence.

        sizes: int or 1-D array
            If `itemsize is an integer, N, the array will be divided
            into elements of size N. If such partition is not possible,
            an error is raised.

            If `itemsize` is 1-D array, the array will be divided into
            elements whose succesive sizes will be picked from itemsize.
            If the sum of itemsize values is different from array size,
            an error is raised.

        immutable : boolean
            Tells whether items content can be changed without modifying their
            size.
        """

        if type(data) in [list,tuple]:
            if type(data[0]) in [list,tuple]:
                sizes = [len(l) for l in data]
                data = [item for sublist in data for item in sublist]
        self._data = np.array(data, copy=False)
        self._size = self._data.size
        self._immutable = immutable

        # Default is one group with all data inside
        _sizes = np.ones(1)*data.size

        # Check item sizes and get items count
        if sizes is not None:
            if type(sizes) is int:
                if (self._size % sizes) != 0:
                    raise ValueError("Cannot partition data as requested")
                self._count = self._size//sizes
                _sizes = np.ones(self._count,dtype=int)*(self._size//self._count)
            else:
                _sizes = np.array(sizes, copy=False)
                self._count = len(sizes)
                if _sizes.sum() != self._size:
                    raise ValueError("Cannot partition data as requested")
        else:
            self._count = 1

        # Store items
        self._items = np.zeros((self._count,2),int)
        C = _sizes.cumsum()
        self._items[1:,0] += C[:-1]
        self._items[0:,1] += C


    @property
    def data(self):
        """ The array's elements, in memory. """
        return self._data[:self._size]


    @property
    def size(self):
        """ Number of base elements, in memory. """
        return self._size


    @property
    def dtype(self):
        """ Describes the format of the elements in the buffer. """
        return self._data.dtype


    def __len__(self):
        """ x.__len__() <==> len(x) """
        return self._count


    def __str__(self):
        s = '( '
        for item in self: s += str(item) + ' '
        s += ')'
        return s


    def __getitem__(self, key):
        """ x.__getitem__(y) <==> x[y] """

        # Getting a specific dtype field for all items
        if isinstance(key,str):
            return self._data[key][:self._size]

        # Getting data for a single item
        elif type(key) is int:
            if key < 0:
                key += len(self)
            if key < 0 or key >= len(self):
                raise IndexError("Tuple index out of range")
            dstart = self._items[key][0]
            dstop  = self._items[key][1]
            return self._data[dstart:dstop]

        # Getting data for several items at once
        elif type(key) is slice:
            istart, istop, step = key.indices(len(self))
            if istart > istop:
                istart,istop = istop,istart
            dstart = self._items[istart][0]
            if istart == istop:
                dstop = dstart
            else:
                dstop  = self._items[istop-1][1]
            return self._data[dstart:dstop]

        # Error
        else:
            raise TypeError("Tuple indices must be integers")


    def __setitem__(self, key, data):
        """ x.__setitem__(i, y) <==> x[i]=y """

        if self._immutable:
            raise TypeError("This tuple is immutable")

        # Setting a specific dtype field for all items
        if type(key) is str:
            self._data[key][:self._size] = data

        # Setting a single item
        elif type(key) is int:
            if key < 0:
                key += len(self)
            if key < 0 or key > len(self):
                raise IndexError("Tuple assignment index out of range")
            dstart = self._items[key][0]
            dstop  = self._items[key][1]
            self._data[dstart:dstop] = data

        # Setting several items at once
        elif type(key) is slice:
            istart, istop, step = key.indices(len(self))
            if istart > istop:
                istart,istop = istop,istart
            if istart == istop:
                dstart = self._items[key][0]
                dstop  = self._items[key][1]
                self._data[dstart:dstop] = data
            else:
                if istart > len(self) or istop > len(self):
                    raise IndexError("Can only assign iterable")
                dstart = self._items[istart][0]
                if istart == istop:
                    dstop = dstart
                else:
                    dstop  = self._items[istop-1][1]
                self._data[dstart:dstop] = data
        # Error
        else:
            raise TypeError("Tuple assignment indices must be integers")
