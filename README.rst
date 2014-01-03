Numpy objects
=============

This is a small collection of objects based on numpy array.


TypedList
---------

A TypedList is a strongly type list whose underlying structure is a contiguous
numpy array. An element of the list is a sequence of elementary dtyped values.
Element can be appended/inserted individually::

    >>> L = TypedList(dtype = int)
    >>> L.append(0)
    >>> L.append([1,2,3])
    >>> print L
    [ [0] [1 2 3] ]

But they can also be appended/inserted by groups, provided group size(s) has
been specified::

    >>> L = TypedList(dtype = int)
    >>> L.append(np.arange(10), 2)
    >>> print L
    [ [0 1] [2 3] [4 5] [6 7] [8 9] ]

Each item can be then accessed using sliced notation::

    >>> L = TypedList(np.arange(10), 1+np.arange(4))
    >>> print L[3]
    [6 7 8 9]
    >>> L[3] += 1
    [7 8 9 10]

The underlying array can be accessed using the `data` property::

    >>> L = TypedList(np.arange(10), 1+np.arange(4))
    >>> print L.data
    [ 0 1 2 3 4 5 6 7 8 9 ]
    >>> L[2] += 1
    print L.data
    [ 0 1 2 4 5 6 6 7 8 9 ]


TypedTuple
----------

A TypeTuple is a fixed size TypedList whose size is determined at creation::

    >>> Z = np.arange(10)
    >>> T = TypedTuple(Z, 1+np.arange(4))
    >>> T[3] += 1
    >>> print Z
    [ 0 1 2 3 4 5 7 8 9 10 ]

It can be made immutable by specifying so at creation time::

    >>> T = TypedTuple(np.arange(10), 1+np.arange(4), immutable=True)
