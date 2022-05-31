from soofea.base import NumberedObject

import numpy as np


class Material(NumberedObject):
    def __init__(self, number):
        NumberedObject.__init__(self, number)


class LinearStVenantKirchhoffMaterial(Material):
    def __init__(self, number, E, nu, twodim_type='plane_strain'):
        Material.__init__(self, number)
        self._E = E
        self._nu = nu
        self._twodim_type = twodim_type

    def getElasticityMatrix(self, dimension=3):

        lam = self._nu * self._E / ((1 + self._nu) * (1 - 2 * self._nu))
        mu = self._E / (2 * (1 + self._nu))

        if self._twodim_type == 'plane_stress':
            lam = 2 * mu * lam / (lam + 2 * mu)

        delta = np.identity(dimension)

        C = np.zeros([dimension, dimension, dimension, dimension])
        for idx in range(dimension):
            for jdx in range(dimension):
                for kdx in range(dimension):
                    for ldx in range(dimension):
                        C[idx, jdx, kdx, ldx] = lam * delta[idx, jdx] * delta[kdx, ldx] + mu * (
                                    delta[idx, kdx] * delta[jdx, ldx] + delta[jdx, kdx] * delta[idx, ldx])

        return C


class HyperelasticStVenantKirchhoffMaterial(Material):
    def __init__(self, number, E, nu, twodim_type='plane_strain'):
        Material.__init__(self, number)
        self._E = E
        self._nu = nu
        self._twodim_type = twodim_type

    def getElasticityMatrix(self, E_green):
        dimension = len(E_green)
        lam = self._nu * self._E / ((1 + self._nu) * (1 - 2 * self._nu))
        mu = self._E / (2 * (1 + self._nu))

        if self._twodim_type == 'plane_stress':
            lam = 2 * mu * lam / (lam + 2 * mu)

        delta = np.identity(dimension)

        C = np.zeros([dimension, dimension, dimension, dimension])
        for i in range(dimension):
            for j in range(dimension):
                for k in range(dimension):
                    for l in range(dimension):
                        C[i, j, k, l] = lam * delta[i, j] * delta[k, l] + mu * (
                                    delta[i, k] * delta[j, l] + delta[j, k] * delta[i, l])

        return C

    def getSecondPK(self, E_green):
        lam = self._nu * self._E / ((1 + self._nu) * (1 - 2 * self._nu))
        mu = self._E / (2 * (1 + self._nu))

        if self._twodim_type == 'plane_stress':
            lam = 2 * mu * lam / (lam + 2 * mu)

        return lam * E_green.T @ np.identity(len(E_green)) + 2 * mu * E_green
