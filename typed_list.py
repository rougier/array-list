# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
"""
A List is a strongly typed list whose type can be anything that can be
interpreted as a numpy data type. 

Example
-------

>>> L = TypedList( [[0], [1,2], [3,4,5], [6,7,8,9]] )
>>> print L
[ [0] [1 2] [3 4 5] [6 7 8 9] ]
>>> print L.data
[0 1 2 3 4 5 6 7 8 9]

You can add several items at once by specifying common or individual size: a
single scalar means all items are the same size while a list of sizes is used to
specify individual item sizes.

Example
-------

>>> L = TypedList( np.arange(10), [3,3,4])
>>> print L
[ [0 1 2] [3 4 5] [6 7 8 9] ]
>>> print L.data
[0 1 2 3 4 5 6 7 8 9]

"""
import numpy as np


class TypedList(object):
    """
    A TypedList is a strongly typed list whose type can be anything that can be
    interpreted as a numpy data type.
    """

    def __init__(self, data=None, sizes=None, dtype=float):
        """ Create a new buffer using given data and sizes or dtype

        Parameters
        ----------

        data : array_like
            An array, any object exposing the array interface, an object
            whose __array__ method returns an array, or any (nested) sequence.

        sizes:  int or 1-D array
            If `itemsize is an integer, N, the array will be divided
            into elements of size N. If such partition is not possible,
            an error is raised.

            If `itemsize` is 1-D array, the array will be divided into
            elements whose succesive sizes will be picked from itemsize.
            If the sum of itemsize values is different from array size,
            an error is raised.

        dtype: np.dtype
            Any object that can be interpreted as a numpy data type.
        """

        if data is not None:
            if type(data) is np.ndarray:
                dtype = data.dtype
            elif type(data) in [list,tuple]:
                if type(data[0]) in [list,tuple]:
                    sizes = [len(l) for l in data]
                    data = [item for sublist in data for item in sublist]
                    data = np.array(data,copy=False)
                    dtype = data.dtype
                else:
                    data = np.array(data,copy=False)
                    dtype = data.dtype
            else:
                raise ValueError("Data type not understood")

        self._data = np.zeros(512, dtype=dtype)
        self._items = np.zeros((64,2), dtype=int)
        self._size = 0
        self._count = 0
        
        if data is not None:
            self.append(data,sizes)



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
        s = '[ '
        for item in self: s += str(item) + ' '
        s += ']'
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
            raise TypeError("List indices must be integers")


    def __setitem__(self, key, data):
        """ x.__setitem__(i, y) <==> x[i]=y """

        # Setting a specific dtype field for all items
        if type(key) is str:
            self._data[key][:self._size] = data

        # Setting a single item
        elif type(key) is int:
            if key < 0:
                key += len(self)
            if key < 0 or key > len(self):
                raise IndexError("List assignment index out of range")
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
            raise TypeError("List assignment indices must be integers")



    def __delitem__(self, key):
        """ x.__delitem__(y) <==> del x[y] """

        # Deleting a single item
        if type(key) is int:
            if key < 0:
                key += len(self)
            if key < 0 or key > len(self):
                raise IndexError("List deletion index out of range")
            istart, istop = key, key+1
            dstart,dstop = self._items[key]

        # Deleting several items
        elif type(key) is slice:
            istart, istop, step = key.indices(len(self))
            if istart > istop:
                istart,istop = istop,istart
            if istart == istop:
                return
            dstart = self._items[istart][0]
            dstop  = self._items[istop-1][1]
        # Error
        else:
            raise TypeError("List deletion indices must be integers")

        # Remove data
        size = self._size - (dstop-dstart)
        self._data[dstart:dstart+size] = self._data[dstop:dstop+size]
        self._size -= dstop-dstart

        # Remove corresponding items
        size = self._count - istop
        self._items[istart:istart+size] = self._items[istop:istop+size]

        # Update other items
        size = dstop-dstart
        self._items[istart:istop+size+1] -= size, size
        self._count -= istop-istart



    def insert(self, index, data, sizes=None):
        """ Insert data before index

        Parameters
        ----------

        index : int
            Index before which data will be inserted.

        data : array_like
            An array, any object exposing the array interface, an object
            whose __array__ method returns an array, or any (nested) sequence.

        sizes:  int or 1-D array
            If `itemsize is an integer, N, the array will be divided
            into elements of size N. If such partition is not possible,
            an error is raised.

            If `itemsize` is 1-D array, the array will be divided into
            elements whose succesive sizes will be picked from itemsize.
            If the sum of itemsize values is different from array size,
            an error is raised.
        """

        if type(data) in [list,tuple] and type(data[0]) in [list,tuple]:
            sizes = [len(l) for l in data]
            data = [item for sublist in data for item in sublist]

        data = np.array(data,copy=False).ravel()
        size = data.size

        # Default is one group with all data inside
        _sizes = np.ones(1)*data.size

        # Check item size and get item number
        if sizes is not None:
            if type(sizes) is int:
                if (size % sizes) != 0:
                    raise ValueError("Cannot partition data as requested")
                _count = size//sizes
                _sizes = np.ones(_count,dtype=int)*(size//_count)
            else:
                _sizes = np.array(sizes,copy=False)
                _count = len(sizes)
                if _sizes.sum() != size:
                    raise ValueError("Cannot partition data as requested")
        else:
            _count = 1

        # Check if data array is big enough and resize it if necessary
        if self._size + size  >= self._data.size:
            capacity = int(2**np.ceil(np.log2(self._size + size)))
            self._data = np.resize(self._data, capacity)

        # Check if item array is big enough and resize it if necessary
        if self._count + _count  >= len(self._items):
            capacity = int(2**np.ceil(np.log2(self._count + _count)))
            self._items = np.resize(self._items, (capacity, 2))
        
        # Check index
        if index < 0:
            index += len(self)
        if index < 0 or index > len(self):
            raise IndexError("List insertion index out of range")

        # Inserting
        if index < self._count:
            istart = index
            dstart = self._items[istart][0]
            dstop  = self._items[istart][1]
            # Move data
            self._data[dstart+size:self._size+size] = self._data[dstart:self._size]
            # Update moved items
            I = self._items[istart:self._count]+size
            self._items[istart+_count:self._count+_count] = I

        # Appending
        else:
            dstart = self._size
            istart = self._count

        # Only one item (faster)
        if _count == 1:
            # Store data
            self._data[dstart:dstart+size] = data
            self._size += size
            # Store data location (= item)
            self._items[istart][0] = dstart
            self._items[istart][1] = dstart+size
            self._count += 1

        # Several items
        else:
            # Store data
            dstop = dstart + size
            self._data[dstart:dstop] = data
            self._size += size

            # Store items
            items = np.ones((_count,2),int)*dstart
            C = _sizes.cumsum()
            items[1:,0] += C[:-1]
            items[0:,1] += C
            istop = istart + _count
            self._items[istart:istop] = items
            self._count += _count


    def append(self, data, sizes=None):
        """
        Append data to the end.

        Parameters
        ----------

        data : array_like
            An array, any object exposing the array interface, an object
            whose __array__ method returns an array, or any (nested) sequence.

        sizes:  int or 1-D array
            If `itemsize is an integer, N, the array will be divided
            into elements of size N. If such partition is not possible,
            an error is raised.

            If `itemsize` is 1-D array, the array will be divided into
            elements whose succesive sizes will be picked from itemsize.
            If the sum of itemsize values is different from array size,
            an error is raised.
        """

        self.insert(len(self), data, sizes)
