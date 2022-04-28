# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 15:35:20 2014

@author: matthiasrambausek
"""

import numpy as np
import numpy.linalg as npl


class Jacobian(object):
    def __init__(self, node_container, int_point):
        self._node_container = node_container
        self._int_point = int_point
        int_point.dH = node_container.type.shape.getDerivativeArray(int_point.getNaturalCoordinates())
        self._calc()

    def _calc(self):
        coordinates = self._node_container.getCoordinateArray()
        self._J = np.dot(coordinates, self._int_point.dH)


class ElementJacobian(Jacobian):
    def __init__(self, element, int_point):
        Jacobian.__init__(self, element, int_point)

    def get(self):
        return self._J

    def getInv(self):
        return npl.inv(self._J)

    def getDet(self):
        J = self._J

        if J.shape[0] == J.shape[1]:
            return npl.det(J)
        elif min(J.shape) == 2:
            return npl.norm(np.cross(J[:, 0], J[:, 1]))
        else:
            return npl.norm(J[:, 0])

    def getDetOfInv(self):
        JInv = npl.inv(self._J)

        if JInv.shape[0] == JInv.shape[1]:
            return npl.det(JInv)
        elif min(JInv.shape) == 2:
            return npl.norm(np.cross(JInv[:, 0], JInv[:, 1]))
        else:
            return npl.norm(JInv[:, 0])
