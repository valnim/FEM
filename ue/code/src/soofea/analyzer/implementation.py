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

    def calcVolumeLoad(self, element):
        F = methodIntegrate(self.volumeLoadIntegrator, element, element.int_points)
        return F

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

    def volumeLoadIntegrator(self, element, int_point, parameters=None):
        dim = element.node_list[0].getDimension()
        n_nodes = len(element.node_number_list)
        n_dofs = dim * n_nodes

        # Die Ansatzfunktionen werden im aktuellen Integrationspunkt
        # ausgewertet
        N = element.type.shape.getArray(int_point.getNaturalCoordinates())

        # Die Determinante der inversen Jacobimatrix wird berechnet
        jacobian = ElementJacobian(element, int_point)
        J_inv_det = jacobian.getDet()

        # Die Volumenlast wird aus dem Integrationspunkt ausgelesen
        b = int_point.volume_load
        if not b:
            b = np.zeros((dim, 1))

        # Der Kraftvektor wird berechnet
        F = np.zeros((dim, n_nodes))
        for idx in range(0, dim):
            for jdx in range(0, n_nodes):
                F[idx, jdx] = F[idx, jdx] + b[idx] * N[jdx] * J_inv_det

        return np.reshape(F, (n_dofs, 1), 'F')


class NonLinearElementImpl(ElementImpl):
    def calcStiffness(self, element):
        A_CC = methodIntegrate(NonLinearElementImpl._constitutiveComponentIntegrator, self, element.int_points, element)
        A_ISC = methodIntegrate(NonLinearElementImpl._initialComponentIntegrator, self, element.int_points, element)
        return A_CC + A_ISC

    def calcLoad(self, element):
        return - methodIntegrate(NonLinearElementImpl._internalForcesIntegrator, self, element.int_points, element)

    def _initialComponentIntegrator(self, int_point, element):
        dim = self.getDimension(element)
        n_nodes = element.getNumberOfNodes()
        dofs_per_element = dim * n_nodes

        _, E_green, dN, J, J_inv_det = self._calcKinematics(int_point, element)
        S = element.material.getSecondPK(E_green)
        delta = np.eye(dim)

        A_ISC = np.zeros([dim, n_nodes, dim, n_nodes])
        for idx in range(dim):
            for jdx in range(n_nodes):
                for kdx in range(dim):
                    for ldx in range(n_nodes):
                        for mdx in range(dim):
                            for ndx in range(dim):
                                for odx in range(dim):
                                    for pdx in range(dim):
                                        A_ISC[idx, jdx, kdx, ldx] += delta[idx, kdx] * dN[ldx, mdx] * J[mdx, ndx] \
                                                                     * S[ndx, odx] * dN[jdx, pdx] * J[pdx, odx] \
                                                                     * J_inv_det

        return np.reshape(A_ISC, (dofs_per_element, dofs_per_element), order='F')

    def _constitutiveComponentIntegrator(self, int_point, element):
        dim = self.getDimension(element)
        n_nodes = element.getNumberOfNodes()
        dofs_per_element = dim * n_nodes

        F, E_green, dN, J, J_inv_det = self._calcKinematics(int_point, element)
        CC = element.material.getElasticityMatrix(E_green)

        A_CC = np.zeros([dim, n_nodes, dim, n_nodes])
        for idx in range(dim):
            for jdx in range(n_nodes):
                for kdx in range(dim):
                    for ldx in range(n_nodes):
                        for mdx in range(dim):
                            for ndx in range(dim):
                                for odx in range(dim):
                                    for pdx in range(dim):
                                        for qdx in range(dim):
                                            for rdx in range(dim):
                                                A_CC[idx, jdx, kdx, ldx] += CC[mdx, ndx, odx, pdx] * F[idx, mdx] \
                                                                            * dN[ldx, qdx] * J[qdx, odx] * F[kdx, pdx] \
                                                                            * dN[jdx, rdx] * J[rdx, ndx] * J_inv_det

        return np.reshape(A_CC, (dofs_per_element, dofs_per_element), order='F')

    def _internalForcesIntegrator(self, int_point, element):
        dim = self.getDimension(element)
        n_nodes = element.getNumberOfNodes()
        dofs_per_element = n_nodes * dim

        F, E_green, dN, J, J_inv_det = self._calcKinematics(int_point, element)
        S = element.material.getSecondPK(E_green)

        F_int = np.zeros((dim, n_nodes))
        for idx in range(dim):
            for jdx in range(n_nodes):
                for kdx in range(dim):
                    for ldx in range(dim):
                        for mdx in range(dim):
                            F_int[idx, jdx] += F[idx, kdx] * S[kdx, ldx] * dN[jdx, mdx] * J[mdx, ldx] * J_inv_det

        return np.reshape(F_int, (dofs_per_element, 1), 'F')

    def _calcKinematics(self, int_point, element):
        jac_undeformed = ElementJacobian(element, int_point, 'undeformed')
        jac_deformed = ElementJacobian(element, int_point, 'spatial')
        I = np.identity(len(jac_undeformed.get()))

        F = np.linalg.inv(jac_deformed.get()) @ jac_undeformed.get()
        E_green = 1/2 * (F.T @ F - I)
        dN = element.type.shape.getDerivativeArray(int_point.getNaturalCoordinates())
        J = jac_undeformed.get()
        J_det_inv = jac_undeformed.getDet()

        return F, E_green, dN, J, J_det_inv

    # def volumeLoadIntegrator(self, element, int_point, parameters=None):
    #     dim = element.node_list[0].getDimension()
    #     n_nodes = len(element.node_number_list)
    #     n_dofs = dim * n_nodes
    #
    #     # Die Ansatzfunktionen werden im aktuellen Integrationspunkt
    #     # ausgewertet
    #     N = element.type.shape.getArray(int_point.getNaturalCoordinates())
    #
    #     # Die Determinante der inversen Jacobimatrix wird berechnet
    #     jacobian = ElementJacobian(element, int_point)
    #     J_inv_det = jacobian.getDet()
    #
    #     # Die Volumenlast wird aus dem Integrationspunkt ausgelesen
    #     b = int_point.volume_load
    #     if not b:
    #         b = np.zeros((dim, 1))
    #
    #     # Der Kraftvektor wird berechnet
    #     F = np.zeros((dim, n_nodes))
    #     for idx in range(0, dim):
    #         for jdx in range(0, n_nodes):
    #             F[idx, jdx] = F[idx, jdx] + b[idx] * N[jdx] * J_inv_det
    #
    #     return np.reshape(F, (n_dofs, 1), 'F')


class FaceImpl(object):
    def calcSurfaceLoad(self, face):
        F = methodIntegrate(self.surfaceLoadIntegrator, face, face.int_points)
        return F

    def surfaceLoadIntegrator(self, face, int_point, parameters=None):
        dim = face.node_list[0].getDimension()
        n_nodes = len(face.node_number_list)
        n_dofs = dim * n_nodes

        # Die Ansatzfunktionen werden im aktuellen Integrationspunkt
        # ausgewertet
        N = face.type.shape.getArray(int_point.getNaturalCoordinates())

        # Die Determinante der inversen Jacobimatrix wird berechnet
        jacobian = ElementJacobian(face, int_point)
        J_inv_det = jacobian.getDet()

        # Die Oberflächenlast wird aus dem Integrationspunkt ausgelesen
        t = int_point.surface_load
        if not t:
            t = np.zeros((dim, 1))

        # Der Kraftvektor wird berechnet
        F = np.zeros((dim, n_nodes))
        for idx in range(0, dim):
            for jdx in range(0, n_nodes):
                F[idx, jdx] = F[idx, jdx] + t[idx] * N[jdx] * J_inv_det

        return np.reshape(F, (n_dofs, 1), 'F')
