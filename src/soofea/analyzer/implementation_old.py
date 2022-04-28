# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 16:34:11 2014

@author: matthiasrambausek
"""

import numpy as np
from soofea.numeric.num_int import methodIntegrate
# from soofea.numeric import kronecker
from soofea.analyzer.jacobian import ElementJacobian


class ElementImpl(object):
    def _get_dV(self, jacobian, element):
        volume = jacobian.getDet()
        if self.getDimension(element) == 2:
            volume *= element.type.height
        return volume

    def _coordinates_to_voigt(self, a):
        return a.flatten('F')

    def _get_permutations(self, a):
        if len(a) == 2:
            return np.array([[a[1], a[0]]])

        elif len(a) == 3:
            return np.array([[a[1], a[0], 0],
                             [0, a[2], a[1]],
                             [a[2], 0, a[0]]])

    def getDimension(self, element):
        return element.node_list[0].getDimension()


class LinearElementImpl(ElementImpl):
    def calcStrainStressInIp(self, element):
        for int_point in element.int_points:
            int_point.jacobian = ElementJacobian(element, int_point)
            int_point.dV = self._get_dV(int_point.jacobian, element)
            int_point.B = self._get_B_matrix(int_point.jacobian, element,
                                             int_point.getNaturalCoordinates())
            int_point.strain = int_point.B.dot(
                self._coordinates_to_voigt(element.getCoordinateArray())
            )
            int_point.C = element.material.getElasticityMatrix(
                dimension=self.getDimension(element)
            )
            int_point.stress = int_point.C.dot(int_point.strain)

    def _get_B_matrix(self, jacobian, element, natural_coordinates):
        h_derivatives = element.type.shape \
            .getDerivativeArray(natural_coordinates).dot(jacobian.getInv())
        N = element.getNumberOfNodes()
        blocks = [None] * N

        for i in range(N):
            h_der = h_derivatives[i, :]
            upper_m = np.diag(h_der)
            lower_m = self._get_permutations(h_der)
            blocks[i] = np.concatenate((upper_m, lower_m), axis=0)

        B = np.concatenate(blocks, axis=1)
        return B

    def calcStiffness(self, element):
        K_C = methodIntegrate(LinearElementImpl._constitutiveComponentIntegrator,
                              self, element.int_points, {})
        return K_C

    def _constitutiveComponentIntegrator(self, int_point, parameter):
        B = int_point.B
        C = int_point.C
        dV = int_point.dV

        return B.T.dot(C.dot(B)) * dV
