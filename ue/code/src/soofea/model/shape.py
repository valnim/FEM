# -*- coding: utf-8 -*-

import numpy as np
import unittest
import plotly.graph_objects as go


class Lagrange(object):
    '''Klasse zur Implementierung von eindimensionalen Lagrange-Polynomen.
Siehe LV-Skriptum Kapitel 2.'''

    def __init__(self, node_positions):
        '''Konstruktor:
@param: node_positions - List der Stützstellen des Polynoms'''
        self._node_positions = node_positions
        self._order = len(node_positions) - 1

    def print_node_positions(self):
        # Ausgabe der Stützstellen
        print(self._node_positions)

    def get(self, r, index):
        '''Gibt den Wert des Lagrangepolynoms mit Index 'index' an der Stelle 'r' zurück.'''
        L = 1.0

        for i in range(self._order + 1):
            if i != index:
                L *= (r - self._node_positions[i]) / \
                     (self._node_positions[index] - self._node_positions[i])

        return L

    def der(self, r, index):
        '''Ableitung des Lagrange-Polynoms zur Stützstelle 'index' nach 'r'.'''
        factor_1 = 1.0
        for i in range(self._order + 1):
            if i != index:
                factor_1 /= self._node_positions[index] - self._node_positions[i]

        sum_i = 0.0
        for i in range(self._order + 1):
            if i != index:

                inner_factor = 1.0
                for j in range(self._order + 1):
                    if j != index and j != i:
                        inner_factor *= r - self._node_positions[j]
                sum_i += inner_factor

        return factor_1 * sum_i


class Shape(object):
    '''Abstrakte Basisklasse für Shapes'''

    def __init__(self, order, shape_dimension):
        self._order = order
        self.dimension = shape_dimension
        self._lagrange = Lagrange(self._calcNodePositions())

    def getNumberOfNodes(self):
        if not hasattr(self, 'number_of_nodes'):
            self._calcNumberOfNodes()
        return self.number_of_nodes

    def getArray(self, natural_coordinates):
        N = self.getNumberOfNodes()

        H = np.zeros((N, 1))
        for i in range(N):
            H[i, 0] = self.get(natural_coordinates, self.getNodeIndex(i))
        return H

    def getDerivativeArray(self, natural_coordinates):
        N = self.getNumberOfNodes()
        dH = np.zeros((N, self.dimension))

        for i in range(N):
            node_index = self.getNodeIndex(i)
            for j in range(self.dimension):
                dH[i, j] = self.der(natural_coordinates,
                                    node_index, j)

        return dH


class LinearShape(Shape):
    '''Klasse für 1D shapes'''

    def __init__(self, order):
        if order > 1:
            raise Exception('QuadShape only implemented for order <= 1')
        Shape.__init__(self, order, 1)

    def _calcNodePositions(self):
        return np.linspace(-1, 1, self._order + 1)

    def _calcNumberOfNodes(self):
        self.number_of_nodes = (self._order + 1)

    def get(self, natural_coordinates, node_index):
        return self._lagrange.get(natural_coordinates[0], node_index)

    def der(self, natural_coordinates, node_index, derivative_direction):
        return self._lagrange.der(natural_coordinates[0], node_index)

    def getNodeIndex(self, local_node_number):
        return local_node_number


class QuadShape(Shape):
    '''Klasse für quad shapes'''

    def __init__(self, order):
        if order > 1:
            raise Exception('QuadShape only implemented for order <= 1')
        Shape.__init__(self, order, 2)

    def _calcNodePositions(self):
        return np.linspace(-1, 1, self._order + 1)

    def _calcNumberOfNodes(self):
        self.number_of_nodes = (self._order + 1) ** 2

    def get(self, natural_coordinates, node_index):
        '''Gl. 2.9'''
        return self._lagrange.get(natural_coordinates[0], node_index[0]) * \
               self._lagrange.get(natural_coordinates[1], node_index[1])

    def der(self, natural_coordinates, node_index, derivative_direction):
        if derivative_direction == 0:
            return self._lagrange.der(natural_coordinates[0], node_index[0]) * \
                   self._lagrange.get(natural_coordinates[1], node_index[1])
        elif derivative_direction == 1:
            return self._lagrange.get(natural_coordinates[0], node_index[0]) * \
                   self._lagrange.der(natural_coordinates[1], node_index[1])

    def getNodeIndex(self, local_node_number):
        if local_node_number == 0:
            return [0, 0]
        elif local_node_number == 1:
            return [1, 0]
        elif local_node_number == 2:
            return [1, 1]
        elif local_node_number == 3:
            return [0, 1]

    def plot(self, local_node_number):
        res = 20
        x = np.linspace(-1, 1, res)
        y = np.linspace(-1, 1, res)
        xx, yy = np.meshgrid(x, y)
        zz = np.zeros_like(xx)
        node_index = self.getNodeIndex(local_node_number)
        for idx in range(res):
            for jdx in range(res):
                zz[idx, jdx] = self.get([x[idx], y[jdx]], node_index)
        fig = go.Figure(
            data=[go.Mesh3d(x=np.reshape(xx, res ** 2), y=np.reshape(yy, res ** 2), z=np.reshape(zz, res ** 2),
                            color='lightblue', opacity=0.50)])
        fig.show()


class HexShape(Shape):
    '''Klasse für hexaeder shapes'''

    def __init__(self, order):
        if order > 1:
            raise Exception('QuadShape only implemented for order <= 1')
        Shape.__init__(self, order, 3)

    def _calcNodePositions(self):
        return np.linspace(-1, 1, self._order + 1)

    def _calcNumberOfNodes(self):
        self.number_of_nodes = (self._order + 1) ** 3

    def get(self, natural_coordinates, node_index):
        '''Gl. 2.9'''
        return self._lagrange.get(natural_coordinates[0], node_index[0]) * \
               self._lagrange.get(natural_coordinates[1], node_index[1]) * \
               self._lagrange.get(natural_coordinates[2], node_index[2])

    def der(self, natural_coordinates, node_index, derivative_direction):
        if derivative_direction == 0:
            return self._lagrange.der(natural_coordinates[0], node_index[0]) * \
                   self._lagrange.get(natural_coordinates[1], node_index[1]) * \
                   self._lagrange.get(natural_coordinates[2], node_index[2])
        elif derivative_direction == 1:
            return self._lagrange.get(natural_coordinates[0], node_index[0]) * \
                   self._lagrange.der(natural_coordinates[1], node_index[1]) * \
                   self._lagrange.get(natural_coordinates[2], node_index[2])
        elif derivative_direction == 2:
            return self._lagrange.get(natural_coordinates[0], node_index[0]) * \
                   self._lagrange.get(natural_coordinates[1], node_index[1]) * \
                   self._lagrange.der(natural_coordinates[2], node_index[2])

    def getNodeIndex(self, local_node_number):
        if local_node_number == 0:
            return [0, 0, 0]
        elif local_node_number == 1:
            return [1, 0, 0]
        elif local_node_number == 2:
            return [1, 1, 0]
        elif local_node_number == 3:
            return [0, 1, 0]
        elif local_node_number == 4:
            return [0, 0, 1]
        elif local_node_number == 5:
            return [1, 0, 1]
        elif local_node_number == 6:
            return [1, 1, 1]
        elif local_node_number == 7:
            return [0, 1, 1]


class TriShape(Shape):
    '''Klasse für triangle shapes'''

    def __init__(self, order):
        if order > 1:
            raise Exception('QuadShape only implemented for order <= 1')
        Shape.__init__(self, order, 2)

    def _calcNodePositions(self):
        return np.array([-1.0, 1.0])

    def _calcNumberOfNodes(self):
        self.number_of_nodes = int((self._order + 1) * (self._order + 2) / 2)

    def get(self, natural_coordinates, node_index):
        '''Gl. 2.9'''
        xi = natural_coordinates[0]
        eta = natural_coordinates[1]

        if node_index == [0, 0]:
            val = 1.0 - xi - eta
        elif node_index == [1, 0]:
            val = xi
        elif node_index == [0, 1]:
            val = eta

        return val

    def der(self, natural_coordinates, node_index, derivative_direction):
        if derivative_direction == 0:
            if node_index == [0, 0]:
                val = -1
            elif node_index == [1, 0]:
                val = 1
            elif node_index == [0, 1]:
                val = 0
        elif derivative_direction == 1:
            if node_index == [0, 0]:
                val = -1
            elif node_index == [1, 0]:
                val = 0
            elif node_index == [0, 1]:
                val = 1

        return val

    def getNodeIndex(self, local_node_number):
        if local_node_number == 0:
            return [0, 0]
        elif local_node_number == 1:
            return [1, 0]
        elif local_node_number == 2:
            return [0, 1]


class TestShapeFunctions(unittest.TestCase):
    def setUp(self):
        self.l1 = Lagrange([-1., +1.])
        self.l2 = Lagrange([-1., 0., +1.])
        self.qshape1 = QuadShape(1);

    #        self.qshape2 = QuadShape( 2 );

    def testLagrangeGet(self):
        # Ex 2.2.

        for i in range(2):
            self.assertAlmostEqual(self.l1.get(self.l1._node_positions[i], i), 1.)

        for i in range(3):
            self.assertAlmostEqual(self.l2.get(self.l2._node_positions[i], i), 1.)
            for j in range(3):
                if (j != i):
                    self.assertAlmostEqual(self.l2.get(self.l2._node_positions[j], i), 0.)

    def testLagrangeDer(self):
        for i in range(2):
            self.assertAlmostEqual(self.l1.der(0.14, i), (-1) ** (i + 1) * 0.5)

        self.assertAlmostEqual(self.l2.der(-1., 0), -1.5)
        self.assertAlmostEqual(self.l2.der(0., 1), 0.)
        self.assertAlmostEqual(self.l2.der(+1., 2), 1.5)

    def testQuadShape(self):
        # Ex 2.3.
        np.testing.assert_almost_equal(self.qshape1.getArray([-1, -1]), np.array([[1, 0, 0, 0]]).T)
        np.testing.assert_almost_equal(self.qshape1.getArray([1, -1]), np.array([[0, 1, 0, 0]]).T)
        np.testing.assert_almost_equal(self.qshape1.getArray([1, 1]), np.array([[0, 0, 1, 0]]).T)
        np.testing.assert_almost_equal(self.qshape1.getArray([-1, 1]), np.array([[0, 0, 0, 1]]).T)

    #        np.testing.assert_almost_equal( self.qshape2.getArray( [-1,-1] ) , np.array([[1,0,0,0,0,0,0,0,0]]).T )
    #        np.testing.assert_almost_equal( self.qshape2.getArray( [1,-1] )  , np.array([[0,1,0,0,0,0,0,0,0]]).T )
    #        np.testing.assert_almost_equal( self.qshape2.getArray( [1,1] )   , np.array([[0,0,1,0,0,0,0,0,0]]).T )
    #        np.testing.assert_almost_equal( self.qshape2.getArray( [-1,1] )  , np.array([[0,0,0,1,0,0,0,0,0]]).T )
    #        np.testing.assert_almost_equal( self.qshape2.getArray( [0,-1] )  , np.array([[0,0,0,0,1,0,0,0,0]]).T )
    #        np.testing.assert_almost_equal( self.qshape2.getArray( [1,0] )   , np.array([[0,0,0,0,0,1,0,0,0]]).T )
    #        np.testing.assert_almost_equal( self.qshape2.getArray( [0,1] )   , np.array([[0,0,0,0,0,0,1,0,0]]).T )
    #        np.testing.assert_almost_equal( self.qshape2.getArray( [-1,0] )  , np.array([[0,0,0,0,0,0,0,1,0]]).T )
    #        np.testing.assert_almost_equal( self.qshape2.getArray( [0,0] )   , np.array([[0,0,0,0,0,0,0,0,1]]).T )

    def testQuadShapeDer(self):
        np.testing.assert_almost_equal(self.qshape1.getDerivativeArray([-1, -1]),
                                       np.array([[-0.5, 0.5, 0, 0], [-0.5, 0, 0, 0.5]]).T)
        np.testing.assert_almost_equal(self.qshape1.getDerivativeArray([1, -1]),
                                       np.array([[-0.5, 0.5, 0, 0], [0, -0.5, 0.5, 0]]).T)
        np.testing.assert_almost_equal(self.qshape1.getDerivativeArray([1, 1]),
                                       np.array([[0, 0, 0.5, -0.5], [0, -0.5, 0.5, 0]]).T)
        np.testing.assert_almost_equal(self.qshape1.getDerivativeArray([-1, 1]),
                                       np.array([[0, 0, 0.5, -0.5], [-0.5, 0, 0, 0.5]]).T)


if __name__ == '__main__':
    unittest.main()
