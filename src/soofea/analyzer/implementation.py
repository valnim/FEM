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

    def getDimension(self, element):
        return element.node_list[0].getDimension()


class LinearElementImpl(ElementImpl):
    def calcStiffness(self, element):
        K_C = methodIntegrate(LinearElementImpl._constitutiveComponentIntegrator,
                              self, element.int_points, element)
        return K_C

    def _constitutiveComponentIntegrator(self, int_point, element):
        dim = self.getDimension(element)
        n_nodes = len(element.node_number_list)
        dofs_per_element = dim * n_nodes

        dN = element.type.shape.getDerivativeArray(int_point.getNaturalCoordinates())

        jacobian = ElementJacobian(element, int_point)
        J = jacobian.getInv()
        J_det = jacobian.getDet()

        C = element.material.getElasticityMatrix(dim)

        K_elem = np.zeros([dim, n_nodes, dim, n_nodes])
        for i in range(dim):
            for j in range(n_nodes):
                for k in range(dim):
                    for l in range(n_nodes):
                        for m in range(dim):
                            for n in range(dim):
                                for o in range(dim):
                                    for p in range(dim):
                                        K_elem[i, j, k, l] += C[i, m, k, n] * dN[l, o] * J[o, n] * dN[j, p] * J[
                                            p, m] * J_det

        return np.reshape(K_elem, (dofs_per_element, dofs_per_element), order='F')

    def calcVolumeLoad(self, element):
        F = methodIntegrate(self.volumeLoadIntegrator, element, element.int_points)
        return F

    def volumeLoadIntegrator(self, element, int_point, parameters=None):
        dim = element.node_list[0].getDimension()
        n_nodes = len(element.node_number_list)
        n_dofs = dim * n_nodes

        # % Die Ansatzfunktionen werden im aktuellen Integrationspunkt
        # % ausgewertet
        N = element.type.shape.getArray(int_point.getNaturalCoordinates())

        # % Die Determinante der inversen Jacobimatrix wird berechnet
        jacobian = ElementJacobian(element, int_point)
        J_inv_det = jacobian.getDet()

        # % Die Volumenlast wird aus dem Integrationspunkt ausgelesen
        b = int_point.volume_load
        if not b:
            b = np.zeros((dim, 1))

        # % Der Kraftvektor wird berechnet
        F = np.zeros((dim, n_nodes))
        for i in range(0, dim):
            for j in range(0, n_nodes):
                F[i, j] = F[i, j] + b[i] * N[j] * J_inv_det

        return np.reshape(F, (n_dofs, 1), 'F')


class FaceImpl(object):
    def calcSurfaceLoad(self, face):
        F = methodIntegrate(self.surfaceLoadIntegrator, face, face.int_points)
        return F

    def surfaceLoadIntegrator(self, face, int_point, parameters=None):
        dim = face.node_list[0].getDimension()
        n_nodes = len(face.node_number_list)
        n_dofs = dim * n_nodes

        # % Die Ansatzfunktionen werden im aktuellen Integrationspunkt
        # % ausgewertet
        N = face.type.shape.getArray(int_point.getNaturalCoordinates())

        # % Die Determinante der inversen Jacobimatrix wird berechnet
        jacobian = ElementJacobian(face, int_point)
        J_inv_det = jacobian.getDet()

        # % Die Oberflächenlast wird aus dem Integrationspunkt ausgelesen
        t = int_point.surface_load
        if not t:
            t = np.zeros((dim, 1))

        # % Der Kraftvektor wird berechnet
        F = np.zeros((dim, n_nodes))
        for i in range(0, dim):
            for j in range(0, n_nodes):
                F[i, j] = F[i, j] + t[i] * N[j] * J_inv_det

        return np.reshape(F, (n_dofs, 1), 'F')
