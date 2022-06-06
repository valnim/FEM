# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 16:34:11 2014

@author: matthiasrambausek
"""

import numpy as np
from soofea.numeric.num_int import methodIntegrate
# from soofea.numeric import kronecker
from soofea.analyzer.jacobian import ElementJacobian, BoundaryJacobian


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

    def calcLoad(self, element):
        F = methodIntegrate(self.volumeLoadIntegrator, element, element.int_points)
        return F

    def volumeLoadIntegrator(self, int_point, element, parameters=None):
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


class LinearFaceImpl(object):
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


class NonlinearFaceImpl(object):
    def calcStiffness(self, face):
        A_p = methodIntegrate(self._pressureStiffnessIntegrator, face, face.int_points)
        A = A_p
        return A

    def calcLoad(self, face):
        F_p = methodIntegrate(self._pressureForcesIntegrator, face, face.int_points)
        F = -F_p
        return F

    def _pressureStiffnessIntegrator(self, face, int_point, parameters=None):
        dim = face.node_list[0].getDimension()
        n_nodes = len(face.node_number_list)
        dofs_per_face = dim * n_nodes

        p, N, dN, levi, a, b = self.calcstuff(face, int_point)

        if dim == 2:
            dN = np.hstack((dN, np.zeros((len(dN), 1))))

        delta = np.eye(dim)

        A_p = np.zeros((3, n_nodes, 3, n_nodes))
        for i in range(2):
            for j in range(n_nodes):
                for k in range(2):
                    for l in range(n_nodes):
                        for m in range(2):
                            for n in range(2):
                                A_p[i, j, k, l] += p * N[j] * levi[i, m, n] * (dN[l, 0] * b[n] * delta[k, m] + dN[l, 1] * a[m] * delta[k, n])
        A_p = A_p[0: dim, :, 0: dim, :]
        return np.reshape(A_p, (dofs_per_face, dofs_per_face), 'F')

    def _pressureForcesIntegrator(self, face, int_point, parameters=None):
        dim = face.node_list[0].getDimension()
        n_nodes = len(face.node_number_list)
        dofs_per_face = dim * n_nodes

        p, N, _, levi, a, b = self.calcstuff(face, int_point)

        F_p = np.zeros((3, n_nodes))
        for i in range(2):
            for j in range(n_nodes):
                for k in range(2):
                    for l in range(2):
                        F_p[i, j] += p * N[j] * levi[i, k, l] * a[k] * b[l]
        F_p = F_p[0: dim, :]
        return np.reshape(F_p, (dofs_per_face, 1), 'F')

    def calcstuff(self, face, int_point):
        jac = BoundaryJacobian(face, int_point, 'spatial')

        levi = self.makeLeviCvita()

        a = jac.a
        b = jac.b

        N = face.type.shape.getArray(int_point.getNaturalCoordinates())
        dN = face.type.shape.getDerivativeArray(int_point.getNaturalCoordinates())

        p = int_point.pressure

        return p, N, dN, levi, a, b

    def makeLeviCvita(self):
        levi = np.zeros((3, 3, 3))

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    if i == 1 and j == 2 and k == 3 or i == 2 and j == 3 and k == 1 or i == 3 and j == 1 and k == 2:
                        levi[i, j, k] = 1
                    elif i == 1 and j == 3 and k == 2 or i == 2 and j == 1 and k == 3 or i == 3 and j == 2 and k == 1:
                        levi[i, j, k] = -1
        return levi

class NonlinearElementImpl(ElementImpl):
    def calcStiffness(self, element):
        A_CC = methodIntegrate(NonlinearElementImpl._constitutiveComponentIntegrator,
                               self, element.int_points, element)
        A_ISC = methodIntegrate(NonlinearElementImpl._initialStressComponentIntegrator,
                                self, element.int_points, element)
        return A_CC + A_ISC

    def _constitutiveComponentIntegrator(self, int_point, element):
        dim = self.getDimension(element)
        n_nodes = len(element.node_number_list)
        dofs_per_element = dim * n_nodes

        # Calculate all relevant quantities.
        [F, E, dN, J, J_det_inv] = self.calcKinematics(element, int_point)

        # Calculate the material elasticity tensor
        CC = element.material.getElasticityMatrix(E)

        # Implementation of the constitutive component of the stiffness matrix
        A_CC = np.zeros((dim, n_nodes, dim, n_nodes))
        for i in range(dim):
            for j in range(n_nodes):
                for k in range(dim):
                    for l in range(n_nodes):
                        for m in range(dim):
                            for n in range(dim):
                                for o in range(dim):
                                    for p in range(dim):
                                        for q in range(dim):
                                            for r in range(dim):
                                                A_CC[i, j, k, l] += CC[m, n, o, p] * F[i, m] * dN[l, q] * J[q, o] \
                                                                   * F[k, p] * dN[j, r] * J[r, n] * J_det_inv

        # Reshaping the stiffness matrix from a 4th order matrix into a 2nd order matrix
        return np.reshape(A_CC, (dofs_per_element, dofs_per_element), 'F')

    def _initialStressComponentIntegrator(self, int_point, element):
        dim = self.getDimension(element)
        n_nodes = len(element.node_number_list)
        dofs_per_element = dim * n_nodes

        # Calculate all relevant quantities.
        [_, E, dN, J, J_det_inv] = self.calcKinematics(element, int_point)

        # Calculation of PK2 tensor
        S = element.material.getSecondPK(E)

        # Kronecker-delta
        delta = np.eye(dim)

        # Implementation of the initial stress component of the stiffness matrix
        A_ISC = np.zeros((dim, n_nodes, dim, n_nodes))
        for i in range(dim):
            for j in range(n_nodes):
                for k in range(dim):
                    for l in range(n_nodes):
                        for m in range(dim):
                            for n in range(dim):
                                for o in range(dim):
                                    for p in range(dim):
                                        A_ISC[i, j, k, l] += delta[i, k] * dN[l, m] * J[m, n] * S[n, o] * dN[j, p]\
                                                             * J[p, o] * J_det_inv
        return np.reshape(A_ISC, (dofs_per_element, dofs_per_element), 'F')

    def _internalForcesIntegrator(self, int_point, element, parameters=None):
        dim = element.node_list[0].getDimension()
        n_nodes = len(element.node_number_list)
        n_dofs = dim * n_nodes

        [F, E, dN, J, J_det_inv] = self.calcKinematics(element, int_point)

        S = element.material.getSecondPK(E)

        F_int = np.zeros((dim, n_nodes))
        for i in range(dim):
            for j in range(n_nodes):
                for k in range(dim):
                    for l in range(dim):
                        for m in range(dim):
                            F_int[i, j] += F[i, k] * S[k, l] * dN[j, m] * J[m, l] * J_det_inv

        return np.reshape(F_int, (n_dofs, 1), 'F')


    def calcKinematics(self, element, int_point):

        jac_undeformed = ElementJacobian(element, int_point, configuration='undeformed')

        jac_deformed = ElementJacobian(element, int_point, configuration='spatial')

        I = np.identity(len(jac_undeformed.getInv()))

        F = np.linalg.inv(jac_deformed.getInv()) @ jac_undeformed.getInv()

        E = 0.5 * (np.transpose(F) @ F-I)

        dN = element.type.shape.getDerivativeArray(int_point.getNaturalCoordinates())
        J = jac_undeformed.getInv()
        J_det_inv = jac_undeformed.getDet()

        return F, E, dN, J, J_det_inv


    def calcLoad(self, element):
        # Volume Forces
        #F_volume = methodIntegrate(NonlinearElementImpl.volumeLoadIntegrator, self, element.int_points, element)

        # internal Forces
        F_int = methodIntegrate(NonlinearElementImpl._internalForcesIntegrator, self, element.int_points, element)

        F = - F_int #+ F_volume
        return F

    def volumeLoadIntegrator(self, int_point, element, parameters=None):
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