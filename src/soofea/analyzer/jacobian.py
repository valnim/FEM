# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 15:35:20 2014

@author: matthiasrambausek
"""

import numpy as np
import numpy.linalg as npl


class Jacobian(object):
    def __init__(self, node_container, int_point, configuration='undeformed'):
        self._node_container = node_container
        self._int_point = int_point
        self._configuration = configuration
        int_point.dH = node_container.type.shape.getDerivativeArray(int_point.getNaturalCoordinates())
        self._calc()

    def _calc(self):
        coordinates = self._node_container.getCoordinateArray(self._configuration)
        self._J = np.dot(coordinates, self._int_point.dH)


class ElementJacobian(Jacobian):
    def __init__(self, element, int_point, configuration='undeformed'):
        Jacobian.__init__(self, element, int_point, configuration)

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


class BoundaryJacobian(Jacobian):
    def __init__(self, boundary, int_point, configuration='undeformed'):
        Jacobian.__init__(self, boundary, int_point, configuration)
        self.a = None
        self.b = None
        self.calcTangentVectors()

    def calcTangentVectors(self):
        J = self._J # TODO check if this is correct
        dimJ = min(J.shape)

        if dimJ == 2:
            self.a = J[:, 0]
            self.b = J[:, 1]
        elif dimJ == 1:
            self.a = np.zeros((3, 1))
            self.a[0:2, 0] = J[:, 0]
            self.b = np.zeros((3, 1))
            self.b[2, 0] = 1
        else:
            raise Exception('Jacobian has wrong dimension')

