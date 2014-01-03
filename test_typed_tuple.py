# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import unittest
import numpy as np
from typed_tuple import TypedTuple


class TypedTupleDefault(unittest.TestCase):

    def test_init_1(self):
        L = TypedTuple(np.arange(10))
        assert len(L) == 1

    def test_init_2(self):
        L = TypedTuple(np.arange(10),5)
        assert len(L) == 2

    def test_init_3(self):
        with self.assertRaises(TypeError):
            L = TypedTuple()

    def test_getitem_1(self):
        L = TypedTuple(np.arange(10),1+np.arange(4))
        assert np.allclose(L[3], [6,7,8,9])

    def test_getitem_2(self):
        Z = np.empty(10)
        L = TypedTuple(Z,1)
        assert np.allclose(L[:5], Z[:5])

    def test_setitem_1(self):
        Z = np.ones(10)
        L = TypedTuple(Z,1)
        L[:5] = 0
        assert np.allclose(L[:], [0,0,0,0,0,1,1,1,1,1])



# -----------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()

