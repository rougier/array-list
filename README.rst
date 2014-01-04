ArrayList
---------

An ArrayList is a strongly typed list whose underlying structure is a contiguous
numpy array. An element of the list is a sequence of elementary dtyped values.
Element can be appended/inserted individually::

    >>> L = TypedList(dtype = int)
    >>> L.append(0)
    >>> L.append([1,2,3])
    >>> print L
    [ [0] [1 2 3] ]

They can also be appended/inserted by groups if group size(s) is specified::

    >>> L = TypedList(dtype = int)
    >>> L.append(np.arange(10), 2)
    >>> print L
    [ [0 1] [2 3] [4 5] [6 7] [8 9] ]
    >>> L = TypedList(np.arange(10), [2,3,5])
    >>> print L
    [ [0 1] [2 3 4] [5 6 7 8 9] ]

Each item can be easily accessed using sliced notation::

    >>> L = TypedList(np.arange(10), 1+np.arange(4))
    >>> print L[3]
    [6 7 8 9]
    >>> L[1:3] += 1
    >>> print L
    [ [0] [2 3] [4 5 6] [6 7 8 9] ]

The underlying array can be accessed using the `data` property::

    >>> L = TypedList(np.arange(10), 1+np.arange(4))
    >>> print L.data
    [ 0 1 2 3 4 5 6 7 8 9 ]
